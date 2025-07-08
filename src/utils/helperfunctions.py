# SPDX-FileCopyrightText: Copyright (c) 2025 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

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
