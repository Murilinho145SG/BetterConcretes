# Better Concretes 2.1.0 — NeoForge 26.1.2

**Port to Minecraft 26.1.2. Full migration to the new rendering, model and recipe APIs; no feature regressions vs 2.0.0.**

## Added

- Minecraft 26.1.2 / NeoForge 26.1.2.17-beta support (Java 25).
- Server → client recipe sync for the `betterconcretes:chisel` and `betterconcretes:water_transform` types via `OnDatapackSyncEvent` (JEI now receives every recipe cleanly on world join).
- Item definitions (`assets/betterconcretes/items/*.json`) for all 65 items — new 26.1 asset layer required for inventory rendering.

## Changed

- **Connected textures (CTM)** reimplemented on the new 26.1 model pipeline: `CustomUnbakedBlockStateModel` + `DynamicBlockStateModel` with 64 pre-baked states × 6 faces built from `MutableQuad` + `UVTransform`. Visuals preserved vs 2.0.0.
- **Chisel GUI** ported to the new `GuiGraphicsExtractor` pipeline: variant cards, hover / selected / "current variant" feedback, centered variant label, and UI click sound all restored.
- **JEI integration** rewritten for JEI 29.5 API: `IRecipeType`, `CRAFTING_STATION` role, `setStandardSlotBackground` / `setOutputSlotBackground`, arrow moved to `createRecipeExtras`. Chisel now shows as a crafting station on the sidebar instead of a redundant middle slot.
- Chisel recipe category layout cleaned up — arrow no longer overlaps the output slot.
- Block and item registration switched to `DeferredRegister.Blocks` / `DeferredRegister.Items` so `Properties.setId` is called automatically (required by 26.1 to avoid "Block id not set" / "Item id not set" NPEs).
- Recipe data files migrated to the new ingredient codec: `{"item": "X"}` → `"X"` across all 337 recipe JSONs.
- Lang files gained 256 `item.betterconcretes.*_concrete` keys (en_us, pt_br, pt_pt, fr_fr). In 26.1, BlockItem description ids resolve to `item.<modid>.<name>` instead of inheriting the block key.
- Default Gradle heap raised to `-Xmx4G` to accommodate 26.1 dev runs.

## Compatibility notes

- **Not world-compatible** with Better Concretes 2.0.0 (MC 1.21.1). Stay on 2.0.0 for existing 1.21.1 worlds.
- Requires **NeoForge 26.1.2.17-beta+** on Minecraft **26.1.2**.
- JEI 29.5.0.26+ recommended (optional).
