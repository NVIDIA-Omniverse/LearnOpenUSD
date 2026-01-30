# SPDX-FileCopyrightText: Copyright (c) 2025 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Collection of Python modules to enable visualization of USD content within Jupyter Notebooks."""

from .helperfunctions import *

# NOTE: The `.visualization` module is not imported here, as it may be referencing `pxr` or other vendor modules, which
# may not have been installed through PIP yet when performing environment checks for the Jupyter Notebook. This module 
# is instead intended to be imported directly through `from utils.visualization import DisplayUSD` in order for `pxr` 
# modules not to "leak" in the Python runtime.
#
# from .visualization import *
