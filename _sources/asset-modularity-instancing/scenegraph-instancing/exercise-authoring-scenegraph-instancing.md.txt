# Exercise: Author Scenegraph Instancing

In this exercise, we will be enabling instancing on all of our component assets. We will observe the impact on the runtime data models and we will compare the startup time of usdview with and without instancing. While this will be an imperfect measurement of performance due to a number of variables that can come into play, it should at least indicate some improvement in performance when using instancing. For a more robust way to measure performance, we recommend the `usdmeasureperformance.py` script included with OpenUSD.


1. **Run** in the terminal:
```powershell
.\scripts\usdview.bat .\instancing_exercises\ex_sg_author_inst\Scenario.usd --camera ExCam_01
```

```{tip}
**Click** *Camera > Select Camera > ExCam_01* if you ever lose your place in the scene or want to get back to this camera position.
```

2. **Click** on the *?* button on the bottom right of the Tree View panel.
![](../../images/asset-modularity-instancing/ex_sg_enable_inst-legend.png)

This will open up the Prim Legend drawer. This legend indicates that scenegraph instances are have light blue text and Prototypes have dark blue text in the Tree View. In this case, we have not enabled instancing yet, so you can see that the stage has no instance prims if you explore the Tree View.

![](../../images/asset-modularity-instancing//inst-proto-legend.png)

3. **Click** *Window > Interpreter* to open the Interpreter window.
4. **Run** the following code in the Interpreter window:
```python
from pprint import pprint
stats = UsdUtils.ComputeUsdStageStats(usdviewApi.stage)
pprint(stats)
```
This should print to the Interpreter window some USD statistics like this:

![](../../images/asset-modularity-instancing//usd-stats.png)

These stats are a useful overview of the contents of your stage including instancing statistics. In this case, we will focus on: `totalPrimCount`, `totalInstanceCount`, and `prototypeCount` to understand the impact of different modifications we make to our stage. Here's a summary of the stats so far:

Scenario | Prims | Instances | Prototypes 
---|---|---|---
No Instancing | 44408 | 0 | 0
Instancing | - | - | -

5. **Close** usdview.

6. **Run** in the terminal:
```powershell
Measure-Command { .\scripts\usdview.bat .\instancing_exercises\ex_sg_author_inst\Scenario.usd --quitAfterStartup }
```

This will measure how long it takes to execute usdview. usdview is an interactive app, but with the `--quitAfterStartup` flag we can just time the startup and time to first frame with the Storm renderer. You can run the command a few times and take an average for a more reliable result. My average was 27.77 seconds on a mid-end laptop.

7. **Open** `instancing_exercises/ex_sg_author_inst/toggle_inst.py` in VSCode to inspect its code.
8. **Run** in the terminal:
```powershell
python .\instancing_exercises\ex_sg_author_inst\toggle_inst.py 1
```

9. **Run** in the terminal:
```powershell
.\scripts\usdview.bat .\instancing_exercises\ex_sg_author_inst\Scenario.usd --camera ExCam_01
```
Note that the component assets in Tree View now have light blue text.

![](../../images/asset-modularity-instancing//light-blue-instances.png)

10. **Click** the triangle icon to the left of "World" in the Tree View to collapse that prim hierarchy.

![](../../images/asset-modularity-instancing/first_prototypes.png)

Note the three prototype prims in dark blue at the bottom. All of the instances in this stage are based on three prototypes. Can you guess what they are?

```{warning}
If the prototypes are not showing, ensure you have gone through the [Setup instructions](../setup.md) to enable *Show > Prototype Prims* among other settings for a smooth experience when following our instructions.
```

11. **Click** on the top left box closest to the camera in the Viewport.
![](../../images/asset-modularity-instancing/select_instanced_box.png)
12. Hover your mouse over the Tree View panel and **press** the "F" key to frame the selected prim in the Tree View.

You should see "CubeBox_A04_26cm_18" selected in the Tree View panel.

13. **Click** the triangle to the left of the select prim in the Tree View to expand the select prim's hierarchy.

Note that it's ancestors are dark blue. These are prims based on a prototype. These are instance proxies.

14. **Click** *Window > Interpreter* to open the Interpreter window.
15. **Run** the following code in the Interpreter window:
```python
from pprint import pprint
stats = UsdUtils.ComputeUsdStageStats(usdviewApi.stage)
pprint(stats)
```

How have the stats changed now that the component assets are instanced? Here is a summary of the results comparing the stats of the Scenario stage with and without instancing:

Scenario | Prims | Instances | Prototypes 
---|---|---|---
No Instancing | 44408 | 0 | 0
Instancing | 1711 | 1450 | 3

16. **Close** usdview.

17. **Run** in the terminal:
```powershell
Measure-Command { .\scripts\usdview.bat .\instancing_exercises\ex_sg_author_inst\Scenario.usd --quitAfterStartup }
```

This will measure how long it takes to execute usdview. My average was 18.98 seconds on a mid-end laptop. That's roughly a **46.3% speed up** to render the first frame with usdview and the Storm renderer.

Scenario | Execution Time (sec) | Improvement (%)
---|---|---
No Instancing | 27.77 | 0% (Baseline)
Instancing | 18.98 | +46.3%