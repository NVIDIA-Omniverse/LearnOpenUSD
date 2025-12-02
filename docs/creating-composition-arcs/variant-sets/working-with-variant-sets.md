# Exercise: Working With Variant Sets
Let’s go through some of the {term}`variant sets <Variant Set>` discussed with a hands‑on exercise in usdview.

1. In the Visual Studio Code terminal, **run** the code below to open the file in usdview:

Windows:
```powershell
.\scripts\usdview.bat .\composition_arcs\variant_sets\simple_example\variant_sets_simple.usd
```
Linux:
```sh
./scripts/usdview.sh ./composition_arcs/variant_sets/simple_example/variant_sets_simple.usd
```

2. **Select** the *Meta Data* tab.
3. In the tree view, **select** "World".

![](../../images/composition-arcs/image99.png)

4. From the *Meta Data* tab, locate the **color variant** field. It will have a drop down where we can select between the different variants. Change the variant to **blue**.

![](../../images/composition-arcs/image24.gif)

If you cannot see the blue color, click in an empty space in the viewport to deselect World.

```{tip}
You can turn off highlighted selection to better see the material change when selecting different variants. In order to turn off the highlighted selection, go to **Display > Selection Highlighting > Never**.
```

![](../../images/composition-arcs/image55.png)

So what exactly is changing when we select blue as our variant?

5. In the tree view, select **Shader**. From there, we can see that `inputs:diffuseColor` is `(0,0,1)`, representing the color blue.

![](../../images/composition-arcs/image71.png)

6. Now change the variant to red. In the tree view, select **World** and in the *Meta Data* tab, click on the **drop down** next to color variant and select **red**.

![](../../images/composition-arcs/image75.gif)

7. Then, in the tree view, click on **Shader** again and notice that `inputs:diffuseColor` now has a value of `(1,0,0)`.

![](../../images/composition-arcs/image79.png)

The “color variant” variant set is sparsely overriding the `inputs:diffuseColor` property. Now let’s see how variant sets can define new prims.

8. In your Visual Studio Code terminal, **run** the code below to open the file in usdview:

Windows:
```powershell
.\scripts\usdview.bat .\composition_arcs\variant_sets\simple_example\variant_sets_define.usd
```
Linux:
```sh
./scripts/usdview.sh ./composition_arcs/variant_sets/simple_example/variant_sets_define.usd
```

9. Make sure you have the **Meta Data** tab selected. In the tree view, select **CubeStack**. The variant set is called “Count variant”. Try selecting different options in the drop down.

![](../../images/composition-arcs/image47.png)

![](../../images/composition-arcs/image69.gif)

What do you notice happening in the {term}`layer <Layer>`? Can you see the changes in the tree view?

In this example, we’re showing how one can define {term}`prims <Prim>` using variant sets. A use case utilizing this example is creating a shelf for your factory. You can swap between various sizes of the shelf that are defining a new row using the same prim.

Let’s take a look at our last example, where we are authoring new {term}`composition arcs <Composition Arcs>` that would only exist within that variant.

10. In the Visual Studio Code terminal, **run** the code below to open the file in usdview:

Windows:
```powershell
.\scripts\usdview.bat .\composition_arcs\variant_sets\simple_example\variant_sets_add_arcs.usd
```
Linux:
```sh
./scripts/usdview.sh ./composition_arcs/variant_sets/simple_example/variant_sets_add_arcs.usd
```

11. Select the **Meta Data** tab. In the tree view, select **World**. The variant set is called “color variant”. Try selecting different options in the drop down.

![](../../images/composition-arcs/image65.png)

At first, this appears to be similar to our first example. However, the material is being composed through a {term}`reference <Reference>`.

12. To see where the material is being composed from, select **CubeMaterial** in the tree view.

![](../../images/composition-arcs/image15.png)

13. In the *Meta Data* tab, notice that the reference is coming from `materials.usd` and targeting the `/Looks/Red` prim as a source. If you selected a different color from the drop down, you might see `/Looks/Green` or `/Looks/Blue` instead.

![](../../images/composition-arcs/image11.png)

Try going back to **World** in the tree view and change the selected variant. See how that changes the reference for CubeMaterial.

Let’s see how we can use variant sets in a practical setting.

Here we are tasked to add a variant for turning off and on the lights. This will be used later for night and day scenes. Right now, the street lamp is always on by default. Let's add a way to control the lights by adding a variant set to the street lamp.

14. **Open** the following file in Visual Studio Code:  `composition_arcs/variant_sets/exercise/variant_sets_exercise.py`

15. First, let’s add a new empty variant set. **Add** the following code into the “Part 1” code block.

```py
vset: Usd.VariantSet = root.GetVariantSets().AddVariantSet("lights")
vset.AddVariant("on")
vset.AddVariant("off")
```

16. Next, let’s define what each variant is. The first variant will be “on”**.** We’ll call our function `toggle_lights()`, which sets the intensity and emissive color of the light and material respectively. **Add** the following code into the “Part 2” code block.

```py
vset.SetVariantSelection("on")
with vset.GetVariantEditContext():
    toggle_lights(True)
```

17. We will repeat this for the “off” variant. **Add** the following code into the “Part 3” code block.

```py
vset.SetVariantSelection("off")
with vset.GetVariantEditContext():
    toggle_lights(False)
```

18. **Save** the file.

19. In the terminal, **run** the following code:

Windows:
```powershell
python .\composition_arcs\variant_sets\exercise\variant_sets_exercise.py
```
Linux:
```sh
python ./composition_arcs/variant_sets/exercise/variant_sets_exercise.py
```

20. In the terminal, **run** the following code to open the file in usdview:

Windows:
```powershell
.\scripts\usdview.bat .\composition_arcs\variant_sets\exercise\street_lamp_dbl_vset.usda
```
Linux:
```sh
./scripts/usdview.sh ./composition_arcs/variant_sets/exercise/street_lamp_dbl_vset.usda
```

21. With the **World** prim selected, swap between the variants in the *Meta Data* tab. Switch between **on** and **off**.

![](../../images/composition-arcs/image20.gif)