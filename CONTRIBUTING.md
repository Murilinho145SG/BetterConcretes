# Contributing to Better Concretes

Thanks for your interest in contributing. This document covers how to report bugs, propose features, and submit code.

## Ground rules

- Be kind. Everyone is bound by the [Code of Conduct](CODE_OF_CONDUCT.md).
- One issue or PR = one concern. Keep changes focused.
- If you're unsure whether a change fits, open an issue first to discuss — it saves everyone time.

## Reporting bugs

Open an issue at [github.com/Murilinho145SG/BetterConcretes/issues](https://github.com/Murilinho145SG/BetterConcretes/issues) and include:

- **Minecraft version** and **NeoForge version** (from `.minecraft/logs/latest.log`, first few lines).
- **Mod version** you're running (the jar filename).
- **Other mods** in the profile (a `crash-reports/` file or full mod list helps if it's a conflict).
- **Steps to reproduce** — the smallest world / item / action sequence that triggers it.
- **Expected vs actual behaviour**.
- A **crash report** or screenshot if applicable (paste as a code block or gist, not a screenshot of text).

JEI-only issues (recipe not showing, category looks wrong) are useful — say JEI version too.

## Feature requests

Open an issue tagged with the intended scope:

- **Content** — new variants, new tools, new categories.
- **Integration** — interop with other mods (Chipped, Create, etc.).
- **Quality of life** — right-click hotkeys, config knobs, datapack hooks.

Large content additions (e.g. slabs & stairs for every variant) need an alignment discussion before code lands — they balloon the block count and affect load times.

## Submitting code

### Local setup

```bash
git clone https://github.com/Murilinho145SG/BetterConcretes.git
cd BetterConcretes
./gradlew build          # produce the jar
./gradlew runClient      # launch a dev client
```

Requires JDK 25 (Mojang ships Java 25 in MC 26.1+).

### Branch and commit style

- Branch from `main`. Name it something searchable: `fix/jei-arrow-overlap`, `feat/slabs`, `docs/readme-badges`.
- Commit messages follow imperative mood: `Fix ...`, `Add ...`, `Port ...`.
- Keep commits atomic. If a change is really two things, make it two commits.

### PR checklist

Before opening a PR:

- [ ] `./gradlew compileJava` passes cleanly — no new warnings.
- [ ] `./gradlew runClient` boots the mod without errors in `run/logs/latest.log`.
- [ ] New user-facing strings have `en_us` entries (other locales are welcome but optional).
- [ ] New blocks/items have corresponding model JSONs, blockstates, and `assets/<modid>/items/` definitions.
- [ ] If you touched recipe codecs, data-files under `data/betterconcretes/recipe/` still parse.
- [ ] Any new public API surface has a one-line comment explaining non-obvious decisions (no narration).

### Code style

- Java 21 features are OK (pattern matching, records, switch expressions).
- Minecraft/NeoForge conventions over Java conventions when they clash (e.g. `Identifier` not `ResourceLocation` in 26.1+).
- No emojis in code or commit messages.
- Don't add Javadoc unless the behaviour is truly non-obvious — identifier names should carry the meaning.
- Don't commit IDE files (`.idea/`, `*.iml`) — `.gitignore` already covers them.

### Tests

There's no automated test suite yet. If you add one (JUnit, NeoForge gametest), it's very welcome — drop it under `src/test/java/` and wire it into `./gradlew test`.

## Content additions (textures, translations)

- **Textures**: 16×16 pixel art, hue-preserved across the 16 vanilla colors. The pipeline that generated the current set lives under `tools/` — there are Python scripts that take a base greyscale master and reproject it across the vanilla palette. Use them or replicate their output size/style.
- **Translations**: lang files live at `src/main/resources/assets/betterconcretes/lang/<locale>.json`. Copy `en_us.json` as a starting point. New locales are always welcome.

## Releasing

Maintainers only:

1. Bump `mod_version` in `gradle.properties`.
2. Write `docs/curseforge_changelog_<version>.md`.
3. `./gradlew clean build`.
4. Tag: `git tag v<version> && git push --tags`.
5. Publish the jar to CurseForge / Modrinth.

## Questions

If something is unclear, open a [discussion](https://github.com/Murilinho145SG/BetterConcretes/discussions) rather than a PR — saves rework.
