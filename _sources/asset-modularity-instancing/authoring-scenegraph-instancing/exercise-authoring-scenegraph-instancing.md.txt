# Exercise: Author Scenegraph Instancing

## Introduction

In this exercise, you will learn how to enable scenegraph instancing on component assets and measure its performance impact. You'll use a Python script to toggle instancing, observe how instances and prototypes appear in usdview, and compare startup times to demonstrate the significant performance benefits of instancing in USD workflows.

```{seealso}
While this will be an imperfect measurement of performance due to a number of variables that can come into play, it should at least indicate some improvement in performance when using instancing. For a more robust way to measure performance, we recommend the [`usdmeasureperformance.py` script](inv:usd:std#toolset:usdmeasureperformance) included with OpenUSD.

For more information about measuring performance, checkout OpenUSD's [Performance Metrics](inv:usd:std#ref_performance_metrics) document.
```

## Exercise Steps

Let's start by opening the warehourse scenario where we will be enabling instancing.

1. **Run** in the terminal:

Windows:
```powershell
.\scripts\usdview.bat .\instancing\ex_sg_author_inst\Scenario.usd --camera ExCam_01
```
Linux:
```sh
./scripts/usdview.sh ./instancing/ex_sg_author_inst/Scenario.usd --camera ExCam_01
```

```{note}
This time we launched usdview with `--camera ExCam_01`. This automatically selects the Camera prim named "ExCam_01" as the active camera for the viewport.
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

The USD statistics can be a useful frame of reference, but we should also measure performance so we can understand what kind of productivity gains we could expect from using scenegraph instancing.

6. **Run** in the terminal:

Windows:
```powershell
Measure-Command { .\scripts\usdview.bat .\instancing\ex_sg_author_inst\Scenario.usd --quitAfterStartup }
```
Linux:
```sh
time ./scripts/usdview.sh ./instancing/ex_sg_author_inst/Scenario.usd --quitAfterStartup
```

`Measure-Command` and `time` are being used to measure how long it takes to execute usdview. usdview is an interactive app, but with the `--quitAfterStartup` flag we can just time the startup and the time to first frame with the Storm renderer. You can run the command a few times and take an average for a more reliable result. My average was 27.77 seconds on a mid-end laptop.

7. **Open** `instancing/ex_sg_author_inst/toggle_inst.py` in VSCode to inspect its code.

```{literalinclude} ../../exercise_content/instancing/ex_sg_author_inst/toggle_inst.py
:caption: toggle_inst.py
:lines: 16-
:lineno-start: 16
:linenos:
```

This script opens `Scenario.usd`, traverses the stage to find all component models, and sets `instanceable` to enable or disable scenegraph instancing based on a commandline argument.

Let's try it out.

8. **Run** in the terminal:

Windows:
```powershell
python .\instancing\ex_sg_author_inst\toggle_inst.py 1
```
Linux:
```sh
python ./instancing/ex_sg_author_inst/toggle_inst.py 1
```

With the `1` argument, this script now sets all component models in `Scenario.usd` to `instanceable=true`. Let's open usdview to see what happened.

9. **Run** in the terminal:

Windows:
```powershell
.\scripts\usdview.bat .\instancing\ex_sg_author_inst\Scenario.usd --camera ExCam_01
```
Linux:
```sh
./scripts/usdview.sh ./instancing/ex_sg_author_inst/Scenario.usd --camera ExCam_01
```
Note that the component assets in the Tree View now have light blue text. This indicates that they are now **instances** according to the Prim Legend.

![](../../images/asset-modularity-instancing/light-blue-instances.png)

10. **Click** the triangle icon to the left of "World" in the Tree View to collapse that prim hierarchy.

![](../../images/asset-modularity-instancing/first_prototypes.png)

Note the three **prototypes** in dark blue at the bottom. All of the instances in this stage are based on three prototypes. Can you guess what they are?

```{warning}
If the prototypes are not showing, ensure you have gone through the [Setup instructions](../setup.md) to enable *Show > Prototype Prims* among other settings for a smooth experience when following our instructions.
```

We enabled instancing on the component models and we have three component models with distinct composition arc configurations: 

* CubeBox_A04_26cm
* BlockPallet_A07
* BulkStorageRack_A01

This is the basis for our prototypes.

11. **Click** on the top left box closest to the camera in the Viewport.
![](../../images/asset-modularity-instancing/select_instanced_box.png)
12. Hover your mouse over the Tree View panel and **press** the "F" key to frame the selected prim in the Tree View.

You should see "CubeBox_A04_26cm_18" selected in the Tree View panel.

13. **Click** the triangle to the left of the select prim in the Tree View to expand the select prim's hierarchy.

Note that it's ancestors are dark blue. These are prims based on a prototype. These are **instance proxies**.

Let's check the USD stage statistics to see what sort of impact this instancing had.

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

That's a considerable reduction in prim count! What about performance?

16. **Close** usdview.

17. **Run** in the terminal:

Windows:
```powershell
Measure-Command { .\scripts\usdview.bat .\instancing\ex_sg_author_inst\Scenario.usd --quitAfterStartup }
```
Linux:
```sh
time ./scripts/usdview.sh ./instancing/ex_sg_author_inst/Scenario.usd --quitAfterStartup
```

This will measure how long it takes to execute usdview. My average was 18.98 seconds on a mid-end laptop. That's roughly a **46.3% speed up** to render the first frame with usdview and the Storm renderer compared to no instancing.

Scenario | Execution Time (sec) | Improvement (%)
---|---|---
No Instancing | 27.77 | 0% (Baseline)
Instancing | 18.98 | +31.7%

Your numbers will differ depending on your hardware and other factors, but you should still see an increase in performance.

## Conclusion

You've successfully enabled scenegraph instancing and witnessed its dramatic performance improvements. By reducing 44,408 prims to just 1,711 prims through instancing, you've seen how USD's instancing system can deliver substantial performance gains while maintaining visual fidelity in complex scenes.