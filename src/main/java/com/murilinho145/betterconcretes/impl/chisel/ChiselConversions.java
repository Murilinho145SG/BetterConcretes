package com.murilinho145.betterconcretes.impl.chisel;

import com.murilinho145.betterconcretes.impl.registers.ColoredBlockSet;
import com.murilinho145.betterconcretes.impl.registers.ConcreteRegister;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.Identifier;
import net.minecraft.world.item.DyeColor;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.Block;

import java.util.EnumMap;
import java.util.HashMap;
import java.util.Map;

/**
 * Maps concrete items (vanilla + mod) into a (color, variantIndex) pair,
 * and provides lookup for siblings within the same color group.
 *
 * Variants: 0=vanilla, 1=smooth, 2=chiseled, 3=polished, 4=brick.
 */
public final class ChiselConversions {

    public static final int VANILLA = 0;
    public static final int SMOOTH = 1;
    public static final int CHISELED = 2;
    public static final int POLISHED = 3;
    public static final int BRICK = 4;
    public static final int VARIANT_COUNT = 5;

    public record Entry(DyeColor color, int variantIndex) {}

    private static volatile Map<Item, Entry> itemToEntry;
    private static volatile EnumMap<DyeColor, Item[]> colorToVariants;

    private ChiselConversions() {}

    public static Entry entryFor(Item item) {
        ensureBuilt();
        return itemToEntry.get(item);
    }

    public static boolean canChisel(Item item) {
        return entryFor(item) != null;
    }

    public static Item variantOf(DyeColor color, int variantIndex) {
        ensureBuilt();
        Item[] variants = colorToVariants.get(color);
        if (variants == null || variantIndex < 0 || variantIndex >= VARIANT_COUNT) return null;
        return variants[variantIndex];
    }

    public static ItemStack result(DyeColor color, int variantIndex, int count) {
        Item item = variantOf(color, variantIndex);
        return item == null ? ItemStack.EMPTY : new ItemStack(item, count);
    }

    public static Item[] variantsOf(DyeColor color) {
        ensureBuilt();
        return colorToVariants.get(color);
    }

    /** Invalidate the cached tables — call after registries change (rare). */
    public static void invalidate() {
        itemToEntry = null;
        colorToVariants = null;
    }

    private static void ensureBuilt() {
        if (itemToEntry != null && colorToVariants != null) return;
        synchronized (ChiselConversions.class) {
            if (itemToEntry != null && colorToVariants != null) return;
            EnumMap<DyeColor, Item[]> byColor = new EnumMap<>(DyeColor.class);
            Map<Item, Entry> byItem = new HashMap<>();
            for (DyeColor color : DyeColor.values()) {
                Item[] variants = new Item[VARIANT_COUNT];
                variants[VANILLA] = vanillaConcrete(color);
                variants[SMOOTH] = itemFromSet(ConcreteRegister.SMOOTH_CONCRETE, color);
                variants[CHISELED] = itemFromSet(ConcreteRegister.CHISELED_CONCRETE, color);
                variants[POLISHED] = itemFromSet(ConcreteRegister.POLISHED_CONCRETE, color);
                variants[BRICK] = itemFromSet(ConcreteRegister.BRICK_CONCRETE, color);
                byColor.put(color, variants);
                for (int i = 0; i < VARIANT_COUNT; i++) {
                    if (variants[i] != null && variants[i] != Item.BY_BLOCK.get(null)) {
                        byItem.put(variants[i], new Entry(color, i));
                    }
                }
            }
            colorToVariants = byColor;
            itemToEntry = byItem;
        }
    }

    private static Item vanillaConcrete(DyeColor color) {
        Identifier id = Identifier.withDefaultNamespace(color.getName() + "_concrete");
        return BuiltInRegistries.BLOCK.get(id).map(ref -> ref.value().asItem()).orElse(null);
    }

    private static Item itemFromSet(ColoredBlockSet set, DyeColor color) {
        return set.item(color);
    }
}
