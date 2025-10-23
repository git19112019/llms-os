"""Plugin system for extending LLMs_OS"""
import importlib
import inspect
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any, List

class PluginInterface(ABC):
    """Base interface for all plugins"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Plugin name"""
        pass
    
    @property
    @abstractmethod
    def version(self) -> str:
        """Plugin version"""
        pass
    
    @abstractmethod
    def execute(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute plugin logic"""
        pass
    
    @abstractmethod
    def validate(self, task: Dict[str, Any]) -> bool:
        """Validate task configuration"""
        pass

class PluginManager:
    """Manage plugin discovery and loading"""
    
    def __init__(self):
        self.plugins: Dict[str, PluginInterface] = {}
        self.plugin_dir = Path(__file__).parent / 'plugins'
    
    def discover_plugins(self) -> List[str]:
        """Auto-discover plugins in plugin directory"""
        discovered = []
        
        if not self.plugin_dir.exists():
            self.plugin_dir.mkdir(parents=True, exist_ok=True)
            return discovered
        
        for plugin_file in self.plugin_dir.glob('*.py'):
            if plugin_file.name.startswith('_'):
                continue
            
            module_name = f"LLMs_OS.plugins.{plugin_file.stem}"
            
            try:
                module = importlib.import_module(module_name)
                
                # Find plugin classes
                for name, obj in inspect.getmembers(module):
                    if (inspect.isclass(obj) and 
                        issubclass(obj, PluginInterface) and 
                        obj != PluginInterface):
                        
                        plugin_instance = obj()
                        self.plugins[plugin_instance.name] = plugin_instance
                        discovered.append(plugin_instance.name)
                        
            except Exception as e:
                print(f"Failed to load plugin {module_name}: {e}")
        
        return discovered
    
    def get_plugin(self, name: str) -> PluginInterface:
        """Get plugin by name"""
        return self.plugins.get(name)
    
    def list_plugins(self) -> List[str]:
        """List all loaded plugins"""
        return list(self.plugins.keys())

# Global plugin manager instance
plugin_manager = PluginManager()
