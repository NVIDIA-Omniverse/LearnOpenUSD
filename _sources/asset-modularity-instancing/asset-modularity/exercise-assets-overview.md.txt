# Exercise: Assets Overview

In this exercise, we will explore and get familiar with the assets that will be used in this course.

1. **Run** in the terminal:
```powershell
.\scripts\usdview.bat .\instancing_exercises\ex_assets_overview\AssetsLineup.usd
```
2. **Click** *Camera > Select Camera > ExCam_01* from the Viewport panel.

![](../../images/asset-modularity-instancing/select_exercise_cam.png)

You should see a view like this in the viewport now:

![](../../images/asset-modularity-instancing/ex_assets_overview-cam_view.png)

```{tip}
**Click** *Camera > Select Camera > ExCam_01* if you ever lose your place in the scene or want to get back to this camera position.
```

These are the five modular assets that we will be using. Let's review them from left to right. First, there are three component assets:
* CubeBox_A04_26cm
* BlockPallet_A07
* BulkStorageRack_A01

The component assets are used in the next two assemblies:
* BoxPallet_A01
* Rack_BoxPallet_A01

Here's a breakdown of these two assemblies:
* BoxPallet_A01
  * 18 CubeBox_A04_26cm (component)
  * 1 BlockPallet_A07 (component)
* Rack_BoxPallet_A01
  * 3 BoxPallet_A01 (assembly)
  * 1 BulkStorageRack_A01 (component)

With just few simple assets, we're able to demonstrate the concepts of asset modularity. We are reusing components in assemblies and even assemblies within another assembly.

3. **Close** usdview.

4. **Run** in the terminal:
```powershell
.\scripts\usdview.bat .\instancing_exercises\ex_assets_overview\Scenario.usd
```
5. **Click** *Camera > Select Camera > ExCam_01* from the Viewport panel.

This is a warehouse scenario with 25 racks of boxes. This is the what we will use to explore how to use scenegraph instancing effectively.

![](../../images/asset-modularity-instancing/warehouse.png)

This scenario has:
* 25 BulkStorageRack_A01
* 75 BlockPallet_A7
* 1350 CubeBox_A04_26cm
* 44408 prims

6. **Close** usdview.