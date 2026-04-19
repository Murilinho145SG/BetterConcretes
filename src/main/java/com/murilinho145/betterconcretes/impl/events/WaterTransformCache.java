package com.murilinho145.betterconcretes.impl.events;

import com.murilinho145.betterconcretes.impl.recipes.WaterTransformRecipe;
import com.murilinho145.betterconcretes.impl.registers.ConcreteRegister;
import net.minecraft.core.Holder;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.crafting.RecipeHolder;
import net.minecraft.world.level.Level;

import java.util.HashMap;
import java.util.Map;

/**
 * Lazy O(1) lookup for {@link WaterTransformRecipe} by input Item.
 * Built on first query after invalidation; rebuilt after datapack reload.
 */
public final class WaterTransformCache {

    private static volatile Map<Item, WaterTransformRecipe> cache;

    private WaterTransformCache() {}

    public static void invalidate() {
        cache = null;
    }

    public static WaterTransformRecipe find(Level level, ItemStack stack) {
        if (stack.isEmpty()) return null;
        Map<Item, WaterTransformRecipe> local = cache;
        if (local == null) {
            local = rebuild(level);
            cache = local;
        }
        return local.get(stack.getItem());
    }

    private static Map<Item, WaterTransformRecipe> rebuild(Level level) {
        Map<Item, WaterTransformRecipe> built = new HashMap<>();
        if (!(level instanceof ServerLevel serverLevel)) return built;
        for (RecipeHolder<?> holder : serverLevel.getServer().getRecipeManager().getRecipes()) {
            if (!(holder.value() instanceof WaterTransformRecipe recipe)) continue;
            recipe.getInput().items().forEach((Holder<Item> itemHolder) ->
                    built.putIfAbsent(itemHolder.value(), recipe));
        }
        return built;
    }
}
