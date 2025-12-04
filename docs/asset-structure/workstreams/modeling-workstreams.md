# Modeling Workstreams With Layer Stacks

Products developed by organizations rarely consist of a single file. Instead, work is organized into logical, maintainable units. Similarly, {term}`assets <Asset>` should model workstreams into {term}`layers <Layer>`.

## User Workstreams

![](../../images/asset-structure/image15.png)

Simple assets can be represented by a single layer, and it may make sense to start there for the sake of simplicity.

However, when different tools, users, and departments are responsible for contributing different {term}`prims <Prim>` to the final composed asset scene graph (such as geometry and materials), it can be beneficial to split the workstreams into multiple layers.

Splitting workflows into parallel streams can offer performance benefits. For example, one content creator can work on the geometry layer while another iterates on the material layer, reducing storage needs and publishing time.

Even if a single user is working on both geometry and materials, it can be helpful to separate the contributions from each application into different layers if they are using different tools for each workstream. This allows each workstream to be tracked as a separate product. Ideally, each workstream should only author its unique contributions sparsely, rather than needlessly overwriting work done by another workstream.

## Computational Workstreams

![](../../images/asset-structure/image11.png)
Assets can also be divided into **computational workstreams**. For instance, a synthetic data simulation might be partitioned across multiple processes or machines. A {term}`layer stack <Layer Stack>` can then be used to stitch the results back together.

![](../../images/asset-structure/image22.png)
Computational workstreams can be dynamic and may not remain consistent from one evaluation to the next. Consider a layer stack where workloads have been dynamically partitioned across multiple processes.

![](../../images/asset-structure/image42.png)
Some workstreams are **hybrids**, combining both computational and user-driven elements. For example, a layer might contribute synthesized motion on top of a hand-authored initial state created by a user.

![](../../images/asset-structure/image51.png)
It's important to keep layer stacks simple and manageable. They are not a replacement for asset versioning systems. Avoid modeling workstreams in layer stacks that might grow procedurally over time, as there is a cost associated with resolving and opening each layer.