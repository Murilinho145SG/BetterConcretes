package com.murilinho145.betterconcretes.impl.registers;

import com.murilinho145.betterconcretes.BetterConcretes;
import com.murilinho145.betterconcretes.impl.blocks.ConnectedConcreteBlock;
import com.murilinho145.betterconcretes.impl.chisel.ChiselMenu;
import com.murilinho145.betterconcretes.impl.items.Chisel;
import com.murilinho145.betterconcretes.impl.recipes.ChiselRecipe;
import com.murilinho145.betterconcretes.impl.recipes.WaterTransformRecipe;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.world.inventory.MenuType;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.crafting.RecipeSerializer;
import net.minecraft.world.item.crafting.RecipeType;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredRegister;

import java.util.function.Supplier;

public class ConcreteRegister {

    public static final DeferredRegister.Items ITEMS =
            DeferredRegister.createItems(BetterConcretes.MODID);
    public static final DeferredRegister.Blocks BLOCKS =
            DeferredRegister.createBlocks(BetterConcretes.MODID);
    public static final DeferredRegister<CreativeModeTab> CTAB =
            DeferredRegister.create(BuiltInRegistries.CREATIVE_MODE_TAB, BetterConcretes.MODID);

    public static final DeferredHolder<Item, Item> CHISEL =
            ITEMS.registerItem("chisel", Chisel::new);

    // ---- Concrete variant block sets (16 colors each) ----

    private static BlockBehaviour.Properties concreteProps(net.minecraft.world.item.DyeColor color) {
        return BlockBehaviour.Properties.of()
                .mapColor(color.getMapColor())
                .strength(1.8f, 6.0f)
                .sound(SoundType.STONE);
    }

    public static final ColoredBlockSet SMOOTH_CONCRETE = new ColoredBlockSet(
            "smooth_{color}_concrete",
            BLOCKS,
            ITEMS,
            ConcreteRegister::concreteProps,
            ConnectedConcreteBlock::new
    );
    public static final ColoredBlockSet CHISELED_CONCRETE = new ColoredBlockSet(
            "chiseled_{color}_concrete",
            BLOCKS,
            ITEMS,
            ConcreteRegister::concreteProps
    );
    public static final ColoredBlockSet POLISHED_CONCRETE = new ColoredBlockSet(
            "polished_{color}_concrete",
            BLOCKS,
            ITEMS,
            ConcreteRegister::concreteProps
    );
    public static final ColoredBlockSet BRICK_CONCRETE = new ColoredBlockSet(
            "brick_{color}_concrete",
            BLOCKS,
            ITEMS,
            ConcreteRegister::concreteProps
    );

    public static final Supplier<CreativeModeTab> BTAB = CTAB.register("concretes", () -> CreativeModeTab.builder()
            .title(Component.translatable("betterconcretes.tab"))
            .icon(() -> CHISEL.get().getDefaultInstance())
            .displayItems((params, output) -> {
                for (DeferredHolder<Item, ? extends Item> entry : ITEMS.getEntries()) {
                    output.accept(entry.get());
                }
            })
            .build());

    public static final DeferredRegister<RecipeType<?>> RECIPE_TYPES =
            DeferredRegister.create(Registries.RECIPE_TYPE, BetterConcretes.MODID);
    public static final Supplier<RecipeType<WaterTransformRecipe>> WATER_TRANSFORM = RECIPE_TYPES.register("water_transform",
            () -> RecipeType.<WaterTransformRecipe>simple(Identifier.fromNamespaceAndPath(BetterConcretes.MODID, "water_transform")));
    public static final DeferredRegister<RecipeSerializer<?>> RECIPE_SERIALIZERS =
            DeferredRegister.create(Registries.RECIPE_SERIALIZER, BetterConcretes.MODID);
    public static final Supplier<RecipeSerializer<WaterTransformRecipe>> WATER_TRANSFORM_SERIALIZER =
            RECIPE_SERIALIZERS.register("water_transform", () -> WaterTransformRecipe.SERIALIZER);
    public static final Supplier<RecipeType<ChiselRecipe>> CHISEL_RECIPE = RECIPE_TYPES.register("chisel",
            () -> RecipeType.<ChiselRecipe>simple(Identifier.fromNamespaceAndPath(BetterConcretes.MODID, "chisel")));
    public static final Supplier<RecipeSerializer<ChiselRecipe>> CHISEL_SERIALIZER =
            RECIPE_SERIALIZERS.register("chisel", () -> ChiselRecipe.SERIALIZER);

    public static final DeferredRegister<MenuType<?>> MENU_TYPES =
            DeferredRegister.create(BuiltInRegistries.MENU, BetterConcretes.MODID);
    public static final Supplier<MenuType<ChiselMenu>> CHISEL_MENU =
            MENU_TYPES.register("chisel", () -> new MenuType<>(ChiselMenu::new, net.minecraft.world.flag.FeatureFlags.VANILLA_SET));
}
