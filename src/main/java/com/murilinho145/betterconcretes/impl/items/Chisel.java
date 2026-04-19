package com.murilinho145.betterconcretes.impl.items;

import com.murilinho145.betterconcretes.impl.chisel.ChiselConversions;
import com.murilinho145.betterconcretes.impl.chisel.ChiselMenu;
import net.minecraft.core.BlockPos;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.SimpleMenuProvider;
import net.minecraft.world.SimpleContainer;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.ContainerLevelAccess;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.context.UseOnContext;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockState;

public class Chisel extends Item {

    public Chisel(Properties properties) {
        super(properties.durability(256));
    }

    @Override
    public InteractionResult use(Level level, Player player, InteractionHand hand) {
        if (!level.isClientSide() && player instanceof ServerPlayer serverPlayer) {
            serverPlayer.openMenu(new SimpleMenuProvider(
                    (id, inv, p) -> new ChiselMenu(id, inv, new SimpleContainer(2), ContainerLevelAccess.create(level, serverPlayer.blockPosition())),
                    Component.translatable("container.betterconcretes.chisel")
            ));
        }
        return level.isClientSide() ? InteractionResult.SUCCESS : InteractionResult.SUCCESS_SERVER;
    }

    @Override
    public InteractionResult useOn(UseOnContext context) {
        Level level = context.getLevel();
        BlockPos pos = context.getClickedPos();
        BlockState state = level.getBlockState(pos);
        Player player = context.getPlayer();
        if (player == null) return InteractionResult.PASS;

        Item blockItem = state.getBlock().asItem();
        ChiselConversions.Entry entry = ChiselConversions.entryFor(blockItem);
        if (entry == null) return InteractionResult.PASS;

        int nextVariant = nextAvailableVariant(entry);
        if (nextVariant == entry.variantIndex()) return InteractionResult.PASS;

        Item targetItem = ChiselConversions.variantOf(entry.color(), nextVariant);
        if (!(targetItem instanceof net.minecraft.world.item.BlockItem blockTarget)) {
            return InteractionResult.PASS;
        }
        Block targetBlock = blockTarget.getBlock();
        BlockState targetState = targetBlock.defaultBlockState();

        if (!level.isClientSide()) {
            level.setBlock(pos, targetState, Block.UPDATE_ALL);
            level.playSound(null, pos, SoundEvents.UI_STONECUTTER_TAKE_RESULT, SoundSource.BLOCKS, 0.8f, 1.0f);
            if (!player.getAbilities().instabuild) {
                context.getItemInHand().hurtAndBreak(1, (ServerLevel) level, player,
                        item -> player.onEquippedItemBroken(item, context.getHand().equals(InteractionHand.MAIN_HAND)
                                ? net.minecraft.world.entity.EquipmentSlot.MAINHAND
                                : net.minecraft.world.entity.EquipmentSlot.OFFHAND));
            }
        }
        return level.isClientSide() ? InteractionResult.SUCCESS : InteractionResult.SUCCESS_SERVER;
    }

    private static int nextAvailableVariant(ChiselConversions.Entry entry) {
        int start = entry.variantIndex();
        for (int step = 1; step <= ChiselConversions.VARIANT_COUNT; step++) {
            int candidate = (start + step) % ChiselConversions.VARIANT_COUNT;
            if (ChiselConversions.variantOf(entry.color(), candidate) != null
                    && ChiselConversions.variantOf(entry.color(), candidate) != Items.AIR) {
                return candidate;
            }
        }
        return start;
    }
}
