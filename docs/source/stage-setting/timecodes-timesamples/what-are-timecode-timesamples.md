# What are TimeCode and Time Samples?

![TimeCode Time Sample Definition](../../images/TimeCodeTimeSample_Definition.webm){loop autoplay controls}
:::{video} ../../images/TimeCodeTimeSample_Definition.webm
:::

In OpenUSD, timeCode and timeSample are two important concepts that enable us
to work with animations and simulation in USD scenes.

TimeCode is a point in time with no unit assigned to it. You can think of
these as frames whose units are derived from the stage.

TimeSample refers to the individual time-varying values associated with an
attribute in USD. Each attribute can have a collection of timeSamples that map
timeCode to the attribute's data type values, allowing for animation over
time.



### How Does It Work?

In a USD scene, the timeCode ordinates of all timeSamples are scaled to
seconds based on the `timeCodesPerSecond` metadata value defined in the root
layer.

This allows flexibility in encoding timeSamples within a range and scale
suitable for the application, while maintaining a robust mapping to real-world
time for playback and decoding.

For example, if the root layer has `timeCodesPerSecond=24`, a timeCode value
of `48.0` would correspond to 2 seconds (48/24) of real time after the
timeCode `0`.

TimeSamples are used to store time-varying data for attributes, such as
positions, rotations, or material properties. When an attribute is evaluated
at a specific timeCode, the value is linearly interpolated from the
surrounding timeSamples, allowing for smooth animation playback.



### Working With Python

![TimeCode TimeSample Python](../../images/TimeCodeTimeSample_Python.webm)

Below is an example of how we can get or set timeSamples in Python. First,
we're getting the timeSamples of the `DisplayColor` on a cube prim. This
method returns a vector of timeCode ordinates at which time samples are
authored for the given attribute.

Lastly, we're setting a translation value of a sphere at a specified timeCode.
This method sets the timeSample value of the attribute at the specified
timeCode.

```python
# Returns authored TimeSamples
cube.GetDisplayColorAttr().GetTimeSamples()

# Sets TimeSample Value (Gf.Vec3d(0,-4.5,0)) at a specified TimeCode (30)
sphere_xform_api.SetTranslate(Gf.Vec3d(0,-4.5,0), time=Usd.TimeCode(30))
```


### Key Takeaways

To sum it up, timeCode provides a unitless time ordinate scaled to real-world
time, while timeSample stores the actual attribute values at specific timeCode
ordinates. Understanding these concepts unlocks a way for creating, manipulating, and rendering dynamic scenes and simulations in OpenUSD-based
workflows across various industries.



