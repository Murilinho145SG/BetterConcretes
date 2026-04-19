package com.murilinho145.betterconcretes.compat.jei;

import com.murilinho145.betterconcretes.BetterConcretes;
import com.murilinho145.betterconcretes.impl.client.ClientRecipeCache;
import com.murilinho145.betterconcretes.impl.recipes.ChiselRecipe;
import com.murilinho145.betterconcretes.impl.recipes.WaterTransformRecipe;
import com.murilinho145.betterconcretes.impl.registers.ConcreteRegister;
import mezz.jei.api.IModPlugin;
import mezz.jei.api.JeiPlugin;
import mezz.jei.api.recipe.IRecipeManager;
import mezz.jei.api.recipe.types.IRecipeType;
import mezz.jei.api.registration.IRecipeCatalystRegistration;
import mezz.jei.api.registration.IRecipeCategoryRegistration;
import mezz.jei.api.registration.IRecipeRegistration;
import mezz.jei.api.runtime.IJeiRuntime;
import net.minecraft.resources.Identifier;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.crafting.RecipeHolder;
import net.minecraft.world.item.crafting.RecipeMap;

import java.util.List;

@JeiPlugin
public class BetterConcretesJeiPlugin implements IModPlugin {

    public static final Identifier PLUGIN_ID =
            Identifier.fromNamespaceAndPath(BetterConcretes.MODID, "jei_plugin");

    public static final IRecipeType<WaterTransformRecipe> WATER_TRANSFORM =
            IRecipeType.create(BetterConcretes.MODID, "water_transform", WaterTransformRecipe.class);

    public static final IRecipeType<ChiselRecipe> CHISEL =
            IRecipeType.create(BetterConcretes.MODID, "chisel", ChiselRecipe.class);

    @Override
    public Identifier getPluginUid() {
        return PLUGIN_ID;
    }

    @Override
    public void registerCategories(IRecipeCategoryRegistration registration) {
        registration.addRecipeCategories(
                new WaterTransformCategory(registration.getJeiHelpers().getGuiHelper()),
                new ChiselCategory(registration.getJeiHelpers().getGuiHelper())
        );
    }

    @Override
    public void registerRecipes(IRecipeRegistration registration) {
        RecipeMap recipes = ClientRecipeCache.get();

        List<WaterTransformRecipe> water = recipes.byType(ConcreteRegister.WATER_TRANSFORM.get())
                .stream().map(RecipeHolder::value).toList();
        registration.addRecipes(WATER_TRANSFORM, water);

        List<ChiselRecipe> chisel = recipes.byType(ConcreteRegister.CHISEL_RECIPE.get())
                .stream().map(RecipeHolder::value).toList();
        registration.addRecipes(CHISEL, chisel);
    }

    @Override
    public void registerRecipeCatalysts(IRecipeCatalystRegistration registration) {
        registration.addCraftingStation(CHISEL, new ItemStack(ConcreteRegister.CHISEL.get()));
    }

    private static volatile IJeiRuntime runtime;

    @Override
    public void onRuntimeAvailable(IJeiRuntime jeiRuntime) {
        runtime = jeiRuntime;
        ClientRecipeCache.setListener(BetterConcretesJeiPlugin::pushCachedRecipes);
        pushCachedRecipes();
    }

    @Override
    public void onRuntimeUnavailable() {
        runtime = null;
        ClientRecipeCache.setListener(null);
    }

    private static void pushCachedRecipes() {
        IJeiRuntime rt = runtime;
        if (rt == null) return;
        RecipeMap recipes = ClientRecipeCache.get();
        IRecipeManager manager = rt.getRecipeManager();

        List<WaterTransformRecipe> water = recipes.byType(ConcreteRegister.WATER_TRANSFORM.get())
                .stream().map(RecipeHolder::value).toList();
        manager.addRecipes(WATER_TRANSFORM, water);

        List<ChiselRecipe> chisel = recipes.byType(ConcreteRegister.CHISEL_RECIPE.get())
                .stream().map(RecipeHolder::value).toList();
        manager.addRecipes(CHISEL, chisel);
    }
}
