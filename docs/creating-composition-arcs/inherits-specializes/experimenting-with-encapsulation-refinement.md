# Exercise: Experimenting With Encapsulation and Refinement

For this example, we’ll be using `cube.usd` that {term}`inherits <Inherit>` from a `_cube_asset` {term}`class <Class>` {term}`prim <Prim>`. The following files can be found in `composition_arcs/inherits/refinement_example`.

![](../../images/composition-arcs/image63.png)

We also have `cube_pyramid.usd` which has a `_local_cube` class prim. Each cube inherits from `_local_cube` on along with `_cube_asset`.

```{note}  
If you cannot see `_cube_asset` in usdview, select **Show > Abstract Class**, above the tree view.
```

Let’s open our example file.

1. In the Visual Studio Code terminal, **run** the code below to open the file in usdview:

Windows:
```powershell
.\scripts\usdview.bat .\composition_arcs\inherits\refinement_example\global_refinement.usd
```
Linux:
```sh
./scripts/usdview.sh ./composition_arcs/inherits/refinement_example/global_refinement.usd
```

**Global refinement** takes advantage of inherit arc targets where the target {term}`path <Path>` never changes. A path outside of encapsulation never gets re-pathed on {term}`reference <Reference>`. So for our example in `global_refinement.usd,` we override `/_cube_asset` and change the color to magenta, meaning all the cubes inheriting from `/_cube_asset` will all turn magenta.

![](../../images/composition-arcs/image46.png)

**Local refinement** is when the inherit arc targets an encapsulated prim. That means the target path gets repathed on reference. We can see this in `local_refinement.usd`.

2. In the Visual Studio Code terminal, **run** the code below to open the file in usdview:

Windows:
```powershell
.\scripts\usdview.bat .\composition_arcs\inherits\refinement_example\local_refinement.usd
```
Linux:
```sh
./scripts/usdview.sh ./composition_arcs/inherits/refinement_example/local_refinement.usd
```

If we modify the `/World/cube_pyramid_01/_local_cube` to have a cyan color, it will only affect cubes that inherit from `/World/cube_pyramid_01/_local_cube` that are contained in `cube_pyramid_01`. The other pyramids will remain unaffected.

![](../../images/composition-arcs/image26.png)
