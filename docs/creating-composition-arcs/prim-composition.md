# What Is Prim Composition?

![](../images/composition-arcs/image93.png)

A {term}`prim <Prim>` is the primary container object in USD. It can contain and order other prims or hold different kinds of data.

---

![](../images/composition-arcs/image2.png)

Prims are composed of {term}`prim specs <Prim Spec>` and {term}`property spec <Property Spec>`.

---

![](../images/composition-arcs/image58.png)

Prim specs and  property specs represent data that is authored on {term}`layers <Layer>`. This can be authored on the same layer or on individual layers.

Prim specs and property specs contain {term}`opinions <Opinions>` about what the final composed prim should look like.

Opinions (which is how we will generalize referring to specs for this module) are the authored values that are stored in the prim spec and property spec in a particular layer.

---

![](../images/composition-arcs/image86.png)

Those are combined during {term}`composition <Composition>`.

Knowing that properties can be {term}`attributes <Attribute>` or {term}`relationships <Relationship>`, when talking about property specs you can infer that there are attribute specs and relationship specs.

You can interact with Specs using the [Sdf (Scene Description Foundations) API](https://openusd.org/release/api/class_sdf_spec.html). Both prim spec and property spec have their own API that is based off of `SdfSpec` API.

The image above shows the different parts of the composition. Here we have the rendered result on the left and the USDA file represented on the right. Sphere is  a prim spec, `radius` is a property spec, and the value to the right of `radius` is an opinion.

Now that we understand how prims are composed, let’s dive in deeper to understand how they work.

![](../images/composition-arcs/image98.png)

## What Are Layers?

​​A layer is a single document that's parsable by USD. USD layers are documents such as files or hosted resources, containing prims and {term}`properties <Property>`. For any given layer, these prims and properties are sparsely defined as prim specs and property specs.

### When and Why Do You Use Them?

Projects often have different data producers (teams, users, departments, services, applications, etc.) that would like to collaborate or contribute to the project. We like to refer to these different data sources as workstreams. Workstreams author their respective data to their own USD layers independently, then USD composes the layers into one cohesive project.

Since each workstream authors its data independently of the others, they leverage USD’s core superpower of collaborative, non-destructive editing.

USD layers are also useful to structure USD content in a way that is suitable for optimization features like deferred loading ({term}`payloads <Payload>`) or {term}`instancing <Instancing>`.