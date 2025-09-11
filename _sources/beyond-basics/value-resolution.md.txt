# Value Resolution

## What Is Value Resolution?

![Value Resolution Definition](../images/foundations/ValueResolution_Defintion.webm)

Value resolution is how OpenUSD figures out the final value of a property or piece of metadata by looking at all the different sources that might have information about it. Think of it like solving a puzzle where you have multiple pieces of information from different places, and you need to figure out what the final answer should be.

Even though value resolution combines many pieces of data together, it's different from composition. Understanding this difference helps you work with USD more effectively.

```{note}
Animation splines were recently added to OpenUSD and are also part of value resolution. We'll update this lesson to include them soon.
```

## How Does It Work?

### Key Differences Between Composition and Value Resolution

1. **Composition is cached, value resolution is not**

   When you open a stage or add new scene data, USD creates an "index" of the composition logic and result at the prim-level for quick access. However, USD doesn't pre-calculate the final values of properties. This keeps the system fast and uses less memory.

   ```{tip}
   If you need to get the same attribute value many times, you can use special tools like `UsdAttributeQuery` to cache this information yourself.
   ```

2. **Composition rules vary by composition arc, value resolution rules vary by data type**

   Composition figures out where all the data comes from and creates an index of sources for each prim. Value resolution then takes this ordered list (from strongest to weakest) and combines the opinion data according to what type of information it is.

### Resolving Different Types of Data

#### Resolving Metadata

For most metadata, the rule is simple: **the strongest opinion wins**. Think of it like a voting system where the most authoritative source gets the final say.

Some metadata like prim specifier, attribute typeName, and several others have special resolution 
rules. A common metadata type you may encount with special resolution rules are dictionaries (like `customData`). Dictionaries combine element by element, so if one layer has `customData["keyOne"]` and another has `customData["keyTwo"]`, the final result will have both keys.

#### Resolving Relationships

Relationships work differently because they can have multiple targets. Instead of just picking the strongest opinion, USD combines all the opinions about what the relationship should point to, following specific rules for how to merge lists (i.e. list ops).

#### Resolving Attributes

Attributes are special because they have three possible sources of values at each location:

1. **Value Clips** - Animation data stored in separate files
2. **TimeSamples** - Specific values at specific times
3. **Default Value** - A non-time-varying value

Value resolution of attributes in the first two cases also account for time scaling and offset operators (e.g. Layer Offsets) and interpolation for time codes that fall between two explicit timeSamples.

## Working With Python

```python
from pxr import Usd, UsdGeom

# Open a stage
stage = Usd.Stage.Open('example.usd')

# Get a prim
prim = stage.GetPrimAtPath('/World/MyPrim')

# Get an attribute
attr = prim.GetAttribute('myAttribute')
# Usd.TimeCode.Default() is implied
default_value = attr.Get()
# Get the value at time code 100.
animated_value = attr.Get(100)
# Use EarliestTime to get earliest animated values if they exist
value = attr.Get(Usd.TimeCode.EarliestTime())
```

When you get an attribute value without an explicit time code, the default time code (`UsdTimeCode::Default()`) is usually not what you want if your stage has animation. Instead, use `UsdTimeCode::EarliestTime()` to make sure you get the actual animated values rather than just the default value.

## Key Takeaways

Value resolution gives OpenUSD its powerful ability to combine data from multiple sources while keeping the system fast and efficient.

This is incredibly useful in real-world workflows. For example, imagine multiple teams working on different parts of a scene - value resolution seamlessly combines everyone's work into a single model without anyone's contributions being lost.

Here's a concrete example with a robot arm:

* The base layer defines the robot arm's default position at `(0, 0, 0)`
* The animation layer overrides this to move the arm to `(5, 0, 0)` during operation

During value resolution, OpenUSD combines these layers, resulting in the robot arm being positioned at `(5, 0, 0)` while keeping all other unchanged properties from the base layer.

Understanding value resolution is key to working effectively with OpenUSD's non-destructive workflow and getting the best performance in multi-threaded applications.



