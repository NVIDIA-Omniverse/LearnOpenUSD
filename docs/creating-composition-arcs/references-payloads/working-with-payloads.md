# Exercise: Working With Payloads

Let’s first look at how {term}`payloads <Payload>` work using simple geometry.

1. In the Visual Studio Code terminal, **run** the following code to open the file in usdview.

Windows:
```powershell
.\scripts\usdview.bat .\composition_arcs\payloads\simple_example\red_cube.usd
```
Linux:
```sh
./scripts/usdview.sh ./composition_arcs/payloads/simple_example/red_cube.usd
```

![](../../images/composition-arcs/image56.png)

Notice that this is the same cube we used in the [Working With References](./working-with-references.md) exercise.

2. **Close** out of usdview and head back to Visual Studio Code.
3. **Open** the following file to view the USDA format: `composition_arcs/payloads/simple_example/payloads_simple.usd`

It’ll look like this:

```usda
#usda 1.0
(
    defaultPrim = "World"
    endTimeCode = 100
    metersPerUnit = 0.01
    startTimeCode = 0
    timeCodesPerSecond = 24
    upAxis = "Y"
)

def Xform "World"
{
    def "red_cube_01" (
        prepend payload = @./red_cube.usd@
    )
    {
        float3 xformOp:rotateXYZ = (0, 0, 0)
        float3 xformOp:scale = (1, 1, 1)
        double3 xformOp:translate = (-75, 0, 0)
        uniform token[] xformOpOrder = ["xformOp:translate", "xformOp:rotateXYZ", "xformOp:scale"]
    }

    def "red_cube_02" (
        prepend payload = @./red_cube.usd@
    )
    {
        float3 xformOp:rotateXYZ = (0, 0, 0)
        float3 xformOp:scale = (1, 1, 1)
        double3 xformOp:translate = (75, 0, 0)
        uniform token[] xformOpOrder = ["xformOp:translate", "xformOp:rotateXYZ", "xformOp:scale"]
    }

    def "red_cube_03" (
        prepend payload = @./red_cube.usd@
    )
    {
        float3 xformOp:rotateXYZ = (0, 0, 0)
        float3 xformOp:scale = (1, 1, 1)
        double3 xformOp:translate = (0, 100, 0)
        uniform token[] xformOpOrder = ["xformOp:translate", "xformOp:rotateXYZ", "xformOp:scale"]
    }
}
```

What are some of the things you notice that are similar to {term}`references <Reference>`? Any differences? You should notice the `payload` keyword instead of the `references` keyword. We can also see that a payload is added similar to how a reference is added in USDA, where the only difference is the keyword.

4. Next, **run** the following code in Visual Studio Code to open the file in usdview:

Windows:
```powershell
.\scripts\usdview.bat .\composition_arcs\payloads\simple_example\payloads_simple.usd
```
Linux:
```sh
./scripts/usdview.sh ./composition_arcs/payloads/simple_example/payloads_simple.usd
```

![](../../images/composition-arcs/image36.png)

You might be asking yourself, how is this any different from using references? What’s the benefit?

Let’s start by showing one of the differences between payloads and references.

5. In usdview, right-click on `red_cube_01` in the tree view. We have the option to {term}`unload <Load and Unload>` the prim.

![](../../images/composition-arcs/image76.png)

6. Click on **Unload**.

![](../../images/composition-arcs/image89.gif)

We can see that the red cube has vanished from the scene. Take note that when selecting **Unload**, all the descendants from the payload are also not in the tree view. This is because payloads have the ability to load (compose) all of the scene description targeted by the payload or unload all their scene description, recomposing all prims beneath the payloaded prim, unloading them from the layer.

On the other hand, references are always composed and present on the {term}`stage <Stage>`. They cannot be unloaded.

7. We can also unload all payloads in the stage at once. In usdview, right-click on **`red_cube_01`** and select **Load** to load it back onto our stage.
8. Then, right-click on **Root** and click **Unload**. This will unload all payloads that are composed on the stage. To load it back, right-click on **Root** and select **Load**.

![](../../images/composition-arcs/image61.gif)

Now, imagine that our scene has become too large and it's hard to see everything when it’s fully loaded into the viewport. You can open the stage with all payloads unloaded and then load just what you need to work on the scene. This is where payloads come in handy.

9. **Open** `composition_arcs/payloads/exercise/payloads_exercise.py` in Visual Studio Code.

Similarly to how we added references to {term}`prims <Prim>`, we will use `GetPayloads()` and `AddPayload()` to add payloads to a prim.

10. **Add** the following code into the script:

```py
xform = UsdGeom.Xform.Define(stage, "/World/sm_bldgF_01")
xform.GetPrim().GetPayloads().AddPayload("./sm_bldgF.usd")
xform = UsdGeom.Xform.Define(stage, "/World/sm_bldgF_02")
xform.GetPrim().GetPayloads().AddPayload("./sm_bldgF.usd")
xform_api = UsdGeom.XformCommonAPI(xform)
xform_api.SetTranslate(Gf.Vec3d(180, 0, 0))
xform = UsdGeom.Xform.Define(stage, "/World/sm_bldgF_03")
xform.GetPrim().GetPayloads().AddPayload("./sm_bldgF.usd")
xform_api = UsdGeom.XformCommonAPI(xform)
xform_api.SetTranslate(Gf.Vec3d(340, 0, 0))
```

11. **Save** the file.

12. In the terminal, **run** the following code:

Windows:
```powershell
python .\composition_arcs\payloads\exercise\payloads_exercise.py
```
Linux:
```sh
python ./composition_arcs/payloads/exercise/payloads_exercise.py
```

13. Now let’s open **`city.usda`**. In the terminal, run the following code:

Windows:
```powershell
.\scripts\usdview.bat .\composition_arcs\payloads\exercise\city.usda
```
Linux:
```sh
./scripts/usdview.sh ./composition_arcs/payloads/exercise/city.usda
```

![](../../images/composition-arcs/image37.png)

As we can see, each building here is actually a payload. We can unload these via a script as well.

14. We can open a Python interpreter window inside of usdview. Go to **Window > Interpreter** to open a Python interpreter.

![](../../images/composition-arcs/image30.png)

15. **Add** the following code into the interpreter then press **enter**. This will unload all the payloads composed under the root. You can also find this code in `composition_arcs/payloads/exercise/usdview_exercise.py`

```py
stage = usdviewApi.stage
root = stage.GetPseudoRoot()
root.Unload()
```

![](../../images/composition-arcs/image33.gif)

16. Let’s say you want to only load one of the buildings back. **Add** the following code into the interpreter then press **enter** to run the code.

```py
bldg = stage.GetPrimAtPath("/World/sm_bldgF_01")
bldg.Load()
```

![](../../images/composition-arcs/image34.gif)

This means that we can unload all payloads in a stage before opening the **{term}`layer <Layer>`**. This can save on load time especially for large scenes.