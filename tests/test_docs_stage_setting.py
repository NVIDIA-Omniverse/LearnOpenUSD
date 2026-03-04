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

"""Tests for stage-setting doc notebooks (docs/stage-setting/).

Notebooks are built to docs/_build/jupyter_execute/; paths are relative to that directory.
Each class targets one notebook with a full-notebook test and one test per code cell with extensive asserts.
"""

from pxr import UsdShade

# Notebook paths and setup tags (run before dependent cells).
STAGE_NOTEBOOK = "stage-setting/stage.ipynb"

PRIMS_NOTEBOOK = "stage-setting/prims.ipynb"
PRIMS_SETUP = ["prims-setup"]

PATHS_NOTEBOOK = "stage-setting/prim-property-paths.ipynb"
PATHS_SETUP = ["paths-setup"]

TIMECODES_NOTEBOOK = "stage-setting/timecodes-timesamples.ipynb"
TIMECODES_SETUP = ["timecodes-setup"]

RELATIONSHIPS_NOTEBOOK = "stage-setting/properties/relationships.ipynb"
RELATIONSHIPS_SETUP = ["relationships-setup"]

ATTRIBUTES_NOTEBOOK = "stage-setting/properties/attributes.ipynb"
ATTRIBUTES_SETUP = ["attributes-setup"]


class TestStageNotebook:
    """Tests for stage-setting/stage.ipynb (no setup cells)."""

    def test_full_notebook(self, run_notebook):
        nb = run_notebook(STAGE_NOTEBOOK)
        assert nb.stage is not None
        assert (nb._work_dir / "_assets" / "root_layer_example.usda").exists()

    def test_cell_create_new(self, run_notebook):
        nb = run_notebook(STAGE_NOTEBOOK, tags=["stage-create-new"])
        assert nb.stage is not None
        assert "file_path" in nb
        assert nb.file_path == "_assets/first_stage.usda"
        out = nb._work_dir / "_assets" / "first_stage.usda"
        assert out.exists()
        assert "stage" in nb.stage.ExportToString()

    def test_cell_open_save(self, run_notebook):
        nb = run_notebook(
            STAGE_NOTEBOOK,
            tags=["stage-create-new", "stage-open-save"],
        )
        assert nb.stage is not None
        world = nb.stage.GetPrimAtPath("/World")
        assert world.IsValid()
        assert world.GetTypeName() == "Xform"
        assert (nb._work_dir / "_assets" / "first_stage.usda").exists()

    def test_cell_create_in_memory(self, run_notebook):
        nb = run_notebook(STAGE_NOTEBOOK, tags=["stage-create-in-memory"])
        assert nb.stage is not None
        world = nb.stage.GetPrimAtPath("/World")
        assert world.IsValid()
        assert (nb._work_dir / "_assets" / "in_memory_stage.usda").exists()

    def test_cell_root_layer(self, run_notebook):
        nb = run_notebook(STAGE_NOTEBOOK, tags=["stage-root-layer"])
        assert nb.stage is not None
        assert "root_layer" in nb
        assert "extra_layer" in nb
        assert nb.root_layer is not None
        assert nb.extra_layer is not None
        assert len(nb.root_layer.subLayerPaths) >= 1
        assert (nb._work_dir / "_assets" / "root_layer_example.usda").exists()
        assert (nb._work_dir / "_assets" / "extra_layer.usdc").exists()


class TestPrimsNotebook:
    """Tests for stage-setting/prims.ipynb."""

    def test_full_notebook(self, run_notebook):
        nb = run_notebook(PRIMS_NOTEBOOK)
        assert (nb._work_dir / "_assets" / "prim_hierarchy.usda").exists()

    def test_cell_define_prim(self, run_notebook):
        nb = run_notebook(PRIMS_NOTEBOOK, tags=PRIMS_SETUP + ["prims-define-prim"])
        assert nb.stage is not None
        hello = nb.stage.GetPrimAtPath("/hello")
        world = nb.stage.GetPrimAtPath("/world")
        assert hello.IsValid()
        assert world.IsValid()
        assert world.GetTypeName() == "Sphere"
        assert (nb._work_dir / "_assets" / "prims.usda").exists()

    def test_cell_sphere(self, run_notebook):
        nb = run_notebook(PRIMS_NOTEBOOK, tags=PRIMS_SETUP + ["prims-sphere"])
        assert nb.stage is not None
        assert "sphere" in nb
        assert nb.sphere.GetRadiusAttr().Get() == 2
        assert (nb._work_dir / "_assets" / "sphere_prim.usda").exists()

    def test_cell_hierarchy(self, run_notebook):
        nb = run_notebook(PRIMS_NOTEBOOK, tags=PRIMS_SETUP + ["prims-hierarchy"])
        assert nb.stage is not None
        geom = nb.stage.GetPrimAtPath("/Geometry")
        group = nb.stage.GetPrimAtPath("/Geometry/GroupTransform")
        box = nb.stage.GetPrimAtPath("/Geometry/GroupTransform/Box")
        assert geom.IsValid() and geom.GetTypeName() == "Scope"
        assert group.IsValid() and group.GetTypeName() == "Xform"
        assert box.IsValid() and box.GetTypeName() == "Cube"
        assert (nb._work_dir / "_assets" / "prim_hierarchy.usda").exists()

    def test_cell_getchild_box(self, run_notebook):
        nb = run_notebook(
            PRIMS_NOTEBOOK,
            tags=PRIMS_SETUP + ["prims-hierarchy", "prims-getchild-box"],
        )
        assert nb.stage is not None
        assert "prim" in nb
        assert nb.prim.GetPath() == "/Geometry"
        # GetChild("Box") returns invalid because Box is under GroupTransform, not Geometry
        child = nb.prim.GetChild("Box")
        assert not child or not child.IsValid()

    def test_cell_getchild_group_transform(self, run_notebook):
        nb = run_notebook(
            PRIMS_NOTEBOOK,
            tags=PRIMS_SETUP + ["prims-hierarchy", "prims-getchild-group-transform"],
        )
        assert nb.stage is not None
        assert "prim" in nb
        assert nb.prim.GetPath() == "/Geometry"
        child = nb.prim.GetChild("GroupTransform")
        assert child.IsValid()
        assert child.GetPath() == "/Geometry/GroupTransform"


class TestPrimPropertyPathsNotebook:
    """Tests for stage-setting/prim-property-paths.ipynb."""

    def test_full_notebook(self, run_notebook):
        nb = run_notebook(PATHS_NOTEBOOK)
        assert (nb._work_dir / "_assets" / "paths_property_authoring.usda").exists()

    def test_cell_get_validate_define(self, run_notebook):
        nb = run_notebook(PATHS_NOTEBOOK, tags=PATHS_SETUP + ["paths-get-validate-define"])
        assert nb.stage is not None
        assert nb.hello_prim.IsValid()
        assert nb.hello_world_prim.IsValid()
        assert not nb.world_prim.IsValid()
        assert (nb._work_dir / "_assets" / "paths.usda").exists()

    def test_cell_build_and_navigate(self, run_notebook):
        nb = run_notebook(PATHS_NOTEBOOK, tags=PATHS_SETUP + ["paths-build-and-navigate"])
        assert nb.stage is not None
        assert nb.stage.GetPrimAtPath("/World/Geometry/Sphere").IsValid()
        assert nb.stage.GetPrimAtPath("/World/Looks/Material").IsValid()
        assert (nb._work_dir / "_assets" / "paths_build_and_nav.usda").exists()

    def test_cell_property_authoring(self, run_notebook):
        nb = run_notebook(PATHS_NOTEBOOK, tags=PATHS_SETUP + ["paths-property-authoring"])
        assert nb.stage is not None
        sphere_prim = nb.stage.GetPrimAtPath("/World/Geom/Sphere")
        assert sphere_prim.IsValid()
        assert sphere_prim.GetAttribute("userProperties:tag").Get() == "surveyed"
        rel = sphere_prim.GetRelationship("my:ref")
        assert rel.IsValid()
        assert list(rel.GetTargets()) == [nb.stage.GetPrimAtPath("/World/Markers/MarkerA").GetPath()]
        assert (nb._work_dir / "_assets" / "paths_property_authoring.usda").exists()


class TestTimecodesTimesamplesNotebook:
    """Tests for stage-setting/timecodes-timesamples.ipynb."""

    def test_full_notebook(self, run_notebook):
        nb = run_notebook(TIMECODES_NOTEBOOK)
        assert (nb._work_dir / "_assets" / "timecode_ex2b.usda").exists()

    def test_cell_sample_stage(self, run_notebook):
        nb = run_notebook(TIMECODES_NOTEBOOK, tags=TIMECODES_SETUP + ["timecodes-sample-stage"])
        assert nb.stage is not None
        assert nb.stage.GetPrimAtPath("/World/Sphere").IsValid()
        assert nb.stage.GetPrimAtPath("/World/Backdrop").IsValid()
        assert (nb._work_dir / "_assets" / "timecode_sample.usda").exists()

    def test_cell_set_start_end(self, run_notebook):
        nb = run_notebook(
            TIMECODES_NOTEBOOK,
            tags=TIMECODES_SETUP + ["timecodes-sample-stage", "timecodes-set-start-end"],
        )
        assert nb.stage is not None
        assert nb.stage.GetStartTimeCode() == 1
        assert nb.stage.GetEndTimeCode() == 60
        assert (nb._work_dir / "_assets" / "timecode_ex1.usda").exists()

    def test_cell_translation_samples(self, run_notebook):
        nb = run_notebook(
            TIMECODES_NOTEBOOK,
            tags=TIMECODES_SETUP
            + [
                "timecodes-sample-stage",
                "timecodes-set-start-end",
                "timecodes-translation-time-samples",
            ],
        )
        assert nb.stage is not None
        assert (nb._work_dir / "_assets" / "timecode_ex2a.usda").exists()

    def test_cell_scale_samples(self, run_notebook):
        nb = run_notebook(
            TIMECODES_NOTEBOOK,
            tags=TIMECODES_SETUP
            + [
                "timecodes-sample-stage",
                "timecodes-set-start-end",
                "timecodes-translation-time-samples",
                "timecodes-scale-time-samples",
            ],
        )
        assert nb.stage is not None
        assert (nb._work_dir / "_assets" / "timecode_ex2b.usda").exists()


class TestRelationshipsNotebook:
    """Tests for stage-setting/properties/relationships.ipynb."""

    def test_full_notebook(self, run_notebook):
        nb = run_notebook(RELATIONSHIPS_NOTEBOOK)
        assert (nb._work_dir / "_assets" / "relationships_ex3.usda").exists()

    def test_cell_prim_collections(self, run_notebook):
        nb = run_notebook(
            RELATIONSHIPS_NOTEBOOK,
            tags=RELATIONSHIPS_SETUP + ["relationships-prim-collections"],
        )
        assert nb.stage is not None
        group = nb.stage.GetPrimAtPath("/World/Group")
        assert group.IsValid()
        members = group.GetRelationship("members")
        assert members.IsValid()
        targets = list(members.GetTargets())
        assert len(targets) == 2
        assert (nb._work_dir / "_assets" / "relationships_ex1.usda").exists()

    def test_cell_proxy_prim(self, run_notebook):
        nb = run_notebook(
            RELATIONSHIPS_NOTEBOOK,
            tags=RELATIONSHIPS_SETUP + ["relationships-proxy-prim"],
        )
        assert nb.stage is not None
        high = nb.stage.GetPrimAtPath("/World/HiRes")
        low = nb.stage.GetPrimAtPath("/World/Proxy")
        assert high.IsValid() and low.IsValid()
        proxy_rel = high.GetRelationship("proxyPrim")
        assert proxy_rel.IsValid()
        assert list(proxy_rel.GetTargets()) == [low.GetPath()]
        assert (nb._work_dir / "_assets" / "relationships_ex2.usda").exists()

    def test_cell_material_binding(self, run_notebook):
        nb = run_notebook(
            RELATIONSHIPS_NOTEBOOK,
            tags=RELATIONSHIPS_SETUP + ["relationships-material-binding"],
        )
        assert nb.stage is not None
        cube_1 = nb.stage.GetPrimAtPath("/World/Cube_1")
        assert cube_1.IsValid()
        binding_api = UsdShade.MaterialBindingAPI.Apply(cube_1)
        mat = binding_api.GetDirectBinding().GetMaterial()
        assert mat is not None
        assert "GreenMat" in str(mat.GetPath())
        assert (nb._work_dir / "_assets" / "relationships_ex3.usda").exists()


class TestAttributesNotebook:
    """Tests for stage-setting/properties/attributes.ipynb."""

    def test_full_notebook(self, run_notebook):
        nb = run_notebook(ATTRIBUTES_NOTEBOOK)
        assert (nb._work_dir / "_assets" / "attributes_ex3.usda").exists()

    def test_cell_retrieve_properties(self, run_notebook):
        nb = run_notebook(
            ATTRIBUTES_NOTEBOOK,
            tags=ATTRIBUTES_SETUP + ["attributes-retrieve-properties"],
        )
        assert nb.stage is not None
        assert "cube_prop_names" in nb
        assert len(nb.cube_prop_names) > 0
        assert (nb._work_dir / "_assets" / "attributes_ex1.usda").exists()

    def test_cell_get_values(self, run_notebook):
        nb = run_notebook(
            ATTRIBUTES_NOTEBOOK,
            tags=ATTRIBUTES_SETUP + ["attributes-get-values"],
        )
        assert nb.stage is not None
        assert nb.cube_size.IsValid() and nb.cube_extent.IsValid()
        assert nb.cube_size.Get() == 2.0  # Cube schema default size
        assert (nb._work_dir / "_assets" / "attributes_ex2.usda").exists()

    def test_cell_set_values(self, run_notebook):
        nb = run_notebook(
            ATTRIBUTES_NOTEBOOK,
            tags=ATTRIBUTES_SETUP + ["attributes-set-values"],
        )
        assert nb.stage is not None
        assert nb.cube_displaycolor.Get() == [(0.0, 1.0, 0.0)]
        assert (nb._work_dir / "_assets" / "attributes_ex3.usda").exists()
