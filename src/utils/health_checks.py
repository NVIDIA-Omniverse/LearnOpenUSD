# Copyright (c) 2024, NVIDIA CORPORATION. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Health check utilities to confirm USD visualization within Jupyter Notebooks can be performed."""

import logging
import os
from packaging.specifiers import SpecifierSet
from packaging.version import Version
import requests
import sys
from typing import List

log = logging.getLogger(__name__)


class StacklessException(RuntimeError):
    """Exception without a stack trace, used for clear and concise User-facing information."""

    def __init__(self, msg: str) -> None:
        self.args = msg,
        sys.exit(self)
 

def get_current_python_version() -> Version:
    """
    Return the version of the current Python environment.
    
    Parameters:
        None

    Return:
        Version: The version of the current Python environment.

    """
    return Version(f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    # return Version("12.0.1")


def is_pip_package_compatible(package_id: str, python_version: Version = get_current_python_version()) -> bool:
    """
    Validate if the given PIP package name is compatible with the given Python environment version.
    
    Parameters:
        package_id (str): Name of the PIP package for which to validate the compatibility against the PYPI repository.

    Return:
        bool: `True` if the given package name is compatible with the given Python environment version, `False`
            otherwise.

    """
    # Fetch the package's metadata from PIP's JSON API:
    response = requests.get(f"https://pypi.org/pypi/{package_id}/json")
    if response.status_code != 200:
        raise Exception(f'Error fetching package metadata for "{package_id}".')

    data = response.json()

    # Extract the `info.requires_python` field:
    requires_python = data["info"].get("requires_python")
    if not requires_python:
        # If the `requires_python` information is not specified, assume the package is compatible:
        return True

    # Check compatibility using the `packaging` library:
    specifier = SpecifierSet(requires_python)

    return python_version in specifier


def list_packages_from_requirements(file_path: str = "./requirements.txt") -> List[str]:
    """
    Return the list of package names contained in the given "requirements.txt" file.
    
    Parameters:
        file_path (str): Path to the "requirements.txt" file.
    
    Return:
        List[str]: The list of package names contained in the given "requirements.txt" path, or an empty list if the
            file does not exist.

    """
    if not os.path.exists(file_path):
        log.info(msg=f'Could not find "{file_path}" containing required packages.')
        return []
    
    packages: List[str] = []
    with open(file_path, "r") as file:
        for line in file:
            # Strip any leading/trailing whitespace characters (including newlines):
            line = line.strip()

            # Ignore empty lines and comments:
            if line and not line.startswith("#"):
                # Split by `==` or any other version specifier to get the package name:
                package_name = line.split("==")[0].split(">=")[0].split("<=")[0].split(">")[0].split("<")[0].split("~")[0].strip()
                packages.append(package_name)
    return packages


def list_incompatible_packages() -> List[str]:
    """
    List the package names that have been identified as incompatible with the current Python version.

    Parameters:
        None

    Return:
        List[str]: The list of package names that have been identified as incompatible with the current Python version.

    """
    incompatible_packages: List[str] = []
    for package_id in list_packages_from_requirements():
        if not is_pip_package_compatible(package_id=package_id):
            incompatible_packages.append(package_id)

    return incompatible_packages


def inspect_environment() -> None:
    """
    Inspect the environment to identify if the current Python environment, Jupyter Kernel version or packages listed in
    the project's "requirements.txt" file are identified as incompatible.

    Raises:
        StacklessException: Raised if any of the packages specified in the "requirements.txt" file have been identified
            as incompatible with the Python version of the current Jupyter Kernel.

    """
    log.debug(msg="Inspecting environment.")

    incompatible_packages = list_incompatible_packages()
    if incompatible_packages:
        incompatible_package_infos: List[str] = []
        for incompatible_package in incompatible_packages:
            log.debug(msg=f'Found incompatible package "{incompatible_package}".')
            incompatible_package_infos.append(f"   * {incompatible_package}: https://pypi.org/project/{incompatible_package}/")

        raise StacklessException(
            f"⚠ The environment could not be initialized for visualizing USD content. The following PIP packages are incompatible with the Kernel's Python version ({get_current_python_version()}):\n" \
                + "\n".join(incompatible_package_infos)
        )
