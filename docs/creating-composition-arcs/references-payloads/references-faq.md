# References Frequently Asked Questions

Let’s take some time to ask some common questions when it comes to working with {term}`references <Reference>`.

## Why not add these as sublayers? Why add them as references?

This depends on two things, the contents of the {term}`layers <Layer>` and what you will need to do with the resulting {term}`composition <Composition>`. Since we are adding `skyscraperA` twice, if added as a {term}`sublayer <Sublayer>` then the first sublayer would overwrite the second `skyscraperA` instead of adding a second skyscraper. For more information on when to use sublayers vs references visit this site: [USD Frequently Asked Questions](https://openusd.org/release/usdfaq.html#i-have-some-layers-i-want-to-combine-should-i-use-sublayers-or-references)

Sublayers are like including, but referencing is like grafting.

## Why prepend?

You may have noticed the prepend operation in the reference statement above. Prepend means that, when this layer is composed with others to populate the {term}`stage <Stage>`, the reference will be inserted before any references that might exist in weaker sublayers. This ensures that the contents of the reference will contribute stronger {term}`opinions <Opinions>` than any reference arcs that might exist in other, weaker layers.

In other words, prepend gives the intuitive result you’d expect when you apply one layer on top of another. This is what the [UsdReferences](https://openusd.org/release/api/class_usd_references.html) API will create by default. You can specify other options with the position parameter, but this should rarely be necessary.