# What Are Model Kinds?

![](../../images/asset-structure/image35.png)

Through composition, OpenUSD can build complex hierarchies of scenes. At the levels of complexity required for a film production shot or a factory line simulation, a single scenegraph can become difficult to navigate for both algorithms and users.

Model hierarchy (also known as *kind* metadata) offers a separate, higher-level view of the underlying scenegraph.

![](../../images/asset-structure/image57.png)
*Model hierarchy is designed to prune traversal at the component model boundary.*

Model hierarchy is designed to prune traversal at a relatively shallow point in the scenegraph. Without it, traversal passes through all prims in your scene, which can be costly. This pruning point is the **component** model boundary. All ancestral prims of component models (when correctly grouped) are part of the model hierarchy, while all descendants are not. 

Let’s talk about two of the specific model kinds, **components** and **assemblies**. This is a refresher of what we discussed in [*Learn OpenUSD: Understanding Model Kinds*](../../beyond-basics/model-kinds.md).

---

## **Component**

![](../../images/asset-structure/image32.png)
The term **component** is often overloaded in many domains. It’s helpful to think of component models as roughly corresponding to consumer facing products. For example, a consumer can purchase a pen, and a consumer can purchase a house. Despite their differences in scale and complexity, both of these would be logical component models in a hierarchy. 

All ancestors of a component model must have their kind metadata set to either a group or a subkind of group, such as assembly. This requirement is primarily to ensure that component discovery is efficient for composition. 

Since the component model kind denotes a “leaf” asset or pruning point in the model hierarchy,  component models cannot contain other component models as descendants. OpenUSD provides the “subcomponent” annotation for important prims that are outside the model hierarchy, which helps facilitate kind-based workflows. Subcomponent prims can contain other subcomponent prims.   
![](../../images/asset-structure/image56.png)
Before we move on to talk about assemblies, take a look at the two examples of model hierarchy above. What makes the first model hierarchy correct? What makes the second model hierarchy incorrect? Can you think of another correct way to organize this model hierarchy? 

---

## **Assembly**

![](../../images/asset-structure/image14.png)
*Assemblies are groups that usually correspond with aggregate assets.*

Assemblies are important groups that usually correspond to aggregate assets. If a house is a component model, then its neighborhood and city could be assembly models. In this example, a neighborhood may contain multiple intermediate group scopes in between the assembly and component for organizational purposes (say grouping trees, street lights, and architecture separately). Assembly models can contain other assembly models, group kinds, and component models.