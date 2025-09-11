# Exercise: Lofting Variant Sets

For this exercise, we added a variant set called `exteriorType` to control the main exterior color. This is defined on the "**Looks**" Scope. We will loft the variant set so that it will be accessible as a new asset parameter and make sure it's available even with the payload unloaded.

1. **Open** the output `lrg_bldgF` in usdview by **running** the following command in Visual Studio Code:

Windows:
```powershell
.\scripts\usdview.bat .\asset_structure\exercise_08\lrg_bldgF.usd
```
Linux:
```sh
./scripts/usdview.sh ./asset_structure/exercise_08/lrg_bldgF.usd
```

2. In usdview, click on the "**Looks**" Scope in the tree view. Note that the *Meta Data* tab shows a new variant set, `exteriorType`.  

![](../../images/asset-structure/image16.png)

3. In the *Meta Data* tab, click on the `exteriorType` variant set dropdown and change the variant selection to “**brick**”. Note the building color change in the viewport.

![](../../images/asset-structure/image47.png)

4. In Visual Studio Code, **open** the following file:  `asset_structure/exercise_08/loft_variant_set.py`

5. Let’s add the code to loft the `exteriorType` variant set from the “**Looks**” Scope to the asset entry point. **Add** the code below into the block:

```py
# Create the same variant set on the default_prim.
lofted_vset: Usd.VariantSet = default_prim.GetVariantSets().AddVariantSet(vset_name)
for variant in variants:
    lofted_vset.AddVariant(variant)
    lofted_vset.SetVariantSelection(variant)
    # The lofted variant set just selects the
    # same variant from the nested variant set.
    with lofted_vset.GetVariantEditContext():
        vset.SetVariantSelection(variant)
lofted_vset.SetVariantSelection(default)
```

Here, we’re lofting the `exteriorType` variant set by creating a matching variant set on the asset entry point. Each variant on the new variant set has just one opinion, it selects its matching variant from the `exteriorType` variant set on the “**Looks**” prim.

6. **Save** the file and then **execute** the script using the following command:

Windows:
```powershell
python .\asset_structure\exercise_08\loft_variant_set.py
```
Linux:
```sh
python ./asset_structure/exercise_08/loft_variant_set.py
```

7. **Open** the output `lrg_bldgF` in usdview by **running** the following command:

Windows:
```powershell
.\scripts\usdview.bat .\asset_structure\exercise_08\lrg_bldgF.usd
```
Linux:
```sh
./scripts/usdview.sh ./asset_structure/exercise_08/lrg_bldgF.usd
```

8. In usdview, click on the "**Looks**" Scope in the tree view. Note that the *Meta Data* tab shows that the `exteriorType` variant set is set to “**stucco**”.

![](../../images/asset-structure/image16.png)

9. In usdview, click on the "**World**" (default) prim in the tree view.

![](../../images/asset-structure/image58.png)

10. In the *Meta Data* tab, click on the **`exteriorType`** variant set dropdown and change the variant selection to “**brick**”. Note the building color change in the viewport.

![](../../images/asset-structure/image8.gif)

11. In usdview, click on the "**Looks**" Scope in the tree view. Note that the *Meta Data* tab shows that the `exteriorType` variant set has also been set to “brick”.

![](../../images/asset-structure/image29.png)