# Exercise: Components

For this exercise, we will set the {term}`model kind <Model>` {term}`metadata <Metadata>` on the default prim to make this {term}`asset <Asset>` a {term}`component <Component>` asset.

1. In Visual Studio Code, **open** the following file: `asset_structure/exercise_09/set_model_kind.py`

2. Let’s use `Usd.ModelAPI` to set the component kind on the asset entry point. **Add** the code below into the block:

```py
Usd.ModelAPI(default_prim).SetKind(Kind.Tokens.component)
```

3. **Save** the file and then execute the script using the following command:

Windows:
```powershell
python .\asset_structure\exercise_09\set_model_kind.py
```
Linux:
```sh
python ./asset_structure/exercise_09/set_model_kind.py
```

4. **Run** the following command in Visual Studio Code to open the file in usdview:

Windows:
```powershell
.\scripts\usdview.bat .\asset_structure\exercise_09\lrg_bldgF.usd
```
Linux:
```sh
./scripts/usdview.sh ./asset_structure/exercise_09/lrg_bldgF.usd
```

5. In usdview, click on the "**World**" (default) prim in the tree view. Note that the *Meta Data* tab shows that the `kind` field is set to `component`. This is a component asset now.

![](../../images/asset-structure/image7.png)