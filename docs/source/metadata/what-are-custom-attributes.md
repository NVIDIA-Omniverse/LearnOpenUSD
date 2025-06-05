Now, let's explore the concept of custom attributes in Universal Scene Description. Understanding custom attributes is essential for tailoring OpenUSD assets and workflows to specific needs, enabling more flexible and detailed scene descriptions.

Custom attributes in OpenUSD are user-defined properties that can be added to prims (the basic building blocks in OpenUSD) to store additional data. Unlike schema attributes, which are predefined and standardized, custom attributes allow users to extend the functionality of OpenUSD at runtime to suit their specific requirements.

### How Does It Work?

#### Custom schemas vs. custom attributes

Custom schemas are a more advanced topic that we’ll cover in future lessons, but let’s compare the two briefly. When considering custom attributes versus custom schemas, the main strengths of custom attributes are their ease of use, and ability to be defined at any time, by any type of user. The main strengths
of custom schemas are their ability to group related information, and provide standardization.

For instance, consider we’re creating a web page for ordering a cake. One approach would be to create a single large, scrollable text field that we can assign a label to, like “What kind of cake do you need”, and let the user enter whatever they want in it.

Another approach might be to create a form with multiple fields, each of which is designed to store a very specific piece of information: what kind of cake, what type of icing, what size, if they want sprinkles, what should be written on top...

The first approach, the single text field, is similar to custom attributes. It allows the user to decide the information they want to enter. It’s also easier--if you’re new to working with USD, or need to implement custom fields very quickly, this might be the way to go.

On the other hand, custom schemas allow us to define a group of data in a more standardized way. However, it requires more planning and consideration, what fields we collect are predefined, and it takes longer to implement.

---

With that, let’s get back to our lesson on custom attributes.

Custom attributes are created and managed using the USD API. They can hold various types of data, such as numeric values, strings, or arrays, and can be sampled over time. This flexibility makes them useful for a wide range of applications, from simple metadata storage to complex animations.

Here are a few ways we can use custom attributes to enhance our OpenUSD workflows:

* **Metadata storage** : Storing additional information about a prim, such as author names, creation dates, or custom tags. 
* **Animation data** : Defining custom animation curves or parameters that are not covered by standard schema attributes.
* **Simulation parameters** : Storing parameters for physics simulations or other procedural generation processes. 
* **Arbitrary end user data** : Because they can be easily defined at run time, custom attributes are the best way to allow end users to define arbitrary custom data.

Custom attributes are the easiest and most flexible way to adapt OpenUSD to specific workflows and requirements, making it a powerful tool for industries like manufacturing, product design, architecture, and engineering, wherever we have multiple data types from many sources with varying purposes--like connecting our OpenUSD to sensor data or IoT for live, connected digital twins, or creating a production model with attributes like part numbers, manufacturer, life cycle costs, and even carbon data that can sync 3D scene description to 2D project documents, like a bill of materials or carbon emission calculators.

### Working With Python

![Custom Attribute Python](../../images/CustomAttribute_Python.webm)

Here’s an example where we’re creating a custom attribute to add a serial number and last maintenance date to a prim, so a supervisor can easily identify which machines are due for maintenance from the 3D model.

```python
stage = Usd.Stage.CreateInMemory()
prim = stage.DefinePrim("/ExamplePrim", "Xform")
serial_num_attr = prim.CreateAttribute("serial_number", Sdf.ValueTypeNames.String)

assert serial_num_attr.IsCustom()

mtce_date_attr = prim.CreateAttribute("maintenance_date", Sdf.ValueTypeNames.String)
serial_num_attr.Set("qt6hfg23")
mtce_date_attr.Set("20241004")

print(f"Serial Number: {serial_num_attr.Get()}")
print(f"Last Maintenance Date: {mtce_date_attr.Get()}")`
```

### Key Takeaways

Custom attributes in OpenUSD provide a versatile way to extend the
functionality of scene descriptions, making them adaptable to various specialized needs. By understanding how to create, set, and retrieve custom attributes, we can enhance our OpenUSD workflows and better manage complex data in our projects, significantly improve the precision and efficiency of digital models, and build USD pipelines that are tailored to specific use
cases.



