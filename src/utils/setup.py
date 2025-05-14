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

"""Perform validation and configuration of the Jupyter Notebook environment for the project."""

import logging
import logging.config

log = logging.getLogger(__name__)


CONTENT_DIRECTORY = "./content"
"""Relative path to the directory where the USD content is located."""


def get_content_directory() -> str:
    """
    Return the relative path to the directory where the USD content is located.

    Parameters:
        None

    Return:
        str: The relative path to the directory where the USD content is located.
    
    """
    return CONTENT_DIRECTORY


def get_content_output_directory() -> str:
    """
    Return the relative path to the directory where the glTF assets converted from the USD content are located.

    Parameters:
        None

    Return:
        str: The relative path to the directory where the glTF assets converted from the USD content are located.

    """
    return f"{CONTENT_DIRECTORY}/output"


def find_next_free_port(start_port: int = 1024, max_port: int = 65535) -> int:
    """
    Find the next free port in the given [start_port;max_port] interval.
    
    Parameters:
        start_port (int): Start port of the search interval.
        max_port (int): End port of the search interval.

    Return:
        int: The next free port identified in the given interval.

    Raises:
        IOError: Raised if no free ports could be found in the specified interval.

    """
    port = start_port

    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while port <= max_port:
        try:
            sock.bind(("", port))
            sock.close()
            return port
        except OSError:
            port += 1

    raise IOError(f"No free ports could be found in the [{start_port};{max_port}] range.")


def setup_log(log_level: int = logging.INFO) -> None:
    """
    Setup the logging characteristics to use for the project.

    Parameters:
        log_level (int): Log verbosity.

    Return:
        None

    """
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple-stream": {
                "format": "[%(levelname)s] %(message)s",
            },
            "standard": {
                "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            },
        },
        "handlers": {
            "console": {
                "level": logging.getLevelName(level=log_level),
                "formatter": "simple-stream",
                "class": "logging.StreamHandler",
            },
            "file": {
                # Create a file log, with severity always set to `DEBUG` in order to collect general logging information:
                "level": logging.getLevelName(level=logging.DEBUG),
                "formatter": "standard",
                "class": "logging.FileHandler",
                "filename": "./session-log.txt",
                "mode": "a",
            },
        },
        "root": {
            "handlers": ["file", "console"],
            # Send log entries of severity `DEBUG` and up to the `handlers` listed above, which can then further filter
            # the log entries based on the specific minimal verbosity they are sensitive to:
            "level": logging.getLevelName(level=logging.DEBUG),
        },
    }

    logging.config.dictConfig(config=logging_config)


def setup_notebook(
    perform_health_checks: bool = True,
    create_sample_assets: bool = False,
    content_directory: str = "./assets",
    log_level: int = logging.INFO,
) -> None:
    """
    Initialize the Jupyter Notebook, so all the required components can be shared between multiple Notebooks and
    authored within a single Python module.

    Parameters:
        perform_health_checks (bool): Flag indicating whether to perform health checks to validate whether environment
            requirements are met for the expected Jupyter Notebook experience.
        create_sample_assets (bool): Flag indicating whether to create sample assets when initializing the Notebook.
        log_level (int): Log verbosity level.

    Returns:
        None

    """
    # Initialize logging behavior for the project:
    setup_log(log_level=log_level)
    log.info(msg="Setting up Notebook.")

    # Record the provided `content_directory`:
    global CONTENT_DIRECTORY
    CONTENT_DIRECTORY = content_directory
    log.debug(msg=f'Setting content directory to "{get_content_directory()}".')
    log.debug(msg=f'Setting content output directory to "{get_content_output_directory()}".')

    # If desired, perform environment health checks against the list of required packages listed in the
    # "requirements.txt" file:
    if perform_health_checks:
        from .health_checks import inspect_environment
        inspect_environment()

    # If desired, create sample USD assets for the Notebook:
    if create_sample_assets:
        from .sample_assets import prepare_sample_assets

        # Create file structure where sample assets and converted USD content can reside:
        import os
        os.makedirs(name=get_content_directory(), exist_ok=True)
        os.makedirs(name=get_content_output_directory(), exist_ok=True)

        prepare_sample_assets()

    from .visualization import initialize_notebook
    initialize_notebook()
