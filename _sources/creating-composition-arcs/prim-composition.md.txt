# What Is Prim Composition?

![](../images/composition-arcs/image93.png)

A prim is the primary container object in USD. It can contain and order other prims or hold different kinds of data.

---

![](../images/composition-arcs/image2.png)

Prims are composed of `primSpecs` and `propertySpecs`.

---

![](../images/composition-arcs/image58.png)

`PrimSpecs` and `propertySpecs` represent data that is authored on layers. This can be authored on the same layer or on individual layers.

`PrimSpecs` and `propertySpecs` contain opinions about what the final composed prim should look like.

Opinions (which is how we will generalize referring to Specs for this module) are the authored values that are stored in the `primSpec` and `propertySpec` in a particular layer.

---

![](../images/composition-arcs/image86.png)

Those are combined during composition.

Knowing that properties can be attributes or relationships, when talking about `propertySpecs` you can infer that there are `attributeSpecs` and `relationshipSpecs`.

You can interact with Specs using the [Sdf (Scene Description Foundations) API](https://openusd.org/release/api/class_sdf_spec.html). Both `primSpec` and `propertySpec` have their own API that is based off of SdfSpec API.

The image above shows the different parts of the composition. Here we have the rendered result on the left and the USDA file represented on the right. Sphere is  a `primSpec`, `radius` is a `propertySpec`, and the value to the right of `radius` is an opinion.

Now that we understand how prims are composed, let’s dive in deeper to understand how they work.

![](../images/composition-arcs/image98.png)

## What Are Layers?

​​A layer is a single document that's parsable by USD. USD layers are documents such as files or hosted resources, containing prims and properties. For any given layer, these prims and properties are sparsely defined as `primSpecs` and `propertySpecs`.

### When and Why Do You Use Them?

Projects often have different data producers (teams, users, departments, services, applications, etc.) that would like to collaborate or contribute to the project. We like to refer to these different data sources as workstreams. Workstreams author their respective data to their own USD layers independently, then USD composes the layers into one cohesive project.

Since each workstream authors its data independently of the others, they leverage USD’s core superpower of collaborative, non-destructive editing.

USD layers are also useful to structure USD content in a way that is suitable for optimization features like deferred loading (Payloads) or instancing.