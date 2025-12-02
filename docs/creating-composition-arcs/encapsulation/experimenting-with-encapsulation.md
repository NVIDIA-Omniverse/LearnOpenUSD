# Exercise: Experimenting With Encapsulation

Let's take a look at two examples, one showing proper encapsulation and the other as improper encapsulation.

1. First, we'll take a look at a {term}`layer <Layer>` with good encapsulation. In the Visual Studio Code terminal, **run** the following code:

Windows:
```powershell
.\scripts\usdview.bat .\composition_arcs\references\encapsulation_example\encapsulated_GOOD.usd
```
Linux:
```sh
./scripts/usdview.sh ./composition_arcs/references/encapsulation_example/encapsulated_GOOD.usd
```

2. Once the file opens in usdview, **expand** the root and its children in the tree view hierarchy in the top left corner.

![](../../images/composition-arcs/image97.png)

Why is it good? What are the clues to show that it is good encapsulation?

We can see in the tree that all {term}`prims <Prim>` are encapsulated under the default prim, 
"World".

3. Now let’s open an example of bad encapsulation. In the terminal in Visual Studio Code, **run** the following:

Windows:
```powershell
.\scripts\usdview.bat .\composition_arcs\references\encapsulation_example\unencapsulated_BAD.usd
```
Linux:
```sh
./scripts/usdview.sh ./composition_arcs/references/encapsulation_example/unencapsulated_BAD.usd
```

4. Back in usdview, **expand** the root and children in the hierarchy in the top left.

![](../../images/composition-arcs/image6.png)

Why is it bad? What are the clues to show that it is bad encapsulation?

As we can see here, our material sits outside of "World", under "Looks." A key part of this asset is not included under the default prim, World.

Let’s see what happens now when both layers are referenced into another layer.

5. In the terminal, **run** the following code:

Windows:
```powershell
.\scripts\usdview.bat .\composition_arcs\references\encapsulation_example\references_encapsulation.usd
```
Linux:
```sh
./scripts/usdview.sh ./composition_arcs/references/encapsulation_example/references_encapsulation.usd
```

![](../../images/composition-arcs/image88.png)

What can we infer about the scene?

As we can see, only one cube has both the mesh and the material brought over. Even though the unencapsulated layer had a material, it was not brought over when referenced. This is because the material was not encapsulated within World and our reference is targeting World as the source prim.

On the other hand, the "unencapsulated_BAD_02" prim is referencing the `encapsulated_GOOD.usd` layer, but it is referencing that asset not as intended by using the Cube as the source prim from the reference. If your reference target is Cube, it will not bring in the material because it’s not in the prim hierarchy.

You should also see output like this in the terminal noting the composition error:
```
Warning (secondary thread): in _ReportErrors at line 3309 of C:\g\163073426\USD\pxr\usd\usd\stage.cpp -- In </World/unencapsulated_BAD_01/Cube.material:binding>: The relationship target </Looks/RedMaterial> from </World/Cube.material:binding> in layer @composition_arcs/references/encapsulation_example/unencapsulated_BAD.usd@ refers to a path outside the scope of the reference from </World/unencapsulated_BAD_01>.  Ignoring. (getting targets for relationship </World/unencapsulated_BAD_01/Cube.material:binding> on stage @composition_arcs/references/encapsulation_example/references_encapsulation.usd@ <0000026F1FD334A0>)
Warning (secondary thread): in _ReportErrors at line 3309 of C:\g\163073426\USD\pxr\usd\usd\stage.cpp -- In </World/unencapsulated_BAD_02.material:binding>: The relationship target </World/RedMaterial> from </World/Cube.material:binding> 
in layer @composition_arcs/references/encapsulation_example/encapsulated_GOOD.usd@ refers to a path outside the scope of the reference from </World/unencapsulated_BAD_02>.  Ignoring. (getting targets for relationship </World/unencapsulated_BAD_02.material:binding> on stage @composition_arcs/references/encapsulation_example/references_encapsulation.usd@ <0000026F1FD334A0>)
```