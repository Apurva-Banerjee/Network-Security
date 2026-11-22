'''the setup.py is an essemtial part of packaging and distributing Python Projects. 
It is used by setuptools to define the configuration of the project such as meta data , dependencies and more
'''

from setuptools import setup, find_packages
from typing import List


HYPHEN_E_DOT = "-e ."


def get_requirements(file_path: str) -> List[str]:
    """
    This function returns the list of requirements from requirements.txt
    """
    requirements: List[str] = []
    try:
        with open(file_path, "r", encoding="utf-8") as file_obj:
            for line in file_obj:
                req = line.strip()
                if req and not req.startswith("#") and req != HYPHEN_E_DOT:
                    requirements.append(req)
    except FileNotFoundError as e:
        print(f"Requirements file not found at {file_path}: {e}")
        raise

    return requirements

# print(get_requirements("requirements.txt"))

setup(
    name="Network Security",
    version="0.0.1",
    author="Banerjee",
    author_email="banerjeeapurv84@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt"),
    
)