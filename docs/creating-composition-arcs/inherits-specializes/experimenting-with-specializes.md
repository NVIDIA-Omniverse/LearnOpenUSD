# Exercise: Experimenting With Specializes

Starting off with a simple example, we will be using a `cube.usd` and `cube_pyramid.usd` similar to our {term}`inherits <Inherit>` exercise. These files can be found in `composition_arcs/specializes/simple_example`.

One of the key differences is in `cube.usd`, `_cube_asset` contains an authored value for `diffuseColor` as `(1,0,0)`.

![](../../images/composition-arcs/image72.png)

Let’s open up our example file.

1. In the Visual Studio Code terminal, **run** the code below to open the file in usdview.

Windows:
```powershell
.\scripts\usdview.bat .\composition_arcs\specializes\simple_example\specializes_simple.usd
```
Linux:
```sh
./scripts/usdview.sh ./composition_arcs/specializes/simple_example/specializes_simple.usd
```

What are some things you notice about the scene? How does it differ from the simple example in the inherits exercise?

2. In the tree view, select **Shader** under `_cube_asset` and take notice of the `diffuseColor`.

![](../../images/composition-arcs/image29.png)

Only the top cube is magenta. Why is this? If you remember, our `cube.usd` is a red cube, where the {term}`specializes <Specialize>` arc contributes the red color. In `cube_pyramid.usd` we authored {term}`opinions <Opinions>` on the bottom two cubes to be blue and green. When we change the red fallback value to a magenta fallback, the other two are unaffected. The other two cubes have an authored opinion apart from the specializes arc on what color they want.

Again, if we were to open the `unaffected_scenario.usd`, we would see the same concept as inherits and the result would be the same. This is because the magenta color was only applied in the context of `specializes_simple.usd`.

![](../../images/composition-arcs/image8.png)

For this scenario, we’re creating a digital twin of the roadways. By default the max speed for each road piece is 30. However, side roads should have a max speed of 20. This needs to be applied to the whole city, so we can do this using a specializes arc.

3. In Visual Studio Code, **open** the following file: `composition_arcs/specializes/exercise/specializes_exercise_1.py`

We will be creating the {term}`class <Class>` in which our roads will specialize from. It will contain a maximum speed {term}`attribute <Attribute>` that is set to 30 by default.

4. **Add** the code below into the Part 1 code block.

```py
class_prim = asset_stage.CreateClassPrim("/_osm_street_data")
max_speed_attr = class_prim.CreateAttribute("osm:street:maxspeed", Sdf.ValueTypeNames.Int, custom=True)
max_speed_attr.Set(30)
```

Then, we’ll traverse to {term}`stage <Stage>` and add this specializes arc to each road mesh. If the road mesh we are looking at is in our listed `side_streets`, we will set its max speed to 20.

5. **Add** the code below into Part 2 block.

```py
for prim in asset_stage.Traverse():
    if prim.IsA(UsdGeom.Mesh) and prim.GetName().startswith("road_") and not "Barrier" in prim.GetName():
        prim.GetSpecializes().AddSpecialize(class_prim.GetPath())
    if prim.GetName() in side_streets:
        prim.GetAttribute("osm:street:maxspeed").Set(20)
```

6. **Run** the script by running the following code in the terminal:

Windows:
```powershell
python .\composition_arcs\specializes\exercise\specializes_exercise_1.py
```
Linux:
```sh
python ./composition_arcs/specializes/exercise/specializes_exercise_1.py
```

7. Now we can view the change in usdview. In the Visual Studio Code terminal, **run** the following code:

Windows:
```powershell
.\scripts\usdview.bat .\composition_arcs\specializes\exercise\main_street.usd
```
Linux:
```sh
./scripts/usdview.sh ./composition_arcs/specializes/exercise/main_street.usd
```

![](../../images/composition-arcs/image41.png)

If you select the road pieces and look at the *Property* panel, you’ll see in that our roads have a new attribute `osm:street:maxspeed` which is coming from the specializes arc. Our side roads also have been set to 20 while our main road is still 30.

Let’s imagine we’ve been told that in `composition_arcs/specializes/exercisescenario_02.usd` we should try setting a new default maximum speed limit of 40. Since we have already created our specializes arc, we just need to {term}`override <Over>` the maxspeed value on the source {term}`prim <Prim>` of the specializes arc to broadcast a fallback.

8. In Visual Studio Code, **open** the following file: `composition_arcs/specializes/exercise/specializes_exercise_2.py`

Similar to what we did previously, we are going to override the class prim, add our maxspeed attribute to it, and set the value to 40.

9. **Add** the code below to the Python file:

```py
class_prim = scenario2.OverridePrim("/_osm_street_data")
max_speed_attr = class_prim.CreateAttribute("osm:street:maxspeed", Sdf.ValueTypeNames.Int, custom=True)
max_speed_attr.Set(40)
```

10. **Save** the file.
11. In the terminal, **run** the following code to run the script

Windows:
```powershell
python .\composition_arcs\specializes\exercise\specializes_exercise_2.py
```
Linux:
```sh
python ./composition_arcs/specializes/exercise/specializes_exercise_2.py
```

12. In the terminal, **run** the following code to **open** the file in usdview.

Windows:
```powershell
.\scripts\usdview.bat .\composition_arcs\specializes\exercise\scenario_02.usd
```
Linux:
```sh
./scripts/usdview.sh ./composition_arcs/specializes/exercise/scenario_02.usd
```

![](../../images/composition-arcs/image17.png)

We can see here that our main roads all have maxspeed of 40 however, our side roads still have a maxspeed of 20 from when we authored it in `main_street.usd`. The side roads were previous refined or made more specialized so they can ignore this fallback broadcast from the specializes arc.

