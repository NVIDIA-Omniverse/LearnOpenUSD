There are two types of schemas used with OpenUSD: IsA schemas and API schemas. Let’s talk about IsA schemas first.

---

### IsA Schemas

IsA schemas, also known as Typed schemas or Prim schemas, essentially tell a prim what it is. Because of this, each prim can only subscribe to one IsA schema at a time.

We use the `typeName` metadata to assign an IsA schema to a prim.  

IsA schemas are derived from the core class `UsdTyped`, the base class for all typed schemas, which is why we hear IsA schemas referred to as “typed” schemas.

These schemas can either be concrete (instantiable) or abstract (non-concrete, serve as base classes). We refer to a schema as concrete when the schema can be instantiated as prims in the USD scene, as we see with `UsdGeomMesh` and `UsdGeomScope`. Concrete schemas provide both a name and a typeName in the schema definition.

Meanwhile, abstract, or non-concrete schemas, provide a name but no typeName in the schema definition. This enables them to serve as a base class for related sets of concrete schemas, the way `UsdGeomPointBased` serves as a base class for geometric objects that contain points, like meshes (`UsdGeomMesh`), or basis curves (`UsdGeomBasisCurves`).

Let’s look at a couple of the common default schemas that will come up as we are learning about OpenUSD.

#### UsdGeom

![Schema USDGeom](../../images/Schema_UsdGeom.webm)

`UsdGeom` defines schemas for representing geometric objects, such as meshes, cameras, and curves as mentioned above. It also includes schemas for transformations, visibility, and other common properties.

```python
# Import related classes
from pxr import UsdGeom

# Define a sphere in the stage
sphere = UsdGeom.Sphere.Define(stage, "/World/Sphere")
	
# Get and Set the radius attribute of the sphere
sphere.GetRadiusAttr().Set(10)
```

#### UsdLux

![Schema UsdLux](../../images/Schema_UsdLux.webm)

`UsdLux` defines schemas for representing light sources in a scene. It includes schemas such as sphere lights, disk lights, and distant lights, which were discussed in the lesson on USD lights.

Examples include `UsdLuxDiskLight`, `UsdLuxRectLight`, and
`UsdLuxSphereLight`.

```python
# Import related classes
from pxr import UsdLux

# Define a disk light in the stage
disk_light = UsdLux.DiskLight.Define(stage, "/World/Lights/DiskLight")
	
# Get all Attribute names that are a part of the DiskLight schema
dl_attribute_names = disk_light.GetSchemaAttributeNames()
	
# Get and Set the intensity attribute of the disk light prim
disk_light.GetIntensityAttr().Set(1000)
```

### API Schemas

In addition to IsA schemas, we have API schemas. API schemas are similar to IsA schemas except it does not specify a typeName. Since it does not have a typeName they are considered to be non-concrete.

API schemas are typically named with the suffix “API” in their C++ or Python class name, such as `UsdShadeConnectableAPI`. Properties that belong to an API schema are namespaced with the schemas base name and camelCased. For example, `UsdPhysics.RigidBodyAPI.CreateVelocityAttr()` will create an attribute named `physics:velocity`.

API schemas can be classified as non-applied or applied schemas, and single-apply or multiple-apply, where single-apply API schemas are applied to only a single instance of a prim, and multiple-apply API schemas can be applied multiple times to the same prim with different instance names.

Unlike IsA schemas, API schemas do not assign a typeName to a prim. Instead, are list-edited in the `apiSchemas` metadata and queryable via the `HasAPI` method. API schemas are assigned to already-typed prims to annotate them with additional properties that govern behaviors.

The following is a key example of an API Schemas.

#### UsdPhysicsRigidBodyAPI

![Schema UsdPhysics](../../images/Schema_UsdPhysics.webm)

`UsdPhysicsRigidBodyAPI` adds physics properties to any `UsdGeomXformable` object for simulation such as rigid body dynamics.

```python
# Import related classes
from pxr import UsdPhysics

# Apply a UsdPhysics Rigidbody API on the cube prim
cube_rb_api = UsdPhysics.RigidBodyAPI.Apply(cube.GetPrim())
	
# Get the Kinematic Enabled Attribute 
cube_rb_api.GetKinematicEnabledAttr()
	
# Create a linear velocity attribute of value 5
cube_rb_api.CreateVelocityAttr(5)
```

This example shows how API schemas can be applied to prims to add specific properties that govern behaviors, such as adding rigid body capabilities to an object hierarchy.



### Key Takeaways

API schemas work alongside IsA schemas to provide a flexible and extensible system for building complex scenes in OpenUSD.

Schemas are a complex topic, but when leveraged correctly, they can simplify development of USD scenes. We’ll cover schemas again, including custom schemas, in future lessons.



