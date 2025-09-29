# Exercise: Authoring Point Instancing

## Introduction

In this exercise, you will learn how to create a PointInstancer from a JSON file that emulates exported data from a simulation application. Point instancing is a powerful technique for efficiently representing large numbers of similar objects. You'll read scatter data of boxes and pallets and create a PointInstancer prim. This technique is essential for handling massive datasets in production workflows.

## Exploring the Point Instancer Script

1. **Open** `instancing/ex_pt_author/author_point_instancer.py` in VSCode to inspect the code.

```{literalinclude} ../../exercise_content/instancing/ex_pt_author/author_point_instancer.py
:caption: author_point_instancer.py
:lines: 16-
:lineno-start: 16
:linenos:
```

The script reads position, orientation, and prototype data from a JSON file, then creates a PointInstancer with two prototypes (a box and a pallet) and populates it with thousands of instances. This demonstrates how to efficiently create thousands of instances of individual assets using a PointInstancer.

## Running the Point Instancer Script

2. **Run** in the terminal:

Windows:
```powershell
python .\instancing\ex_pt_author\author_point_instancer.py
```
Linux:
```sh
python ./instancing/ex_pt_author/author_point_instancer.py
```

You shouldn't notice any additional output in the terminal or file system. We will open up `Scenario.usd` in usdview to see what the script did.

## Viewing the Point Instancer Results

3. **Run** in the terminal:

Windows:
```powershell
.\scripts\usdview.bat .\instancing\ex_pt_author\Scenario.usd --camera ExCam_01
```
Linux:
```sh
./scripts/usdview.sh ./instancing/ex_pt_author/Scenario.usd --camera ExCam_01
```

![](../../images/asset-modularity-instancing/point-instancer.png)

Notice how the scattered boxes and pallets are now represented as a single PointInstancer prim, dramatically reducing the scene complexity while maintaining the same visual appearance as if we had used scenegraph instancing.

4. **Close** usdview.

## Conclusion

You've successfully learned how to create PointInstancers from exported data, a crucial technique for handling large-scale scenes efficiently. PointInstancer can represent 100,000s of objects with minimal memory overhead while maintaining full visual fidelity, making this approach essential for production workflows with massive datasets.

