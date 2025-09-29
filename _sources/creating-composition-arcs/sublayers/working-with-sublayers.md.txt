# Exercise: Working with Sublayers

1. Head over to Visual Studio Code and open the following file: 
   `composition_arcs/sublayers/simple_example/sublayerA.usd`

   We will also be looking into `sublayerB.usd` and `sublayers_simple.usd`.
   ![](../../images/composition-arcs/image45.png)

Looking at `sublayerA.usda` we can see that a `Cube` is being defined under `Geometry` which is a child of `World`. You might have noticed that `World` and `Geometry` both have an *over* specifier.

Now, let’s look at `sublayerB.usda`. You should notice two changes compared to `sublayerA.usda`. Those differences are a new *def* specifier for a `Sphere` and an *over* specifier for `Cube`.

**So why are over specifiers being used here?**

Over is short for “override” or “compose over”, and its purpose is to provide a neutral prim container for overriding opinions. Even when an over appears in a stronger layer than a def or class for the same `primSpec` it does not change the resolved specifier for that prim. In the case of `sublayerB.usda`, we are authoring an overriding opinion for `Geometry` in which we have defined a `Sphere` prim.

Let’s open `sublayers_simple.usda`. What do you notice? Any differences between the two USDA files we looked at previously?

2. Keep those differences in mind as we open `sublayers_simple.usd` in usdview. In the terminal, **run** the following command:

Windows:
```powershell
.\scripts\usdview.bat .\composition_arcs\sublayers\simple_example\sublayers_simple.usd
```
Linux:
```sh
./scripts/usdview.sh ./composition_arcs/sublayers/simple_example/sublayers_simple.usd
```

Here is what the file looks like in usdview:

![](../../images/composition-arcs/image52.png)

Were your assumptions correct? Now that you can visually view the USD file, what are some observations you have that you didn’t have before?

After opening the USD file in usdview, we can inspect where prims are coming from.

3. Below the *Viewport,* select the **Layer Stack** tab. It will show you the layer stack for the selected prim.
4. Try selecting the **Cube** and **Sphere** in our stage tree and see how the layer stack changes.

![](../../images/composition-arcs/image31.gif)

Selecting **Cube**, we can see there is an opinion coming from both `sublayerB.usda` and `sublayerA.usda` in the layer stack. However, when we click on **Sphere**, `sublayerB.usda` is the only one in the layer stack.

Before we continue, think about the behavior we’re seeing.

Why is the sphere on top of the cube, what caused this?

What would happen if `sublayerB` defined a cube rather than a sphere?

How can we apply this to other industries?

Imagine we have received two layers, one containing the geometry of a building (`geometry.usd`) from one workstream and another containing all the materials (`shading.usd`). So how can we combine the two? By creating a new USD layer, we can add both `geometry.usd` and `shading.usd` as sublayers.

![](../../images/composition-arcs/image92.png)
![](../../images/composition-arcs/image53.png)

You can find these files in the `composition_arcs/sublayers/exercise/contents/` folder.
![](../../images/composition-arcs/image73.png)

5. To start, go to `composition_arcs/sublayers/exercise/sublayers_exercise.py` from Visual Studio Code’s explorer window.

We will be adding in code that adds sublayers to our root layer. This is done using [Sdf.Layer API](https://openusd.org/release/api/class_sdf_layer.html).

![](../../images/composition-arcs/image94.png)

Let’s talk about what is going on in this script.

```{literalinclude} ../../exercise_content/composition_arcs/sublayers/exercise/sublayers_exercise.py
:caption: sublayers_exercise.py
:linenos:
```

Currently, our script is creating a new root layer that is in centimeters with the Y-axis as our up axis. The stage gets saved into `my_skyscraper.usda`.

First we want to retrieve the root layer from our stage then append the sublayers. The first appended sublayer will have the highest opinion.

6. **Add** the code into the designated section inside of `sublayers_exercise.py`

```py
root_layer: Sdf.Layer = stage.GetRootLayer()
root_layer.subLayerPaths.append("./contents/shading.usd")
root_layer.subLayerPaths.append("./contents/geometry.usd")
```
7. **Save** the file. (Ctrl + S) or *File > Save*
8. Let's run the script. In the terminal, **run** the following code:

Windows:
```powershell
python .\composition_arcs\sublayers\exercise\sublayers_exercise.py
```
Linux:
```sh
python ./composition_arcs/sublayers/exercise/sublayers_exercise.py
```

Now, we should see a new file: `my_skyscraper.usda`.

9. Let’s view it in usdview. In the terminal, **run** the following code:

Windows:
```powershell
.\scripts\usdview.bat .\composition_arcs\sublayers\exercise\my_skyscraper.usda
```
Linux:
```sh
./scripts/usdview.sh ./composition_arcs/sublayers/exercise/my_skyscraper.usda
```

![](../../images/composition-arcs/image18.png)

Here, we can see the sublayers we added by selecting root in the hierarchy window in the top left. In the *Meta Data* tab at the bottom right, there will be a section for `subLayers`.

You can look at the completed script in: `composition_arcs/sublayers/exercise/sublayers_exercise_full.py`