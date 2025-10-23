"""Asynchronous execution engine for LLMs_OS"""
import asyncio
import aiohttp
import yaml
from typing import Dict, Any, List
from concurrent.futures import ThreadPoolExecutor
from .exceptions import WorkflowExecutionError
from .validators import WorkflowValidator
from .monitoring import MetricsCollector
from .registry import get_action

class AsyncExecutor:
    """Execute workflows asynchronously"""
    
    def __init__(self, max_workers: int = 10):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()
        self.executor.shutdown(wait=True)
    
    async def execute_task(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single task asynchronously"""
        action = task.get('action')
        action_func = get_action(action)
        
        if not action_func:
            raise WorkflowExecutionError(f"Action not found: {action}")
        
        # Check if action is async
        if asyncio.iscoroutinefunction(action_func):
            result = await action_func(task, context, session=self.session)
        else:
            # Run sync function in thread pool
            result = await asyncio.get_event_loop().run_in_executor(
                self.executor, action_func, task, context
            )
        
        return result or {}
    
    async def execute_parallel_tasks(self, tasks: List[Dict], context: Dict) -> Dict:
        """Execute multiple tasks in parallel"""
        tasks_to_run = []
        
        for task in tasks:
            if task.get('parallel', False):
                tasks_to_run.append(self.execute_task(task, context))
            else:
                # Execute sequential task and wait
                if tasks_to_run:
                    results = await asyncio.gather(*tasks_to_run, return_exceptions=True)
                    tasks_to_run = []
                
                result = await self.execute_task(task, context)
                context.update(result)
        
        # Execute remaining parallel tasks
        if tasks_to_run:
            results = await asyncio.gather(*tasks_to_run, return_exceptions=True)
        
        return context

async def execute_yaml_async(file_path: str) -> None:
    """Execute workflow from YAML file asynchronously"""
    with open(file_path, 'r', encoding='utf-8') as f:
        workflow = yaml.safe_load(f)
    
    # Validate workflow
    WorkflowValidator.validate(workflow)
    
    # Execute with metrics tracking
    with MetricsCollector.track_workflow():
        async with AsyncExecutor() as executor:
            context = {}
            tasks = workflow.get('tasks', [])
            await executor.execute_parallel_tasks(tasks, context)
