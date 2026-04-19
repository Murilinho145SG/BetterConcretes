package com.murilinho145.betterconcretes.impl.recipes;

import com.mojang.serialization.MapCodec;
import com.murilinho145.betterconcretes.impl.registers.ConcreteRegister;
import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.world.item.ItemStackTemplate;
import net.minecraft.world.item.crafting.Ingredient;
import net.minecraft.world.item.crafting.Recipe;
import net.minecraft.world.item.crafting.RecipeBookCategories;
import net.minecraft.world.item.crafting.RecipeBookCategory;
import net.minecraft.world.item.crafting.RecipeSerializer;
import net.minecraft.world.item.crafting.RecipeType;
import net.minecraft.world.item.crafting.SingleItemRecipe;

public class ChiselRecipe extends SingleItemRecipe {
    public static final MapCodec<ChiselRecipe> MAP_CODEC = simpleMapCodec(ChiselRecipe::new);
    public static final StreamCodec<RegistryFriendlyByteBuf, ChiselRecipe> STREAM_CODEC = simpleStreamCodec(ChiselRecipe::new);
    public static final RecipeSerializer<ChiselRecipe> SERIALIZER = new RecipeSerializer<>(MAP_CODEC, STREAM_CODEC);

    public ChiselRecipe(Recipe.CommonInfo commonInfo, Ingredient ingredient, ItemStackTemplate result) {
        super(commonInfo, ingredient, result);
    }

    @Override
    public RecipeSerializer<ChiselRecipe> getSerializer() {
        return ConcreteRegister.CHISEL_SERIALIZER.get();
    }

    @Override
    public RecipeType<ChiselRecipe> getType() {
        return ConcreteRegister.CHISEL_RECIPE.get();
    }

    @Override
    public String group() {
        return "";
    }

    @Override
    public RecipeBookCategory recipeBookCategory() {
        return RecipeBookCategories.STONECUTTER;
    }

    public Ingredient getInput() {
        return this.input();
    }

    public ItemStackTemplate getResult() {
        return this.result();
    }
}
