# What Is Asset Validation?

![](../../images/data-exchange/image20.png)

Typical unit tests and automated testing of your data exchange implementation are encouraged, but you shouldn't stop there. You might be learning OpenUSD as you're developing. How do you know that you are authoring good quality and compliant USD content? That's where usdchecker comes in.

usdchecker is one of the tools that comes as part of the USD Toolset, the command-line tools included with OpenUSD. usdchecker can validate a USD {term}`stage <Stage>` or USDZ package using a set of defined rules to provide the best assurance that an {term}`asset <Asset>` will be properly interchangeable and renderable by {term}`Hydra <Hydra>`.

## Omniverse Asset Validator

![](../../images/data-exchange/image29.png)

Omniverse Asset Validator is based on usdchecker and provides a GUI for asset validation. The asset validator includes:

- User interface
- Command line interface
- Python API
- Automatic fixes for failed validations
- Ability to add new rules