# Exercise: Working With Relocates

Let's go through some of the {term}`relocates <Relocate>` we discussed with a hands-on exercise in usdview.

## Renaming a Referenced Prim

1. In the Visual Studio Code terminal, **run** the code below to open the file in usdview:

Windows:
```powershell
.\scripts\usdview.bat .\composition_arcs\relocates\simple_example\relocates_simple.usd
```
Linux:
```sh
./scripts/usdview.sh ./composition_arcs/relocates/simple_example/relocates_simple.usd
```

2. In the tree view, **expand** `World` and then `StreetLamp`.

Notice that the child {term}`prim <Prim>` is called `geometry`, with `pole` and `bulb` beneath it.

3. Now **open** `composition_arcs/relocates/simple_example/lamp_asset.usd` in Visual Studio Code.

The {term}`asset <Asset>` on disk has no prim called `geometry`. Its child is named `lamp_grp_v2_FINAL`. The name you saw in usdview is produced entirely by the relocate in `relocates_simple.usd`.

4. **Open** `composition_arcs/relocates/simple_example/relocates_simple.usd` in Visual Studio Code and look at the {term}`layer <Layer>` {term}`metadata <Metadata>` at the top:

```usda
relocates = {
    </World/StreetLamp/lamp_grp_v2_FINAL>: </World/StreetLamp/geometry>
}
```

That single entry is doing all the work. The referenced asset is untouched.

5. Back in usdview, **select** the `geometry` prim and open the *Composition* tab.

The composition {term}`index <Index>` shows the {term}`reference <Reference>` arc that brought the prim in, alongside the relocate that renamed it.

```{tip}
Try editing the target path in `relocates_simple.usd` to something else, such as `</World/StreetLamp/geo>`, save, and reload usdview with **File > Reload All Layers**. The prim's name in the tree view follows whatever you put on the right-hand side of the mapping.
```

## Reparenting a Referenced Prim

A relocate can also move a prim out of the subtree it arrived in.

6. In the terminal, **run** the code below to open the next file in usdview:

Windows:
```powershell
.\scripts\usdview.bat .\composition_arcs\relocates\reparent_example\relocates_reparent.usd
```
Linux:
```sh
./scripts/usdview.sh ./composition_arcs/relocates/reparent_example/relocates_reparent.usd
```

7. In the tree view, **expand** `World`.

`District_01` carries the reference to `block_asset.usd` and contains `office_tower` and `warehouse`. But `clock_tower` — which is authored inside that same asset — appears under `Landmarks` instead.

8. **Open** `composition_arcs/relocates/reparent_example/block_asset.usd` to confirm that `clock_tower` really is a sibling of the other two buildings in the source asset.

The relocate lifted it out of `District_01` and grafted it under `Landmarks`, without editing the asset:

```usda
relocates = {
    </World/District_01/clock_tower>: </World/Landmarks/clock_tower>
}
```

This is the pattern to reach for when an asset's internal organization doesn't match how your pipeline needs to group things downstream.

## Authoring Relocates From Python

Relocates are layer metadata, so you author them on the layer rather than on a prim. Let's clean up a vendor asset that ships mesh prims with awkward names and a leftover rig helper.

9. **Open** the following file in Visual Studio Code: `composition_arcs/relocates/exercise/relocates_exercise.py`

The script already references `signage_asset.usd` under `/World/Sign_01`. That asset contains `sign_MESH_01`, `post_MESH_01`, and `tmp_rig_helper`.

10. First, let's rename the two mesh prims to match our naming convention. **Add** the following code into the code block:

```py
stage.GetRootLayer().relocates = [
    (Sdf.Path("/World/Sign_01/sign_MESH_01"), Sdf.Path("/World/Sign_01/sign")),
    (Sdf.Path("/World/Sign_01/post_MESH_01"), Sdf.Path("/World/Sign_01/post")),
]
```

11. Next, let's drop the rig helper we don't need. Relocating a prim to an empty path removes it from the composed {term}`stage <Stage>`. **Add** a third entry to the list:

```py
    (Sdf.Path("/World/Sign_01/tmp_rig_helper"), Sdf.Path.emptyPath),
```

12. **Save** the file.

13. In the terminal, **run** the following code:

Windows:
```powershell
python .\composition_arcs\relocates\exercise\relocates_exercise.py
```
Linux:
```sh
python ./composition_arcs/relocates/exercise/relocates_exercise.py
```

14. In the terminal, **run** the following code to open the result in usdview:

Windows:
```powershell
.\scripts\usdview.bat .\composition_arcs\relocates\exercise\main_street_signage.usda
```
Linux:
```sh
./scripts/usdview.sh ./composition_arcs/relocates/exercise/main_street_signage.usda
```

15. **Expand** `World` and `Sign_01` in the tree view.

You should see `sign` and `post`, and no `tmp_rig_helper`.

16. **Open** `main_street_signage.usda` in Visual Studio Code to see how USD serialized what you authored:

```text
relocates = {
    </World/Sign_01/sign_MESH_01>: </World/Sign_01/sign>, 
    </World/Sign_01/post_MESH_01>: </World/Sign_01/post>, 
    </World/Sign_01/tmp_rig_helper>: <>
}
```

The empty path `<>` on the last line is the removal.

```{caution}
Relocates only apply to prims introduced by a {term}`composition arc <Composition Arcs>`. If you point a relocate's source at a prim defined directly in your own layer, USD does not report an error — the prim is quietly dropped and the target is never created. When a prim vanishes unexpectedly after you add a relocate, check that its source path really does come from a reference or payload.
```

A completed version of the script is available at `composition_arcs/relocates/exercise/relocates_exercise_full.py`.
