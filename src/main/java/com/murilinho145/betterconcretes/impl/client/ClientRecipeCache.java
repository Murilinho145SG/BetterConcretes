package com.murilinho145.betterconcretes.impl.client;

import net.minecraft.world.item.crafting.RecipeMap;

public final class ClientRecipeCache {
    private static volatile RecipeMap recipes = RecipeMap.EMPTY;
    private static volatile Runnable onUpdate;

    private ClientRecipeCache() {}

    public static RecipeMap get() {
        return recipes;
    }

    public static void setListener(Runnable callback) {
        onUpdate = callback;
    }

    static void set(RecipeMap map) {
        recipes = map;
        Runnable cb = onUpdate;
        if (cb != null) cb.run();
    }
}
