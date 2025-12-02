# Sublayers Frequently Asked Questions

Before we continue, let’s talk about some common questions you may have about {term}`sublayers <Sublayer>`.

## What Is `subLayerPaths`?

`subLayerPaths` is a property within the `Sdf` API. It is a list that contains all the sublayers in a {term}`Layer <Layer>`.

Why can we not use the C++ `SetSubLayerPaths(const std::vector< std::string > &newPaths)` or `InsertSubLayerPath(const std::string &path, int index=-1)`. Since we are using Python, the `Sdf` APIs are pythonic so it’s a property instead. To see the full list properties for `Sdf.Layer` and other classes visit the [Sdf module Python documentation](https://docs.omniverse.nvidia.com/kit/docs/pxr-usd-api/latest/pxr/Sdf.html).

## How would I remove a sublayer?

In Python, you would want to use `remove()`. You also need to provide which layer you want to remove. If we were to remove the `shading.usd` layer it would look like this:

```py
root_layer.subLayerPaths.remove("./contents/shading.usd")
```

## How can I find sublayers of a given layer?

Since we already know how to get sublayers of the root layer we can then use that to get the sublayers of those layers. Here’s a snippet on how we can retrieve the sublayers of any layer.

```py
from pathlib import Path
from pxr import Usd, Sdf

working_dir = Path(__file__).parent

stage = Usd.Stage.Open(str(working_dir / "my_skyscraper.usda"))

root_layer: Sdf.Layer = stage.GetRootLayer()
sublayers = root_layer.subLayerPaths
```
