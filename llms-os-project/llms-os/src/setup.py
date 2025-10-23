"""Setup configuration for LLMs_OS"""
from setuptools import setup, find_packages

setup(
    name="LLMs_OS",
    version="2.0.0",
    description="Enhanced Workflow Automation System with LLMs",
    author="LLMs_OS Team",
    packages=find_packages(),
    install_requires=[
        "pyyaml>=6.0.1",
        "jinja2>=3.1.2",
        "requests>=2.31.0",
        "aiohttp>=3.9.1",
        "prometheus-client>=0.19.0",
        "python-dotenv>=1.0.0",
        "colorama>=0.4.6",
        "rich>=13.7.0",
        "tenacity>=8.2.3",
        "pydantic>=2.5.3",
        "jsonschema>=4.20.0",
    ],
    entry_points={
        "console_scripts": [
            "llms-os=LLMs_OS.cli:main",
        ],
    },
    python_requires=">=3.10",
)
