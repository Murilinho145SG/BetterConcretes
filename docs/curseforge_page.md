# Better Concretes

> 64 new concrete variants across all 16 vanilla colors — smooth, polished, chiseled and brick — plus a custom Chisel tool, dedicated workbench GUI, connected textures on smooth concretes, and full JEI integration.

![BetterConcretes banner](LOGO_BANNER_URL)

---

## What is it

Vanilla concrete comes in 16 colors and exactly one look. **Better Concretes** turns each of those colors into a full building palette:

- **Smooth** — seamless, tileable concrete with connected-textures (CTM) on every face. Build a wall and the seams disappear.
- **Polished** — clean, symmetric slabs with a subtle highlight, for sharp modern architecture.
- **Chiseled** — carved panel with a center detail, for focal points and trim.
- **Brick** — detailed brick pattern with color-true mortar. 16 unique brick styles.

All 64 blocks are part of a single `Better Concretes` creative tab and discoverable through the common `c:concretes` tag, so other mods and datapacks can hook into them without hardcoding our mod id.

![Full palette grid — 4 variants × 16 colors](PALETTE_GRID_URL)

---

## The Chisel

A new iron tool, craftable on a **stonecutter** from a single iron ingot, opens the **Chisel** workbench.

- Drop any Better Concretes block into the input.
- Pick one of the four variants on the right-hand side.
- Pull the output — the Chisel takes a small durability hit and you keep every other aspect of the block: color stays, tag membership stays, inventory slot stays.

Every variant ↔ variant conversion is indexed in **JEI** under the *Chiseling* category, so recipe viewers show the full conversion graph at a glance.

![Chisel tool](CHISEL_HERO_URL)

---

## What's new in 2.0.0

This is a full rewrite and port, not a patch release.

The original **Better Concrete** (singular, Forge 1.20.1) was an 83-line quality-of-life mod with a single feature: concrete powder entities would transform into solid concrete when dropped in water. That mod stays where it is.

**Better Concretes 2.0.0** (plural, **NeoForge 1.21.1**) is a content pack:

- 64 textured blocks with hand-built pixel art at 16×16
- Connected-texture (CTM) rendering on all smooth concretes via a custom `BakedModel`
- Custom `ChiselRecipe` type with its own serializer — datapack-friendly
- 320 JSON chiseling recipes (every variant → every other variant, per color)
- JEI plugin with two categories: `Water Transform` and `Chiseling`
- Common tag support: `c:concretes`, `c:building_blocks`, plus per-color tags
- Full translations for English, Português (BR), Português (PT) and Français
- Stonecutter recipe for the Chisel itself

The modid changed from `betterconcrete` to `betterconcretes`, so this release is **not save-compatible** with the old mod. Worlds relying on `betterconcrete:*` blocks will not port automatically.

---

## Installation

1. Install **NeoForge 21.1.193** for Minecraft **1.21.1**.
2. Drop `betterconcretes-neoforge-1.21.1-2.0.0.jar` into your `mods` folder.
3. Optional but recommended: **JEI 19.22.0.315+** — it unlocks the Chiseling recipe category.

No config file, no runtime registry dances. It just loads.

---

## Compatibility

- **JEI**: Full integration. No JEI installed? The mod still works; you just lose the recipe viewer.
- **Common tags** (`c:concretes`, `c:building_blocks`, `c:{color}_concretes`): other mods can target our blocks without a hard dependency.
- **Chipped / Rechiseled**: no direct integration yet — both mods lack a public chisel-recipe API in 1.21.1. Dedicated bridges may ship as separate addons.

---

## Known items / roadmap

- Port to the next Minecraft version is on the roadmap.
- Slabs and stairs are not included in this release — they would multiply the block count to 256+ and the pack is already a dense content drop. On the backlog.
- Light-source variants (glowing concrete) are being prototyped.

---

## Credits

- **Mod author**: murilinho145
- **Textures**: hand-built procedural pixel art (Python + Pillow), hue-preserved across the 16-color palette.
- **Font / logo**: adapted from the original 1.20.1 project.

---

## License

All Rights Reserved. Modpack inclusion is welcome — please link back to this page and credit the author.
