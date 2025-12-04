# Exercise: Adding User Workstreams

In this exercise, we'll organize our {term}`asset <Asset>` structure into {term}`layers <Layer>`, specifically `geometry.usd` and `shading.usd`, to manage our workstreams effectively. We've already taken the first step by moving the geometry to a `geometry.usd` layer. You can think of this as if a modeler had exported the initial {term}`model <Model>` from their digital content creation tool (DCC) into the `geometry.usd` layer.

Next, we'll create a script to simulate the work of a surfacing artist. This script will mimic a sparse export of only material and binding information from a surfacing DCC. This data will be authored to a `shading.usd` layer, which we will then add as a {term}`sublayer <Sublayer>` to our asset.

---

1. Let’s look at `lrg_bldgF.usd`. In the Visual Studio Code terminal, **run** the following command to **open** the layer in usdview:

Windows:
```powershell
.\scripts\usdview.bat .\asset_structure\exercise_04\lrg_bldgF.usd
```
Linux:
```sh
./scripts/usdview.sh ./asset_structure/exercise_04/lrg_bldgF.usd
```

![](../../images/asset-structure/image4.png)

As we can see, the asset does not have any materials assigned to it. This represents the state before a surfacing artist has begun their work on the asset.

Now, let's simulate the work of a surfacing artist through a Python script.

2. In Visual Studio Code, **open** the following file: `asset_structure/exercise_04/export_sparse_materials.py`

Notice the `material_data` defined at the top of the script. This represents the data that we might have extracted from a DCC, reflecting the work of a surfacing artist.

3. In the Visual Studio Code terminal, **run** the following command to execute the script:

Windows:
```powershell
python .\asset_structure\exercise_04\export_sparse_materials.py
```
Linux:
```sh
python ./asset_structure/exercise_04/export_sparse_materials.py
```

After running the script, a `shading.usd` layer has been written to the contents folder and added as a sublayer to `lrg_bldgF.usd`.

4.  **Open** the layer with usdview using the following command:

Windows:
```powershell
.\scripts\usdview.bat .\asset_structure\exercise_04\lrg_bldgF.usd
```
Linux:
```sh
./scripts/usdview.sh ./asset_structure/exercise_04/lrg_bldgF.usd
```

![](../../images/asset-structure/image17.png)

After running the script, we can see that the materials are bound to the mesh subset and show up on our model.

Let’s simulate another shading update to the asset.

5.  In Visual Studio Code, go back to our `export_sparse_material.py` script.

6.  **Locate** `diffuseColor` for `roof` in our `material_data` dictionary.

```py
material_data = {
	"materials": {
 	"door": {"diffuseColor": (0.3882353, 0.4, 0.44705883), "roughness": 1.0, "metallic": 1.0},
 	"window": {"diffuseColor": (0.7372549, 0.8862745, 1), "roughness": 1.0, "metallic": 1.0},
 	"material_defaultMat": {"diffuseColor": (0.764151, 0.764151, 0.764151), "roughness": 1.0, "metallic": 1.0},
 	"border": {"diffuseColor": (0.56078434, 0.5686275, 0.6), "roughness": 1.0, "metallic": 1.0},
 	"roof": {"diffuseColor": (0.3372549, 0.7372549, 0.6), "roughness": 1.0, "metallic": 1.0},
	},
	"assignments": {
 	"large_buildingF": {
     	"subsets": {
         	"door": "door",
         	"window":"window",
         	"subset_defaultMat": "material_defaultMat",
         	"border": "border",
         	"roof": "roof"
     	},
     	"mesh_mtl": None
 	}
	 
	}
}
```

7.  Change the values for `diffuseColor` in `roof` to **`(0.0, 0.0, 1.0)`**.

```py
"roof": {"diffuseColor": (0.0, 0.0, 1.0), "roughness": 1.0, "metallic": 1.0},
```

8.  **Save** the file and **run** the following command in the terminal:

Windows:
```powershell
python .\asset_structure\exercise_04\export_sparse_materials.py
```
Linux:
```sh
python ./asset_structure/exercise_04/export_sparse_materials.py
```

9. Now, let’s view the file by **running** the following command in the terminal:

Windows:
```powershell
.\scripts\usdview.bat .\asset_structure\exercise_04\lrg_bldgF.usd
```
Linux:
```sh
./scripts/usdview.sh ./asset_structure/exercise_04/lrg_bldgF.usd
```

![](../../images/asset-structure/image53.png)

Now our roof is blue instead of green. What can we infer from this?

We can infer that this setup, with separate workstreams for modeling and surfacing, allows the modeling artist and the surfacing artist to iterate on the same asset independently. This way, they don't block each other's progress and avoid conflicts.