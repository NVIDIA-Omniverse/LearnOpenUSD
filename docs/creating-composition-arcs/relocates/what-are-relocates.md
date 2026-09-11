# Relocates

## What Are Relocates?

When you {term}`reference <Reference>` an {term}`asset <Asset>`, its children arrive in your scene under the referencing {term}`prim <Prim>`. Those children are real prims on the {term}`stage <Stage>`, but you never authored them in your {term}`layer <Layer>` — they appear only as a result of {term}`composition <Composition>`.

That distinction matters the moment you want to rename or move one of them. A prim you authored locally can be renamed by editing your own layer. A prim that arrived across a composition arc cannot: its name lives in the source asset, and editing that asset would change it for every other consumer.

{term}`Relocates <Relocate>` solve exactly this problem. A relocate is a rule, recorded in layer {term}`metadata <Metadata>`, that maps the path where a prim *would* appear to the path where you want it in this {term}`layer stack <Layer Stack>`. The source asset is untouched, and every other scene that references it is unaffected.

You author relocates as a dictionary in layer metadata, mapping source path to target path:

```usda
#usda 1.0
(
    relocates = {
        </World/StreetLamp/lamp_grp_v2_FINAL>: </World/StreetLamp/geometry>
    }
)
```

Only prim paths participate. {term}`Attributes <Attribute>` and {term}`relationships <Relationship>` are not relocated — a relocate moves a prim and everything beneath it, but you cannot use one to move a single property.

```{note}
Relocates are the "E" in {term}`LIVERPS <LIVERPS Strength Ordering>` — for "rElocates". They sit between variant sets and references in strength order, which is why the mnemonic changed from LIVRPS to LIVERPS.
```

## When and Why Do You Use Them?

Relocates let you rename or reparent prims that arrive through composition arcs without destructively editing the source layer. That is useful when:

- The prim lives in a referenced asset you do not own or do not want to modify.
- Your pipeline has naming conventions that the incoming asset does not follow.
- You want a cleaner {term}`namespace <Namespace>` for downstream scene organization, but still want to keep consuming the asset as delivered.

The common thread is that you need local namespace control while preserving asset reuse.

## Renaming in Place

The simplest use is a rename. Here, a vendor's lamp asset exposes its geometry under a working name that leaked out of the DCC it was built in:

```usda
def Xform "LampAsset"
{
    def Xform "lamp_grp_v2_FINAL"
    {
        def Cylinder "pole" { }
        def Sphere "bulb" { }
    }
}
```

Referencing that asset and relocating the child gives you the name you want:

```usda
#usda 1.0
(
    defaultPrim = "World"
    relocates = {
        </World/StreetLamp/lamp_grp_v2_FINAL>: </World/StreetLamp/geometry>
    }
)

def Xform "World"
{
    def Xform "StreetLamp" (
        prepend references = @./lamp_asset.usd@
    )
    {
    }
}
```

The composed stage now shows `/World/StreetLamp/geometry`, with `pole` and `bulb` beneath it. The `lamp_asset.usd` file on disk is unchanged.

## Reparenting Across the Hierarchy

A relocate target does not have to stay under the same parent. You can lift a composed prim out of the subtree it arrived in and graft it somewhere else in the same layer stack.

Suppose a city block asset ships its buildings and its landmark together, but your pipeline tracks landmarks in a separate group so lighting can work on them independently:

```usda
#usda 1.0
(
    defaultPrim = "World"
    relocates = {
        </World/District_01/clock_tower>: </World/Landmarks/clock_tower>
    }
)

def Xform "World"
{
    def Xform "District_01" (
        prepend references = @./block_asset.usd@
    )
    {
    }

    def Xform "Landmarks"
    {
    }
}
```

After composition, `clock_tower` resolves at `/World/Landmarks/clock_tower`. It is no longer a child of `District_01`, even though that is the prim carrying the reference.

## Removing a Prim

Relocating a prim to an empty path removes it from the composed stage. This is how you drop scaffolding that an asset ships but your scene does not need:

```text
relocates = {
    </World/Sign_01/tmp_rig_helper>: <>
}
```

This is a composition-time removal, not a {term}`deactivation <Active and Inactive>`. The prim never appears on the stage at all.

## Constraints Worth Knowing

Relocates come with rules, and two of them cause most of the confusion.

**You can only relocate a prim introduced by a composition arc.** A prim defined directly in your own layer stack is yours to rename by editing it. If you write a relocate whose source is a locally-defined prim, the relocate does not apply.

```{caution}
A relocate with a locally-defined source prim does not raise a composition error — the prim is simply dropped from the composed stage, and the target is never created. If a prim disappears after you add a relocate, check that its source path really does come from a reference or payload.
```

**The source path stops being a valid place to author.** Once a relocate is in effect, the old path no longer exists on the stage. Any {term}`opinion <Opinions>` you author there is ignored:

```usda
over "StreetLamp"
{
    over "lamp_grp_v2_FINAL"   # ignored — this path was relocated away
    {
        double size = 99
    }
}
```

USD does warn about this one:

```text
In </World/StreetLamp/geometry>: The layer @relocates_simple.usd@ has an invalid
opinion at the relocation source path </World/StreetLamp/lamp_grp_v2_FINAL>,
which will be ignored.
```

After a relocate, author against the target path instead.

```{seealso}
For the full set of rules, see [Relocates](inv:usd:std#glossary:relocates) in the OpenUSD glossary.
```
