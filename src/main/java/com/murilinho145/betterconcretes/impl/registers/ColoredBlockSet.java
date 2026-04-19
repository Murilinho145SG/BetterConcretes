package com.murilinho145.betterconcretes.impl.registers;

import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.DyeColor;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredRegister;

import java.util.Collection;
import java.util.EnumMap;
import java.util.function.Function;

/**
 * Registers a family of 16 colored blocks (one per {@link DyeColor}) using a name pattern
 * with a {@code {color}} placeholder, e.g. {@code smooth_{color}_concrete}.
 *
 * Each color produces a {@link Block} and a matching {@link BlockItem}, both registered
 * via the supplied {@link DeferredRegister} instances.
 */
public final class ColoredBlockSet {

    private final EnumMap<DyeColor, DeferredHolder<Block, Block>> blocks = new EnumMap<>(DyeColor.class);
    private final EnumMap<DyeColor, DeferredHolder<Item, Item>> items = new EnumMap<>(DyeColor.class);
    private final String namePattern;

    public ColoredBlockSet(
            String namePattern,
            DeferredRegister.Blocks blockRegister,
            DeferredRegister.Items itemRegister,
            Function<DyeColor, BlockBehaviour.Properties> propsFactory
    ) {
        this(namePattern, blockRegister, itemRegister, propsFactory, Block::new);
    }

    public ColoredBlockSet(
            String namePattern,
            DeferredRegister.Blocks blockRegister,
            DeferredRegister.Items itemRegister,
            Function<DyeColor, BlockBehaviour.Properties> propsFactory,
            Function<BlockBehaviour.Properties, Block> blockFactory
    ) {
        this.namePattern = namePattern;
        for (DyeColor color : DyeColor.values()) {
            String name = namePattern.replace("{color}", color.getName());
            DeferredHolder<Block, Block> blockHolder =
                    blockRegister.registerBlock(name, blockFactory::apply, () -> propsFactory.apply(color));
            DeferredHolder<Item, Item> itemHolder =
                    itemRegister.registerItem(name, props -> new BlockItem(blockHolder.get(), props));
            this.blocks.put(color, blockHolder);
            this.items.put(color, itemHolder);
        }
    }

    public Block block(DyeColor color) {
        return blocks.get(color).get();
    }

    public Item item(DyeColor color) {
        return items.get(color).get();
    }

    public String nameFor(DyeColor color) {
        return namePattern.replace("{color}", color.getName());
    }

    public Collection<DeferredHolder<Block, Block>> allBlocks() {
        return blocks.values();
    }

    public Collection<DeferredHolder<Item, Item>> allItems() {
        return items.values();
    }
}
