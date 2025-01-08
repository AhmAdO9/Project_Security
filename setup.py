
''' The setup.py file is an essential part of packaging and distributing Python projects. It is used by setuptools (or distutils in older python versions) to define the configuration of your project, such as it's metadata, dependencies, and more. '''


from typing import List
from setuptools import setup, find_packages
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import CustomException

def get_requirements(file_path:str)->List[str]:

    HYPHEN_E_DOT = "-e ."
    
    """This function is going to return the list of required packages"""
    try:
        packages:List[str] = []
        with open(file_path, 'r') as file_object:
            for package in file_object.readlines():
                package = package.strip()
                if package == HYPHEN_E_DOT:
                    pass
                else:
                    packages.append(package)

        return packages
    except Exception as e:
        raise CustomException(e, sys)


setup(
    name='NetworkSecurity',
    version="1.0.0",
    author='Faheem',
    email='adahm7114@gmail.com',
    packages = find_packages(),
    install_requires = get_requirements('requirements.txt')
)
