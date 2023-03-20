from setuptools import setup, find_packages

setup(
    name='quotexapi',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'websocket-client'
    ],
    entry_points={
        'console_scripts': [
            'quotexapi=quotexapi.__main__:main'
        ]
    }
)
