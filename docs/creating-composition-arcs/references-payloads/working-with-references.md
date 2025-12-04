# Exercise: Working With References

Let’s see {term}`references <Reference>` in action now. We will be going over the reference we looked at in the lecture, but viewing it in usdview.

1. Head over to Visual Studio Code and **run** the following code to open the file in usdview:

Windows:
```powershell
.\scripts\usdview.bat .\composition_arcs\references\simple_example\red_cube.usd
```
Linux:
```sh
./scripts/usdview.sh ./composition_arcs/references/simple_example/red_cube.usd
```

![](../../images/composition-arcs/image56.png)

What are some of the things you notice? How is this {term}`layer <Layer>` organized? Keep these questions in mind as we will go over it again later on, when we talk about encapsulation.

As you might have noticed all {term}`prims <Prim>` are underneath and contained within the "World" prim.

2. **Close** the window and head back to Visual Studio Code.
3. **Open** `composition_arcs/references/simple_example/references_simple.usd` in Visual Studio Code, and notice where the references are being made.

![](../../images/composition-arcs/image62.png)

We can also see that there are {term}`property specs <Property Spec>` being applied to each.

![](../../images/composition-arcs/image44.png)

Looking at these property specs, how do these affect the layer? Does it also affect `red_cube.usd`?

4. Head back into Visual Studio Code and scroll down to view more of `references_simple.usd`. Take a look at `blue_cube_01` and when you scroll down further you can see that it is being used as a reference for `blue_cube_02` and `blue_cube_03`.

![](../../images/composition-arcs/image21.png)

![](../../images/composition-arcs/image22.png)

Knowing all this, what are some assumptions we can make about how this scene will look?

5. In the Visual Studio Code terminal, **run** the following code to open the file in usdview.

Windows:
```powershell
.\scripts\usdview.bat .\composition_arcs\references\simple_example\references_simple.usd
```
Linux:
```sh
./scripts/usdview.sh ./composition_arcs/references/simple_example/references_simple.usd
```

![](../../images/composition-arcs/image74.png)

We can also see where the references are being pulled from.

6. In the tree view, click on **`red_cube_01`** to select it, then click on the **Layer Stack** tab in the bottom right of usdview.

![](../../images/composition-arcs/image87.gif)

Here we can see in our layer stack that the `red_cube.usd` is part of it. So what does that mean? It means that we are targeting the data that is inside of `red_cube.usd` and composing it in our current layer.

7. Click on the **Composition** tab to the right of the *Layer Stack* tab to see the lists of the layers that compose the selected prim. Notice that the arc type is `reference`.

![](../../images/composition-arcs/image54.png)

We can also see the composition of `blue_cube_02` when selected.
![](../../images/composition-arcs/image66.png)

Going back to the questions we asked before and some new questions:

Looking at these property specs, how do these affect the layer?

Does it also affect `red_cube.usd`?

What if we did not have a default prim?

Now after having a basic understanding let’s apply it to a scenario.

The script we're creating could simulate an artist interactively building a city or it could be a tool that will procedurally generate a city. Let’s say we need to create a row of buildings. We can set this up using references.

Let’s take a look at what {term}`assets <Asset>` we are using. You can also open these files in usdview. Here we have `skyscraperA` and `skyscraperE`.\
![](../../images/composition-arcs/image39.png)

![](../../images/composition-arcs/image51.png)

8. Go to `composition_arcs/references/exercise/references_exercise.py`

9. **Add** the following code within the `PART ONE` section:

```py
skyscraper_01 = UsdGeom.Xform.Define(stage, "/World/skyscraperA_01")
skyscraper_01.GetPrim().GetReferences().AddReference(skyscraperA_relpath)
skyscraper_02 = UsdGeom.Xform.Define(stage, "/World/skyscraperA_02")
skyscraper_02.GetPrim().GetReferences().AddReference(skyscraperA_relpath)
skyscraper_02_xformapi = UsdGeom.XformCommonAPI(skyscraper_02)
skyscraper_02_xformapi.SetTranslate(Gf.Vec3d(180, 0, 0))
```
Here we are creating two destination prims and both will have a reference to `skyscraperA`.

10. **Save** the file.
11. Let’s run the script to see it in action. In the terminal, **run** the following code:

Windows:
```powershell
python .\composition_arcs\references\exercise\references_exercise.py
```
Linux:
```sh
python ./composition_arcs/references/exercise/references_exercise.py
```

This will create a new layer called `city.usda`.

12. Now let’s view it in usdview. In the Visual Studio Code terminal, **run** the following code:

Windows:
```powershell
.\scripts\usdview.bat .\composition_arcs\references\exercise\city.usda
```
Linux:
```sh
./scripts/usdview.sh ./composition_arcs/references/exercise/city.usda
```

![](../../images/composition-arcs/image4.png)

Here we can see the same skyscraper is now in our scene twice. You can see where the reference is coming from by expanding World and selecting `skyscraperA_01` or `skyscraperA_02`. In the *Meta Data* tab, note the "references" field.
![](../../images/composition-arcs/image27.png)

We can also see this in the new `city.usda` that we authored. If you were to open `city.usda` in Visual Studio Code, you’ll see the following:

```usda
#usda 1.0
(
    metersPerUnit = 0.01
    upAxis = "Y"
)

def Xform "World"
{
    def Xform "skyscraperA_01" (
        prepend references = @../../lib/assets/envir/city/skyscraperA/skyscraperA.usd@
    )
    {
    }

    def Xform "skyscraperA_02" (
        prepend references = @../../lib/assets/envir/city/skyscraperA/skyscraperA.usd@
    )
    {
        double3 xformOp:translate = (180, 0, 0)
    }
}
```

Let’s add one more skyscraper reference into the stage.

13. Using similar code, add the following snippets to the `PART TWO` section of `references_exercise.py`

```py
skyscraper_03 = UsdGeom.Xform.Define(stage, "/World/skyscraperE_01")
skyscraper_03.GetPrim().GetReferences().AddReference(skyscraperE_relpath)
skyscraper_03_xformapi = UsdGeom.XformCommonAPI(skyscraper_03)
skyscraper_03_xformapi.SetTranslate(Gf.Vec3d(340, 0, 0))
```

In this case we are using `skyscraperE` instead of `skyscraperA`.

14. **Save** the file.

15. In the Visual Studio Code terminal, **run** the following code:

Windows:
```powershell
python .\composition_arcs\references\exercise\references_exercise.py
```
Linux:
```sh
python ./composition_arcs/references/exercise/references_exercise.py
```

16. Now let’s view it in usdview. In the Visual Studio Code terminal, **run** the following code:

Windows:
```powershell
.\scripts\usdview.bat .\composition_arcs\references\exercise\city.usda
```
Linux:
```sh
./scripts/usdview.sh ./composition_arcs/references/exercise/city.usda
```

![](../../images/composition-arcs/image60.png)

As we can see we now have a small city block. Our colleagues are able to still continue to work in their respective skyscraper assets while we continue to build out our city.