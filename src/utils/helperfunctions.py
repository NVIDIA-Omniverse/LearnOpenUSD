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

"""OpenUSD Stage creation utilities."""

import logging
import os

log = logging.getLogger(__name__)


def create_new_stage(relative_file_path: str):
    """
    Return the OpenUSD Stage at the given location if one already exists, otherwise create a new USD Stage at the
    given location and return its instance.

    Parameters:
        relative_file_path (str): Location of the OpenUSD Stage to open or to create.

    Return:
        Usd.Stage: The instance of the OpenUSD Stage at the given location.

    """
    layer_identifier = os.path.join(os.getcwd(), relative_file_path)
    log.debug(msg=f'Creating new Stage at "{relative_file_path}" (absolute path: "{layer_identifier}").')

    # NOTE: Importing the `pxr` or other vendor modules, is done here rather than at the top-level as it is possible
    # that Users may not have installed it through PIP yet (e.g. when running Jupyter Notebooks for the first time,
    # before even running the `!pip install ...` command located in the first cell of Notebooks).
    from pxr import Usd, Sdf

    layer = Sdf.Layer.Find(identifier=layer_identifier)
    if layer:
        log.debug(msg=f'Layer already exists at "{layer_identifier}".')

        stage = Usd.Stage.Open(layer.identifier)
        return stage
        # del layer
        # del stage

    return Usd.Stage.CreateNew(relative_file_path)
