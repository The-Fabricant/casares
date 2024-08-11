from setuptools import setup, find_packages

setup(
    name='Casares',
    version='0.4',
    packages=find_packages(),
    install_requires=[
        'Flask>=1.1.2',
        'Pillow>=8.1.0',
    ],
    author='Marco Marchesi',
    author_email='marco@thefabricant.com',
    description='A server as a python decorator',
)
