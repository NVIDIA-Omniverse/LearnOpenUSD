# Exercise: Experimenting With Inherits

First, we will look at a simple example of {term}`inherits <Inherit>` using `cube.usd` and `cube_pyramid.usd`. Both can be found in `composition_arcs/inherits/simple_example`.

Our `cube.usd` is the same cube we have used in previous examples. The main difference is that there is a {term}`class <Class>` called `_cube_asset` which the "World" {term}`prim <Prim>` is inheriting from. There are no authored {term}`opinions <Opinions>` in `_cube_asset`.

![](../../images/composition-arcs/image90.png)

```{note}  
If you are trying to view the file in usdview and cannot see `_cube_asset` in the tree view, go to **Show > Abstract Prims**. This will show classes in the tree view.
```

![](../../images/composition-arcs/image101.png)

The next file, `cube_pyramid.usd` {term}`references <Reference>` `cube.usd` three times to create a pyramid. Each cube is also a different color. Let’s get started with the exercise.

![](../../images/composition-arcs/image49.png)

1. In the Visual Studio Code terminal, **run** the code below to open the file in usdview:

Windows:
```powershell
.\scripts\usdview.bat .\composition_arcs\inherits\simple_example\inherits_simple.usd
```
Linux:
```sh
./scripts/usdview.sh ./composition_arcs/inherits/simple_example/inherits_simple.usd
```

In this {term}`layer <Layer>` we are referencing `cube_pyramid.usd`, however each cube has the same color instead of different colors. Why is this?

![](../../images/composition-arcs/image95.png)

We can see that there is an opinion on `_cube_asset` that has an authored value on the `inputs:diffuseColor` to be `(1,1,0)`. This is being broadcasted to any prim that inherits `_cube_asset`. In this case, each one of our cubes in `cube_pyramid.usd` inherits from `_cube_asset`.

![](../../images/composition-arcs/image81.png)

How does this affect prims in `cube_pyramid.usd` or other scenarios referencing `cube_pyramid.usd`? Let's open another layer that also is referencing `cube_pyramid.usd`.

2. In the Visual Studio Code terminal, **run** the code below to open the file in usdview:

Windows:
```powershell
.\scripts\usdview.bat .\composition_arcs\inherits\simple_example\unaffected_scenario.usd
```
Linux:
```sh
./scripts/usdview.sh ./composition_arcs/inherits/simple_example/unaffected_scenario.usd
```

![](../../images/composition-arcs/image5.png)

As we can see, this one is unaffected. However, if we were to make all the cubes to be yellow in `cube_pyramid.usd` then both `unaffected_scenario.usd` and `inherits_simple.usd` would show yellow cubes. You might not want that and it may be a one-off, so that’s where you would want to leverage an inherits arc to limit your change to just the context where the inherited prim is overridden.

So why create an inherits arc? Let’s look at `composition_arcs/inherits/practical_example/night_scene_01.usd`, where the city scene is in a night environment. The director comes in and says, "I want all of the street lights to be yellow just for this scene. The other city night scenes should preserve the white lighting."

![](../../images/composition-arcs/image28.png)

We could directly modify the street lamp {term}`asset <Asset>` that is referenced, but since the director only wants to affect the context that we were looking at and not any others this isn’t the best option. A change to the referenced asset would ripple to every scene. The next obvious choice would be to just author {term}`overrides <Over>` for all the referenced lights in `night_scene_01.usd`. We could do it manually or scripted. This can be labor intensive, prone to error, and potentially adds a lot of extra authored data that doesn’t need to be there.

Instead, let's look at how the inherits arc can help in this scenario. If the street lamp asset has an inherits arc, we can author a new opinion on the inherits source prim in `night_scene_01.usd`. The opinion is then broadcast to all prims that inherit from the source prim, but just for that context. The other scenes will be unaffected. Let's use an inherits arc on the street lamp to change the color of the lights.

3. Open the following file in Visual Studio Code: `composition_arcs/inherits/exercise/inherits_exercise_1.py`

We need to create the class, `_street_lamp_dbl` in which our street lamps will inherit from. Then we'll have the default prim in our {term}`stage <Stage>` inherit from our newly created class.

4. **Add** the following code to the script:

```py
class_prim = asset_stage.CreateClassPrim("/_street_lamp_dbl")
root = asset_stage.GetDefaultPrim()
root.GetInherits().AddInherit(class_prim.GetPath())
```

5. **Save** the file.
6. In the Visual Studio Code terminal, **run** the following code:

Windows:
```powershell
python .\composition_arcs\inherits\exercise\inherits_exercise_1.py
```
Linux:
```sh
python ./composition_arcs/inherits/exercise/inherits_exercise_1.py
```

7. After running the script, return to the terminal and **run** the following code to open usdview:

Windows:
```powershell
.\scripts\usdview.bat .\composition_arcs\inherits\exercise\street_lamp_dbl.usd
```
Linux:
```sh
./scripts/usdview.sh ./composition_arcs/inherits/exercise/street_lamp_dbl.usd
```

![](../../images/composition-arcs/image48.png)

As we can see, we’ve created an abstract prim and set the street light's default prim to inherit it. The inherited abstract prim in this case is *not* encapsulated within the default prim and will be used as a global refinement. More on this later.

8. Now with the inherits arc established, we can use it to give the street lights a yellow tint. In Visual Studio Code open the following file: `composition_arcs/inherits/exercise/inherits_exercise_2.py`

The stage, `composition_arcs/inherits/exercise/scenario_02.usd`, will represent the scene that the director asked to change. `composition_arcs/inherits/exercise/scenario_01.usd` will represent a scene that we don't want to affect. In `scenario_02.usd`, we will override the same class from the street lamp asset and author our overrides inside the class which will then be broadcasted to all those inheriting from `_street_lamp_dbl`.

9. **Add** the following code to the Python file:

```py
class_prim = scenario2.OverridePrim("/_street_lamp_dbl")
light_prim = scenario2.OverridePrim(class_prim.GetPath().AppendPath("Lights/sphere_light_01"))
light = UsdLux.LightAPI(light_prim)
light.CreateColorAttr((0.5, 0.4, 0.1))
light_prim = scenario2.OverridePrim(class_prim.GetPath().AppendPath("Lights/sphere_light_02"))
light = UsdLux.LightAPI(light_prim)
light.CreateColorAttr((0.5, 0.4, 0.1))
shader_prim = scenario2.OverridePrim(class_prim.GetPath().AppendPath("Looks/light/light"))
shader = UsdShade.Shader(shader_prim)
shader.CreateInput("emissiveColor", Sdf.ValueTypeNames.Color3f).Set((0.5, 0.4, 0.1))
```

10. **Save** the file and **run** it by running the following code in the terminal:

Windows:
```powershell
python .\composition_arcs\inherits\exercise\inherits_exercise_2.py
```
Linux:
```sh
python ./composition_arcs/inherits/exercise/inherits_exercise_2.py
```

Now let’s see how it affected our `scenario_02.usd` stage.

11. In the terminal, **run** the following code to open the file in usdview.

Windows:
```powershell
.\scripts\usdview.bat .\composition_arcs\inherits\exercise\scenario_02.usd
```
Linux:
```sh
./scripts/usdview.sh ./composition_arcs/inherits/exercise/scenario_02.usd
```

![](../../images/composition-arcs/image83.png)

12. In the terminal, **run** the following code to open `scenario_01.usd` in usdview and verify that it was unaffected.

Windows:
```powershell
.\scripts\usdview.bat .\composition_arcs\inherits\exercise\scenario_01.usd
```
Linux:
```sh
./scripts/usdview.sh ./composition_arcs/inherits/exercise/scenario_02.usd
```
Now we can manipulate all of the lights in any stage with a simple override without affecting other stages.