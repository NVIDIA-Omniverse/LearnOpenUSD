# Exercise: Assets Overview

## Introduction
In this exercise, you will explore the modular asset library that forms the foundation of this instancing module. You'll examine five key assets ranging from simple components to complex assemblies, understanding how they combine to create a realistic warehouse scenario with over 44,000 prims from just a few reusable building blocks.

## Exercise Steps

1. **Run** in the terminal:

Windows:
```powershell
.\scripts\usdview.bat .\instancing\ex_assets_overview\AssetsLineup.usd
```
Linux:
```sh
./scripts/usdview.sh ./instancing/ex_assets_overview/AssetsLineup.usd
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

```{tip}
Spend some time exploring the folder and asset structure for these assets in `instancing/src_assets/`.
```

Next we will explore how we used these assets to build up a warehourse scenario.

3. **Close** usdview.

4. **Run** in the terminal:

Windows:
```powershell
.\scripts\usdview.bat .\instancing\ex_assets_overview\Scenario.usd
```
Linux:
```sh
./scripts/usdview.sh ./instancing/ex_assets_overview/Scenario.usd
```

5. **Click** *Camera > Select Camera > ExCam_01* from the Viewport panel.

This is a warehouse scenario with 25 racks of boxes. This is scene we will use as we learn how to use scenegraph instancing effectively.

![](../../images/asset-modularity-instancing/warehouse.png)

This scenario has:
* 25 BulkStorageRack_A01
* 75 BlockPallet_A7
* 1350 CubeBox_A04_26cm
* 44408 prims

To make this stage, all we had to do was reference and arrange "BulkStorageRack_A01" 25 times. You can see how leveraging asset modularity we can hide a lot of complexity as we build up large scenes for higher level workflows.

6. **Close** usdview.

## Key Takeaways

You've successfully explored the modular asset system that enables efficient scene construction through strategic reuse. By understanding how simple components combine into assemblies and scale into complex environments, you've gained insight into the power of asset modularity for managing large-scale 3D scenes with minimal complexity.
