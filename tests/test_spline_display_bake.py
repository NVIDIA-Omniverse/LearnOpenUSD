# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
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

"""Tests for spline-to-time-sample baking used by DisplayUSD previews."""

import os
import tempfile

import pytest
from pxr import Ts, Usd, UsdGeom

from lousd.utils.visualization import BakeSplineAttributesToTimeSamples, DisplayBakeUSDPath


@pytest.fixture()
def spline_usd_path():
    tmp = tempfile.mkdtemp()
    path = os.path.join(tmp, "rot_spline.usda")
    stage = Usd.Stage.CreateNew(path)
    UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
    stage.SetTimeCodesPerSecond(24)
    stage.SetStartTimeCode(0)
    stage.SetEndTimeCode(10)

    xf = UsdGeom.Xform.Define(stage, "/X")
    UsdGeom.Cube.Define(stage, "/X/Cube")
    op = xf.AddRotateZOp(opSuffix="spin")
    attr = op.GetAttr()
    tn = str(attr.GetTypeName())
    spline = Ts.Spline(tn)
    spline.SetKnot(Ts.Knot(typeName=tn, time=0, value=0, nextInterp=Ts.InterpLinear))
    spline.SetKnot(Ts.Knot(typeName=tn, time=10, value=45, nextInterp=Ts.InterpLinear))
    attr.SetSpline(spline)
    stage.Save()
    yield path


def test_display_bake_usd_path_suffix():
    assert DisplayBakeUSDPath("_assets/foo.usda").endswith("_display_bake.usda")


def test_bake_replaces_spline_with_time_samples(spline_usd_path: str):
    tmp = os.path.dirname(spline_usd_path)
    out = os.path.join(tmp, "out.usda")
    BakeSplineAttributesToTimeSamples(spline_usd_path, out)

    baked = Usd.Stage.Open(out)
    attr = baked.GetPrimAtPath("/X").GetAttribute("xformOp:rotateZ:spin")
    assert attr.IsValid()
    assert not attr.HasSpline()
    assert attr.GetNumTimeSamples() == 11
    xformable = UsdGeom.Xformable(baked.GetPrimAtPath("/X"))
    assert len(xformable.GetTimeSamples()) >= 1


def test_bake_without_time_code_range_preserves_spline(tmp_path):
    src = str(tmp_path / "no_range.usda")
    stage = Usd.Stage.CreateNew(src)
    xf = UsdGeom.Xform.Define(stage, "/X")
    attr = xf.AddRotateZOp(opSuffix="spin").GetAttr()
    tn = str(attr.GetTypeName())
    spline = Ts.Spline(tn)
    spline.SetKnot(Ts.Knot(typeName=tn, time=0, value=0, nextInterp=Ts.InterpLinear))
    spline.SetKnot(Ts.Knot(typeName=tn, time=10, value=45, nextInterp=Ts.InterpLinear))
    attr.SetSpline(spline)
    stage.Save()

    out = str(tmp_path / "no_range_out.usda")
    BakeSplineAttributesToTimeSamples(src, out)

    baked = Usd.Stage.Open(out)
    baked_attr = baked.GetPrimAtPath("/X").GetAttribute("xformOp:rotateZ:spin")
    assert baked_attr.HasSpline()
    assert baked_attr.GetNumTimeSamples() == 0


def test_bake_value_spline_usd_path_not_modified(spline_usd_path: str):
    before = open(spline_usd_path, encoding="utf-8").read()
    out = os.path.join(os.path.dirname(spline_usd_path), "out.usda")
    BakeSplineAttributesToTimeSamples(spline_usd_path, out)
    after = open(spline_usd_path, encoding="utf-8").read()
    assert before == after
