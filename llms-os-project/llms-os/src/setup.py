from setuptools import setup, find_packages

setup(
    name="LLMs_OS",
    version="2.0.0",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'llms-os=LLMs_OS.cli:main',
        ],
    },
    python_requires='>=3.10',
)
