# Better Concretes 2.0.0 — NeoForge 1.21.1

**First release under the new name. Full rewrite and port from the old Forge 1.20.1 mod.**

## Added

- **64 new blocks**: 4 variants (`smooth`, `polished`, `chiseled`, `brick`) × 16 vanilla colors.
- **Chisel tool**: new iron item, crafted on a stonecutter (1 iron ingot → 1 chisel).
- **Chisel GUI**: wooden workbench UI with 4 variant cards and a single output slot.
- **Connected textures (CTM)** on all smooth concretes — seams disappear on walls and floors.
- **JEI Chiseling category**: shows every variant-to-variant conversion across all 16 colors.
- **JEI Water Transform category**: documents the vanilla concrete powder + water interaction for reference.
- **Common tags**: `c:concretes`, `c:building_blocks`, `c:{color}_concretes` (16 per-color tags) for both blocks and items.
- **Translations**: English, Português (Brasil), Português (Portugal), Français.
- Stonecutter recipe for the Chisel itself.

## Changed

- Modid renamed from `betterconcrete` → `betterconcretes` (reflects the shift from QOL tweak to content pack).
- Jar naming convention: `betterconcretes-neoforge-<mc_version>-<mod_version>.jar`.

## Compatibility notes

- **Not save-compatible** with the old `betterconcrete` 1.20.1 Forge mod. Blocks will not carry over.
- Requires **NeoForge 21.1.193+** on Minecraft **1.21.1**.
- JEI 19.22.0.315+ recommended (optional).

## Fixes vs prior releases

- CTM UV mapping on NORTH/SOUTH faces (previously rendered mirrored).
- Strong colors (red, yellow, cyan) no longer desaturate in the brick variant — HSL shifts replaced the old additive RGB shifts.
- Black brick is now symmetric (previous rng could pick double-dark for the bottom-right sub-brick).
