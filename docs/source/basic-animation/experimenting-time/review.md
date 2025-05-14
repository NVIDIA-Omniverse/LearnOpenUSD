# Review: Experimenting with TimeCode and Timesamples

We just explored the concepts of timeCode and timeSamples. In this module, we:

  * **Identified the attributes in OpenUSD that control timing.** We set timeCodes for our USD stage, establishing a timeline that forms the foundation for our animated scenes.
  * **Demonstrated how to use OpenUSD to create an animation.** We applied timeSamples to individual attributes in our stage to create a simple animation.

Test your knowledge with the following quiz.

:::{quizdown}

## What is a timeCode in OpenUSD?

- [ ] A point in time that specifies the duration of an animation
- [x] A point in time with no specific unit, derived from the stage's <code>timeCodesPerSecond</code>
- [ ] A frame of reference used to control object hierarchy
- [ ] A unit of measurement for object scaling in simulations

## What is a timeSample in OpenUSD used for?

- [ ] To capture the start and end times of an animation sequence
- [x] To store attribute values at specific points in time, allowing animation over time
- [ ] To manage keyframe transitions in complex animation networks
- [ ] To define object shading properties

## What is a limitation of using timeSamples in OpenUSD?

- [ ] TimeSamples cannot be used for any type of animation
- [ ] TimeSamples are a replacement for animation curves in complex animations
- [x] TimeSamples are suited for linear, baked animations but are not ideal for complex animations
- [ ] TimeSamples must be defined using scripting for accurate animation playback
:::