# Exercise: Encapsulating Your Asset

Let’s look at an example of what encapsulation looks like.

1. **Open** up `lrg_bldgF.usd` in usdview by **running** the following command in your Visual Studio Code terminal:

Windows:
```powershell
.\scripts\usdview.bat .\asset_structure\exercise_02\lrg_bldgF.usd
```
Linux:
```sh
./scripts/usdview.sh ./asset_structure/exercise_02/lrg_bldgF.usd
```

![](../../images/asset-structure/image18.png)

Take note that the roof color is a shade of green. Now we will see what happens when we {term}`reference <Reference>` this {term}`layer <Layer>` into another layer.

2. **Open** up `scene.usda` in usdview by **running** the following command in the Visual Studio Code terminal:

Windows:
```powershell
.\scripts\usdview.bat .\asset_structure\exercise_02\scene.usda
```
Linux:
```sh
./scripts/usdview.sh ./asset_structure/exercise_02/scene.usda
```

![](../../images/asset-structure/image65.png)

In this scene, we’re referencing the building from the first file, but the roof is now white. Why is this? Also note the warnings in the terminal:
```
Warning: in _ReportErrors at line 3309 of C:\g\163073426\USD\pxr\usd\usd\stage.cpp -- In </World/lrg_bldgF_01/large_buildingF/roof.material:binding>: The relationship target </roof> from </World/large_buildingF/roof.material:binding> in layer @asset_structure/exercise_02/lrg_bldgF.usd@ refers to a path outside the scope of the reference from </World/lrg_bldgF_01>.  Ignoring. (getting targets for relationship </World/lrg_bldgF_01/large_buildingF/roof.material:binding> on stage @asset_structure/exercise_02/scene.usda@ <000001DFF5FC1DD0>)
Warning: in _ReportErrors at line 3309 of C:\g\163073426\USD\pxr\usd\usd\stage.cpp -- In </World/lrg_bldgF_02/large_buildingF/roof.material:binding>: The relationship target </roof> from </World/large_buildingF/roof.material:binding> in layer @asset_structure/exercise_02/lrg_bldgF.usd@ refers to a path outside the scope of the reference from </World/lrg_bldgF_02>.  Ignoring. (getting targets for relationship </World/lrg_bldgF_02/large_buildingF/roof.material:binding> on stage @asset_structure/exercise_02/scene.usda@ <000001DFF5FC1DD0>)
Warning: in _ReportErrors at line 3309 of C:\g\163073426\USD\pxr\usd\usd\stage.cpp -- In </World/lrg_bldgF_03/large_buildingF/roof.material:binding>: The relationship target </roof> from </World/large_buildingF/roof.material:binding> in layer @asset_structure/exercise_02/lrg_bldgF.usd@ refers to a path outside the scope of the reference from </World/lrg_bldgF_03>.  Ignoring. (getting targets for relationship </World/lrg_bldgF_03/large_buildingF/roof.material:binding> on stage @asset_structure/exercise_02/scene.usda@ <000001DFF5FC1DD0>)
```

The roof material {term}`prim <Prim>` was not fully encapsulated in `World`. Only prims defined beneath `World` were brought over.

How can we fix this? Very similar to how we created an entry point in the first exercise, let’s re-parent our roof so it is encapsulated underneath `World`.

3. **Open** `asset_structure/exercise_02/encapsulate.py` in Visual Studio Code. Note that this Python file contains very similar code to what we saw in our last exercise.   
4. In the terminal, **run** the following command:

Windows:
```powershell
python .\asset_structure\exercise_02\encapsulate.py
```
Linux:
```sh
python ./asset_structure/exercise_02/encapsulate.py
```

5. Next, **open** up `scene.usda` in usdview by **running** the following command:

Windows:
```powershell
.\scripts\usdview.bat .\asset_structure\exercise_02\scene.usda
```
Linux:
```sh
./scripts/usdview.sh ./asset_structure/exercise_02/scene.usda
```

![](../../images/asset-structure/image60.png)

Our roof material is now encapsulated within `World`, so in `scene.usda` the roof material now gets brought over with the referenced building prim.  