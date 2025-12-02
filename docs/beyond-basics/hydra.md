# Hydra

In this lesson, we'll explore {term}`Hydra <Hydra>`, a powerful rendering architecture within OpenUSD. Understanding Hydra enables efficient and flexible rendering of complex 3D scenes.

## What Is Hydra?

```{kaltura} 1_aggsw6zi
```

Hydra is a rendering architecture within OpenUSD that provides a high-performance, scalable, and extensible solution for rendering large 3D scenes. It serves as a bridge between the scene description data, such as USD, and the rendering backend, such as OpenGL or DirectX.

The open and extensible nature of Hydra means it supports many different renderers, like Arnold and Renderman, and OpenUSD's included HdStorm renderer offers a simple way for developers to visualize data out of the box.

Hydra has three main parts:

* A scene delegate, which provides the scene information
* The render {term}`index <Index>`, which keeps track of changes and manages the scene
* The render delegate, which uses the render index and scene delegate to visualize scene information to create the final image.

### How Does It Work?

Hydra operates on one or more scene delegates, which is a hierarchical representation of the scene data. It processes the scene delegates into an abstract renderable scene, which render delegates can use to generate rendering instructions tailored for the specific rendering backend. This approach decouples the scene data from the rendering backend, allowing for flexibility and extensibility.

Hydra supports various render delegate plugins, enabling developers to create custom rendering backends or extend existing ones. OpenUSD ships with HdStorm, the real-time OpenGL/Metal/Vulkan render delegate leveraged by usdview and many other tools. It also ships with HdTiny and HdEmbree, which can be used as
examples of how to implement render delegates.

## Key Takeaways

Understanding Hydra enables efficient and flexible rendering of complex 3D scenes. Now, we know that:

* Hydra is a rendering architecture within OpenUSD that bridges scene data and rendering backends.
* It operates on a scene delegate and enables render delegate plugins to generate rendering instructions for specific backends.
* Hydra supports various rendering backends and techniques, including rasterization and ray tracing.
* It provides extensibility through plugins and custom rendering backends.

With its support for various rendering techniques, extensibility, and decoupling of scene data from rendering backends, Hydra empowers users to create work in large scenes. We encourage you to explore Hydra further and leverage its capabilities in your OpenUSD projects.



