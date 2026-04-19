package com.murilinho145.betterconcretes.compat.jei;

import com.murilinho145.betterconcretes.impl.recipes.WaterTransformRecipe;
import mezz.jei.api.gui.builder.IRecipeLayoutBuilder;
import mezz.jei.api.gui.drawable.IDrawable;
import mezz.jei.api.gui.widgets.IRecipeExtrasBuilder;
import mezz.jei.api.helpers.IGuiHelper;
import mezz.jei.api.recipe.IFocusGroup;
import mezz.jei.api.recipe.RecipeIngredientRole;
import mezz.jei.api.recipe.category.IRecipeCategory;
import mezz.jei.api.recipe.types.IRecipeType;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;

public class WaterTransformCategory implements IRecipeCategory<WaterTransformRecipe> {

    private static final int WIDTH = 100;
    private static final int HEIGHT = 26;
    private static final int INPUT_X = 4;
    private static final int OUTPUT_X = 80;
    private static final int SLOT_Y = 4;

    private final IDrawable icon;

    public WaterTransformCategory(IGuiHelper guiHelper) {
        this.icon = guiHelper.createDrawableItemStack(new ItemStack(Items.WATER_BUCKET));
    }

    @Override
    public IRecipeType<WaterTransformRecipe> getRecipeType() {
        return BetterConcretesJeiPlugin.WATER_TRANSFORM;
    }

    @Override
    public Component getTitle() {
        return Component.translatable("betterconcretes.jei.water_transform");
    }

    @Override
    public int getWidth() {
        return WIDTH;
    }

    @Override
    public int getHeight() {
        return HEIGHT;
    }

    @Override
    public IDrawable getIcon() {
        return icon;
    }

    @Override
    public void setRecipe(IRecipeLayoutBuilder builder, WaterTransformRecipe recipe, IFocusGroup focuses) {
        builder.addSlot(RecipeIngredientRole.INPUT, INPUT_X, SLOT_Y)
                .setStandardSlotBackground()
                .add(recipe.getInput());

        builder.addSlot(RecipeIngredientRole.OUTPUT, OUTPUT_X, SLOT_Y)
                .setOutputSlotBackground()
                .add(recipe.getResult());
    }

    @Override
    public void createRecipeExtras(IRecipeExtrasBuilder builder, WaterTransformRecipe recipe, IFocusGroup focuses) {
        builder.addRecipeArrow().setPosition(40, SLOT_Y);
    }
}
