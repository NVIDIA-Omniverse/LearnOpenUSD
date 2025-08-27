# Nested Instancing

![](../../images/asset-modularity-instancing/slides/Slide35.jpg)

Instances can contain other instances.

Common patterns:
* Instanced assemblies with instanced components.
* Instanced components with instanced material networks.

Enables large-scale scene aggregation.
Scenegraph instances can include Point Instancers too and vice versa.
Be cautious about too much complexity

## Exercise: Nested Scenegraph Instancing

In this exercise, we will start with the instanced component assets and introduce nested instancing by enabling instancing for the entire rack assemblies. We will see how that impacts performance as well as authoring flexibility.

1. **Run** in the terminal:
```powershell
.\scripts\usdview.bat .\instancing_exercises\ex_sg_nested_inst\Scenario.usd --camera ExCam_01
```

```{tip}
**Click** *Camera > Select Camera > ExCam_01* if you ever lose your place in the scene or want to get back to this camera position.
```

2. **Click** on the top left box in the Viewport.
3. Hover your mouse over the Tree View panel and **press** the "F" key to frame the selected prim in the Tree View. 

You should see "CubeBox_A04_26cm_18" selected in the Tree View panel. Note the light blue text indicating that we have instancing enabled for our component assets. In the next steps, we are going to utilize nested instancing and see how that impacts the stage.

Note also the decals on the boxes. The boxes with decals showing form a T-shape on the left pallet and the boxes on the right pallet have no decals showing.
![](../../images/asset-modularity-instancing//decal-config.png)

4. **Close** usdview.

5. **Open** `instancing_exercises/ex_sg_nest/toggle_nested_inst.py` in VSCode to inspect its code.
6. **Run** in the terminal:
```powershell
python .\instancing_exercises\ex_sg_nested_inst\toggle_nested_inst.py 1
```
7. **Run** in the terminal:
```powershell
.\scripts\usdview.bat .\instancing_exercises\ex_sg_nested_inst\Scenario.usd --camera ExCam_01
```

Note that the Rack_BoxPallet prims are now instances.
![](../../images/asset-modularity-instancing//rack-instances.png)

8. **Click** *Window > Interpreter* to open the Interpreter window.
9. **Run** the following code in the Interpreter window:
```python
from pprint import pprint
stats = UsdUtils.ComputeUsdStageStats(usdviewApi.stage)
pprint(stats)
```

Scenario | Prims | Instances | Prototypes 
---|---|---|---
No Instancing | 44408 | 0 | 0
Instancing | 1711 | 1450 | 3
Nested Instancing | 1482 | 25 | 1

10. **Close** the Interpreter window.

![](../../images/asset-modularity-instancing//local-opinion-lost.png)

Note that every pallet now has the same T-shape formation for box decals. The stage has lost a significant amount of diversity. A creator painstakingly authored local opinions in Warehouse.usd to give unique positions and rotations to each box for added realism. These opinions within the rack instances are now being ignored. We’ll look at this more closely in the next exercises.

11. **Close** usdview.

12. **Run** in the terminal:
```powershell
Measure-Command { .\scripts\usdview.bat .\instancing_exercises\ex_sg_nested_inst\Scenario.usd --quitAfterStartup }
```

This will measure how long it takes to execute usdview. usdview is an interactive app, but with the `--quitAfterStartup` flag we can just time the startup and time to first frame with the Storm renderer. You can run the command a few times and take an average for a more reliable result. My average was 5.31 seconds on a mid-end laptop. Let's compare my performance results of the different instancing strategies:

Scenario | Execution Time (sec) | Improvement (%)
---|---|---
No Instancing | 27.77 | 0% (Baseline)
Instancing | 18.98 | +46.3%
Nested Instancing | 5.31 | +423.0%
