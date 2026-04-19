# Better Concretes

> 64 new concrete variants across all 16 vanilla colors — smooth, polished, chiseled and brick — plus a custom Chisel tool, dedicated workbench GUI, connected textures on smooth concretes, and full JEI integration.

[![MC](https://img.shields.io/badge/Minecraft-26.1.2-62B47A?logo=minecraft&logoColor=white)](https://www.minecraft.net)
[![NeoForge](https://img.shields.io/badge/NeoForge-26.1.2.17--beta-D35400)](https://neoforged.net)
[![JEI](https://img.shields.io/badge/JEI-29.5.0.26-3498DB)](https://modrinth.com/mod/jei)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## What is it

Vanilla concrete comes in 16 colors and exactly one look. **Better Concretes** turns each of those colors into a full building palette:

- **Smooth** — seamless, tileable concrete with connected-textures (CTM) on every face. Build a wall and the seams disappear.
- **Polished** — clean, symmetric slabs with a subtle highlight, for sharp modern architecture.
- **Chiseled** — carved panel with a center detail, for focal points and trim.
- **Brick** — detailed brick pattern with color-true mortar. 16 unique brick styles.

All 64 blocks are part of a single `Better Concretes` creative tab and discoverable through the common `c:concretes` tag, so other mods and datapacks can hook into them without hardcoding our mod id.

---

## The Chisel

A new iron tool, craftable on a **stonecutter** from a single iron ingot, opens the **Chisel** workbench.

- Drop any Better Concretes block into the input.
- Pick one of the four variants on the right-hand side.
- Pull the output — the Chisel takes a small durability hit and you keep every other aspect of the block: color stays, tag membership stays, inventory slot stays.

Every variant ↔ variant conversion is indexed in **JEI** under the *Chiseling* category, so recipe viewers show the full conversion graph at a glance.

Right-clicking a Better Concretes block directly with the Chisel in hand cycles to the next variant in place — no GUI needed for quick edits.

---

## Installation

1. Install **NeoForge 26.1.2.17-beta+** for Minecraft **26.1.2** (Java 25).
2. Drop `betterconcretes-neoforge-26.1.2-2.1.0.jar` into your `mods` folder.
3. Optional but recommended: **JEI 29.5.0.26+** — it unlocks the Chiseling and Water Transform recipe categories.

No config file, no runtime registry dances. It just loads.

---

## Compatibility

- **JEI**: Full integration — the Chisel appears as a crafting station on the sidebar and every chiseling recipe is indexed.
- **Common tags** (`c:concretes`, `c:building_blocks`, `c:{color}_concretes`): other mods can target our blocks without a hard dependency.
- Not save-compatible with Better Concretes **2.0.0** (MC 1.21.1) — stay on 2.0.0 for existing 1.21.1 worlds.

---

## Building from source

```bash
git clone https://github.com/Murilinho145SG/BetterConcretes.git
cd BetterConcretes
./gradlew build
```

The jar lands in `build/libs/betterconcretes-neoforge-26.1.2-<version>.jar`.

To run a dev client: `./gradlew runClient`.

---

## Version history

- **2.1.0** — MC 26.1.2 / NeoForge 26.1.2.17-beta port. Full migration to the new model, recipe and screen APIs. Features preserved vs 2.0.0. See [changelog](docs/curseforge_changelog_2.1.0.md).
- **2.0.0** — First release under `betterconcretes`, NeoForge 1.21.1. 64 blocks, Chisel tool, CTM, JEI. See [changelog](docs/curseforge_changelog_2.0.0.md).

---

## Contributing

Issues and PRs welcome — see [CONTRIBUTING.md](CONTRIBUTING.md). By participating you agree to the [Code of Conduct](CODE_OF_CONDUCT.md).

---

## Credits

- **Mod author**: [murilinho145](https://github.com/Murilinho145SG)
- **Textures**: hand-built procedural pixel art (Python + Pillow), hue-preserved across the 16-color palette.

---

## License

[MIT](LICENSE). Modpack inclusion is welcome — attribution appreciated but not required.
