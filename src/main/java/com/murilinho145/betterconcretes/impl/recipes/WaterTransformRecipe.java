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

public class WaterTransformRecipe extends SingleItemRecipe {
    public static final MapCodec<WaterTransformRecipe> MAP_CODEC = simpleMapCodec(WaterTransformRecipe::new);
    public static final StreamCodec<RegistryFriendlyByteBuf, WaterTransformRecipe> STREAM_CODEC = simpleStreamCodec(WaterTransformRecipe::new);
    public static final RecipeSerializer<WaterTransformRecipe> SERIALIZER = new RecipeSerializer<>(MAP_CODEC, STREAM_CODEC);

    public WaterTransformRecipe(Recipe.CommonInfo commonInfo, Ingredient ingredient, ItemStackTemplate result) {
        super(commonInfo, ingredient, result);
    }

    @Override
    public RecipeSerializer<WaterTransformRecipe> getSerializer() {
        return ConcreteRegister.WATER_TRANSFORM_SERIALIZER.get();
    }

    @Override
    public RecipeType<WaterTransformRecipe> getType() {
        return ConcreteRegister.WATER_TRANSFORM.get();
    }

    @Override
    public String group() {
        return "";
    }

    @Override
    public RecipeBookCategory recipeBookCategory() {
        return RecipeBookCategories.CRAFTING_BUILDING_BLOCKS;
    }

    public Ingredient getInput() {
        return this.input();
    }

    public ItemStackTemplate getResult() {
        return this.result();
    }
}
