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

"""Tests for beyond-basics doc notebooks (docs/beyond-basics/).

Notebooks are built to docs/_build/jupyter_execute/; paths are relative to that directory.
Each class has a full-notebook test and one test per code cell with extensive asserts.
"""

from pxr import Kind, Usd, UsdGeom
import pytest


VALUE_RESOLUTION_NOTEBOOK = "beyond-basics/value-resolution.ipynb"
VALUE_RESOLUTION_SETUP = ["value-resolution-setup"]

UNITS_NOTEBOOK = "beyond-basics/units.ipynb"
UNITS_SETUP = ["units-setup"]

STAGE_TRAVERSAL_NOTEBOOK = "beyond-basics/stage-traversal.ipynb"
STAGE_TRAVERSAL_SETUP = ["stage-traversal-setup"]

PRIMVARS_NOTEBOOK = "beyond-basics/primvars.ipynb"
PRIMVARS_SETUP = ["primvars-setup"]

MODEL_KINDS_NOTEBOOK = "beyond-basics/model-kinds.ipynb"
MODEL_KINDS_SETUP = ["model-kinds-setup"]

CUSTOM_PROPERTIES_NOTEBOOK = "beyond-basics/custom-properties.ipynb"
CUSTOM_PROPERTIES_SETUP = ["custom-properties-setup"]

ACTIVE_INACTIVE_NOTEBOOK = "beyond-basics/active-inactive-prims.ipynb"
ACTIVE_INACTIVE_SETUP = ["active-inactive-setup"]

SPLINE_ANIMATION_NOTEBOOK = "beyond-basics/spline-animation.ipynb"
SPLINE_ANIMATION_SETUP = ["spline-animation-setup"]

ASSET_INFO_NOTEBOOK = "beyond-basics/asset-info.ipynb"
ASSET_INFO_SETUP = ["asset-info-setup"]

EDIT_TARGETS_NOTEBOOK = "beyond-basics/edit-targets-layer-muting.ipynb"
EDIT_TARGETS_SETUP = ["edit-targets-setup"]


class TestValueResolutionNotebook:
    """Tests for beyond-basics/value-resolution.ipynb."""

    def test_full_notebook(self, run_notebook):
        nb = run_notebook(VALUE_RESOLUTION_NOTEBOOK)
        assert (nb._work_dir / "_assets" / "value_resolution_composed_explicit.usda").exists()

    def test_cell_attribute_animation(self, run_notebook):
        nb = run_notebook(
            VALUE_RESOLUTION_NOTEBOOK,
            tags=VALUE_RESOLUTION_SETUP + ["value-resolution-attribute-animation"],
        )
        assert nb.stage is not None
        assert nb.stage.GetStartTimeCode() == 1
        assert nb.stage.GetEndTimeCode() == 120
        world = nb.stage.GetPrimAtPath("/World")
        ground = nb.stage.GetPrimAtPath("/World/Ground")
        anim_cube = nb.stage.GetPrimAtPath("/World/AnimCube")
        assert world.IsValid() and ground.IsValid() and anim_cube.IsValid()
        assert nb.stage.GetDefaultPrim().GetPath() == "/World"
        assert (nb._work_dir / "_assets" / "value_resolution_attr.usda").exists()

    def test_cell_customdata_relationship(self, run_notebook):
        nb = run_notebook(
            VALUE_RESOLUTION_NOTEBOOK,
            tags=VALUE_RESOLUTION_SETUP + ["value-resolution-customdata-relationship"],
        )
        assert nb.composed_stage is not None
        assert nb.xform_prim.IsValid()
        assert nb.xform_prim.GetPath() == "/World/XformPrim"
        assert "source" in nb.xform_prim.GetCustomData()
        assert len(list(nb.xform_prim.GetRelationship("look:targets").GetTargets())) == 2
        assert (nb._work_dir / "_assets" / "value_resolution_composed_explicit.usda").exists()


class TestUnitsNotebook:
    """Tests for beyond-basics/units.ipynb."""

    def test_full_notebook(self, run_notebook):
        nb = run_notebook(UNITS_NOTEBOOK)
        assert (nb._work_dir / "_assets" / "units_timecode_scene.usda").exists()

    def test_cell_meters_per_unit(self, run_notebook):
        nb = run_notebook(
            UNITS_NOTEBOOK,
            tags=UNITS_SETUP + ["units-meters-per-unit"],
        )
        assert "scene_stage" in nb
        assert nb.scene_stage is not None
        assert UsdGeom.GetStageMetersPerUnit(nb.scene_stage) == 0.001
        assert nb.scene_stage.GetPrimAtPath("/World").IsValid()
        assert (nb._work_dir / "_assets" / "units_mismatch_scene.usda").exists()

    def test_cell_timecodes_per_second(self, run_notebook):
        nb = run_notebook(
            UNITS_NOTEBOOK,
            tags=UNITS_SETUP + ["units-timecodes-per-second"],
        )
        assert "scene_stage" in nb
        assert nb.scene_stage is not None
        assert nb.scene_stage.GetTimeCodesPerSecond() == 24
        assert (nb._work_dir / "_assets" / "units_timecode_scene.usda").exists()


class TestStageTraversalNotebook:
    """Tests for beyond-basics/stage-traversal.ipynb."""

    def test_full_notebook(self, run_notebook):
        nb = run_notebook(STAGE_TRAVERSAL_NOTEBOOK)
        assert (nb._work_dir / "_assets" / "stage_traversal.usda").exists()

    def test_cell_traverse(self, run_notebook):
        nb = run_notebook(
            STAGE_TRAVERSAL_NOTEBOOK,
            tags=STAGE_TRAVERSAL_SETUP + ["stage-traversal-traverse"],
        )
        assert nb.stage is not None
        paths = [p.GetPath() for p in nb.stage.Traverse()]
        assert len(paths) >= 1
        assert any(p == "/World" for p in paths)

    def test_cell_filter_types(self, run_notebook):
        nb = run_notebook(
            STAGE_TRAVERSAL_NOTEBOOK,
            tags=STAGE_TRAVERSAL_SETUP + ["stage-traversal-filter-types"],
        )
        assert nb.stage is not None
        assert "scope_count" in nb
        assert "xform_count" in nb
        assert nb.scope_count >= 0 and nb.xform_count >= 0

    def test_cell_children(self, run_notebook):
        nb = run_notebook(
            STAGE_TRAVERSAL_NOTEBOOK,
            tags=STAGE_TRAVERSAL_SETUP + ["stage-traversal-children"],
        )
        assert nb.stage is not None
        default_prim = nb.stage.GetDefaultPrim()
        assert default_prim.IsValid()
        assert default_prim.GetPath() == "/World"
        children = list(default_prim.GetAllChildren())
        assert len(children) >= 1

    def test_cell_prim_range(self, run_notebook):
        nb = run_notebook(
            STAGE_TRAVERSAL_NOTEBOOK,
            tags=STAGE_TRAVERSAL_SETUP + ["stage-traversal-prim-range"],
        )
        assert nb.stage is not None
        assert "prim_range" in nb
        box = nb.stage.GetPrimAtPath("/World/Box")
        assert box.IsValid()


class TestPrimvarsNotebook:
    """Tests for beyond-basics/primvars.ipynb."""

    def test_full_notebook(self, run_notebook):
        nb = run_notebook(PRIMVARS_NOTEBOOK)
        assert (nb._work_dir / "_assets" / "primvars_mesh_deformation.usda").exists()

    def test_cell_displaycolor_interpolation(self, run_notebook):
        nb = run_notebook(
            PRIMVARS_NOTEBOOK,
            tags=PRIMVARS_SETUP + ["primvars-displaycolor-interpolation"],
        )
        assert nb.stage is not None
        per_prim = nb.stage.GetPrimAtPath("/World/PerPrim")
        per_face = nb.stage.GetPrimAtPath("/World/PerFace")
        per_vertex = nb.stage.GetPrimAtPath("/World/PerVertex")
        assert per_prim.IsValid() and per_face.IsValid() and per_vertex.IsValid()
        assert (nb._work_dir / "_assets" / "primvars_displaycolor.usda").exists()

    def test_cell_mesh_deformation(self, run_notebook):
        nb = run_notebook(
            PRIMVARS_NOTEBOOK,
            tags=PRIMVARS_SETUP + ["primvars-mesh-deformation"],
        )
        assert nb.stage is not None
        mesh = nb.stage.GetPrimAtPath("/World/Plane")
        assert mesh.IsValid()
        assert mesh.GetTypeName() == "Mesh"
        assert len(nb.plane_privar_api.GetPrimvar("deformation").Get()) == 4
        assert (nb._work_dir / "_assets" / "primvars_mesh_deformation.usda").exists()


class TestModelKindsNotebook:
    """Tests for beyond-basics/model-kinds.ipynb."""

    def test_full_notebook(self, run_notebook):
        nb = run_notebook(MODEL_KINDS_NOTEBOOK)
        assert (nb._work_dir / "_assets" / "model_kinds_component.usda").exists()

    def test_cell_component_traversal(self, run_notebook):
        nb = run_notebook(
            MODEL_KINDS_NOTEBOOK,
            tags=MODEL_KINDS_SETUP + ["model-kinds-component-traversal"],
        )
        assert nb.stage is not None
        world = nb.stage.GetPrimAtPath("/World")
        component = nb.stage.GetPrimAtPath("/World/Component")
        markers = nb.stage.GetPrimAtPath("/World/Markers")
        assert world.IsValid() and component.IsValid() and markers.IsValid()
        assert Usd.ModelAPI(world).GetKind() == Kind.Tokens.group
        assert Usd.ModelAPI(component).GetKind() == Kind.Tokens.component
        assert (nb._work_dir / "_assets" / "model_kinds_component.usda").exists()


class TestCustomPropertiesNotebook:
    """Tests for beyond-basics/custom-properties.ipynb."""

    def test_full_notebook(self, run_notebook):
        nb = run_notebook(CUSTOM_PROPERTIES_NOTEBOOK, needs_content=True)
        assert (nb._work_dir / "_assets" / "sensor_data.usda").exists()

    def test_cell_create_attributes(self, run_notebook):
        nb = run_notebook(
            CUSTOM_PROPERTIES_NOTEBOOK,
            tags=CUSTOM_PROPERTIES_SETUP + ["custom-properties-setup-asset", "custom-properties-create-attributes"],
            needs_content=True,
        )
        assert nb.stage is not None
        box = nb.stage.GetPrimAtPath("/World/Packages/Box")
        assert box.IsValid()
        weight = box.GetAttribute("acme:weight")
        category = box.GetAttribute("acme:category")
        assert weight.IsValid() and weight.Get() == 5.5
        assert category.IsValid() and category.Get() == "Cosmetics"
        assert (nb._work_dir / "_assets" / "custom_attributes.usda").exists()

    def test_cell_modify_attributes(self, run_notebook):
        nb = run_notebook(
            CUSTOM_PROPERTIES_NOTEBOOK,
            tags=CUSTOM_PROPERTIES_SETUP
            + ["custom-properties-setup-asset", "custom-properties-create-attributes", "custom-properties-modify-attributes"],
            needs_content=True,
        )
        assert nb.stage is not None
        box = nb.stage.GetPrimAtPath("/World/Packages/Box")
        weight = box.GetAttribute("acme:weight")
        assert weight.IsValid()
        assert weight.Get() == 4.25

    def test_cell_namespaces(self, run_notebook):
        nb = run_notebook(
            CUSTOM_PROPERTIES_NOTEBOOK,
            tags=CUSTOM_PROPERTIES_SETUP + ["custom-properties-namespaces"],
        )
        assert nb.stage is not None
        sensor = nb.stage.GetPrimAtPath("/EnvironmentSensor")
        assert sensor.IsValid()
        temp = sensor.GetAttribute("acme:sensor:temperature")
        assert temp.IsValid()
        assert (nb._work_dir / "_assets" / "sensor_data.usda").exists()


class TestActiveInactivePrimsNotebook:
    """Tests for beyond-basics/active-inactive-prims.ipynb."""

    def test_full_notebook(self, run_notebook):
        nb = run_notebook(ACTIVE_INACTIVE_NOTEBOOK)
        assert (nb._work_dir / "_assets" / "active-inactive.usda").exists()

    def test_cell_deactivate(self, run_notebook):
        nb = run_notebook(
            ACTIVE_INACTIVE_NOTEBOOK,
            tags=ACTIVE_INACTIVE_SETUP + ["active-inactive-content-setup", "active-inactive-deactivate"],
        )
        assert nb.stage is not None
        box = nb.stage.GetPrimAtPath("/World/Box")
        assert box.IsValid()
        assert not box.IsActive()
        # Traverse should not include /World/Box and its descendants
        traversed_paths = [p.GetPath() for p in nb.stage.Traverse()]
        assert "/World/Box" not in traversed_paths


class TestSplineAnimationNotebook:
    """Tests for beyond-basics/spline-animation.ipynb."""

    def test_full_notebook(self, run_notebook):
        nb = run_notebook(SPLINE_ANIMATION_NOTEBOOK)
        assert (nb._work_dir / "_assets" / "spline_layer_offset_scene.usda").exists()

    def test_cell_inner_loop(self, run_notebook):
        nb = run_notebook(
            SPLINE_ANIMATION_NOTEBOOK,
            tags=SPLINE_ANIMATION_SETUP + ["spline-animation-inner-loop"],
        )
        assert nb.stage is not None
        yaw = nb.stage.GetPrimAtPath("/World/RotatingCube").GetAttribute("xformOp:rotateZ:yaw")
        assert yaw.IsValid() and yaw.HasSpline()
        assert (nb._work_dir / "_assets" / "spline_inner_loop.usda").exists()

    def test_cell_extrapolation(self, run_notebook):
        nb = run_notebook(
            SPLINE_ANIMATION_NOTEBOOK,
            tags=SPLINE_ANIMATION_SETUP + ["spline-animation-extrapolation"],
        )
        assert nb.stage is not None
        rock = nb.stage.GetPrimAtPath("/World/RockingCube").GetAttribute("xformOp:rotateY:rock")
        assert rock.IsValid() and rock.HasSpline()
        assert (nb._work_dir / "_assets" / "spline_extrapolation.usda").exists()

    def test_cell_layer_offset(self, run_notebook):
        nb = run_notebook(
            SPLINE_ANIMATION_NOTEBOOK,
            tags=SPLINE_ANIMATION_SETUP + ["spline-animation-layer-offset"],
        )
        assert nb.rig_stage is not None
        assert nb.scene is not None
        assert nb.early.IsValid() and nb.late.IsValid()
        assert (nb._work_dir / "_assets" / "spline_slide_rig.usda").exists()
        assert (nb._work_dir / "_assets" / "spline_layer_offset_scene.usda").exists()


class TestAssetInfoNotebook:
    """Tests for beyond-basics/asset-info.ipynb."""

    def test_full_notebook(self, run_notebook):
        nb = run_notebook(ASSET_INFO_NOTEBOOK)
        assert (nb._work_dir / "_assets" / "chair_a.usda").exists()
        assert (nb._work_dir / "_assets" / "asset_info_scene.usda").exists()

    def test_cell_author(self, run_notebook):
        nb = run_notebook(
            ASSET_INFO_NOTEBOOK,
            tags=ASSET_INFO_SETUP + ["asset-info-author"],
        )
        assert nb.stage is not None
        prim = nb.stage.GetPrimAtPath("/chair_a")
        assert prim.IsValid()
        assert nb.stage.GetDefaultPrim().GetPath() == "/chair_a"

        model = Usd.ModelAPI(prim)
        assert model.GetAssetName() == "chair_a"
        assert model.GetAssetVersion() == "v003"
        assert model.GetAssetIdentifier().path == "asset://chairs/chair_a.usd"

        # Custom keys live in the same dictionary as the conventional ones
        info = prim.GetAssetInfo()
        assert info["department"] == "set_dress"
        assert set(info) == {"identifier", "name", "version", "department"}
        assert prim.HasAuthoredAssetInfo()
        assert (nb._work_dir / "_assets" / "chair_a.usda").exists()

    def test_cell_through_reference(self, run_notebook):
        nb = run_notebook(
            ASSET_INFO_NOTEBOOK,
            tags=ASSET_INFO_SETUP + ["asset-info-author", "asset-info-through-reference"],
        )
        chair_1 = nb.chair_1
        assert chair_1.IsValid()

        # Asset info composes through the reference without being authored locally
        info = chair_1.GetAssetInfo()
        assert info["name"] == "chair_a"
        assert info["version"] == "v003"
        assert info["department"] == "set_dress"
        assert chair_1.HasAuthoredAssetInfo()

    def test_cell_per_key_override(self, run_notebook):
        nb = run_notebook(
            ASSET_INFO_NOTEBOOK,
            tags=ASSET_INFO_SETUP
            + ["asset-info-author", "asset-info-through-reference", "asset-info-per-key-override"],
        )
        composed = nb.composed

        # Overriding one key must not drop the others
        assert composed["version"] == "v004"
        assert composed["name"] == "chair_a"
        assert composed["department"] == "set_dress"
        assert composed["identifier"].path == "asset://chairs/chair_a.usd"

        # Only the overridden key is authored in the referencing layer
        scene_spec = nb.scene.GetRootLayer().GetPrimAtPath("/World/Chair_1")
        assert scene_spec.GetInfo("assetInfo") == {"version": "v004"}


class TestEditTargetsLayerMutingNotebook:
    """Tests for beyond-basics/edit-targets-layer-muting.ipynb."""

    def test_full_notebook(self, run_notebook):
        nb = run_notebook(EDIT_TARGETS_NOTEBOOK)
        for name in ("root.usda", "shot.usda", "base.usda"):
            assert (nb._work_dir / "_assets" / name).exists()

    def test_cell_author_routes_edits_by_target(self, run_notebook):
        nb = run_notebook(
            EDIT_TARGETS_NOTEBOOK,
            tags=EDIT_TARGETS_SETUP + ["edit-targets-author"],
        )
        # Each opinion landed in the layer it was targeted at
        assert nb.base.GetAttributeAtPath("/World/Ball.radius").default == 1.0
        assert nb.shot.GetAttributeAtPath("/World/Ball.radius").default == 5.0
        # ...and nothing leaked into the root layer, which only holds the sublayer list
        assert nb.root.GetPrimAtPath("/World") is None
        assert list(nb.root.subLayerPaths) == ["./shot.usda", "./base.usda"]
        # The stronger sublayer wins composition
        assert nb.ball.GetRadiusAttr().Get() == 5.0
        # EditContext restored the original target on exit
        assert nb.stage.GetEditTarget().GetLayer() == nb.root

    def test_cell_muting_falls_back_without_editing(self, run_notebook):
        nb = run_notebook(
            EDIT_TARGETS_NOTEBOOK,
            tags=EDIT_TARGETS_SETUP + ["edit-targets-author", "edit-targets-muting"],
        )
        # The cell unmutes at the end, so the composed value is back to the shot opinion
        assert nb.ball.GetRadiusAttr().Get() == 5.0
        # Muting never touched the layer's data or the scene description
        assert nb.shot.GetAttributeAtPath("/World/Ball.radius").default == 5.0
        assert "mute" not in nb.root.ExportToString().lower()

        # Guard the identifier match itself. MuteLayer fails silently when the
        # identifier does not match the one the stage resolved, so assert that
        # muting actually changes composition rather than trusting the call.
        nb.stage.MuteLayer(nb.shot.identifier)
        assert nb.stage.IsLayerMuted(nb.shot.identifier)
        assert nb.ball.GetRadiusAttr().Get() == 1.0
        nb.stage.UnmuteLayer(nb.shot.identifier)
        assert nb.ball.GetRadiusAttr().Get() == 5.0

    def test_cell_muting_is_per_stage(self, run_notebook):
        nb = run_notebook(
            EDIT_TARGETS_NOTEBOOK,
            tags=EDIT_TARGETS_SETUP
            + ["edit-targets-author", "edit-targets-muting", "edit-targets-per-stage"],
        )
        # Two stages on identical scene description disagree, because muting is stage state
        assert nb.stage_b.IsLayerMuted(nb.shot.identifier) is False
        assert UsdGeom.Sphere.Get(nb.stage_b, "/World/Ball").GetRadiusAttr().Get() == 5.0
