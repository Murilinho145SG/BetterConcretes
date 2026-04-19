package com.murilinho145.betterconcretes.impl.events;

import com.murilinho145.betterconcretes.impl.recipes.WaterTransformRecipe;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.entity.item.ItemEntity;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.neoforge.event.OnDatapackSyncEvent;
import net.neoforged.neoforge.event.server.ServerStartedEvent;
import net.neoforged.neoforge.event.tick.EntityTickEvent;

public class WaterTransformHandler {

    @SubscribeEvent
    public void onEntityTick(EntityTickEvent.Post event) {
        if (!(event.getEntity() instanceof ItemEntity item)) return;
        Level level = item.level();
        if (level.isClientSide()) return;
        if (!item.isInWater()) return;

        ItemStack stack = item.getItem();
        WaterTransformRecipe recipe = WaterTransformCache.find(level, stack);
        if (recipe == null) return;

        ItemStack result = recipe.getResult().create();
        result.setCount(Math.min(result.getMaxStackSize(), stack.getCount()));
        item.setItem(result);

        if (level instanceof ServerLevel serverLevel) {
            serverLevel.sendParticles(
                    ParticleTypes.SPLASH,
                    item.getX(), item.getY() + 0.25, item.getZ(),
                    8,
                    0.2, 0.1, 0.2,
                    0.0
            );
        }
        level.playSound(
                null,
                item.getX(), item.getY(), item.getZ(),
                SoundEvents.GENERIC_SPLASH, SoundSource.BLOCKS,
                0.5f, 0.9f + level.getRandom().nextFloat() * 0.2f
        );
    }

    @SubscribeEvent
    public void onServerStarted(ServerStartedEvent event) {
        WaterTransformCache.invalidate();
    }

    @SubscribeEvent
    public void onDatapackSync(OnDatapackSyncEvent event) {
        WaterTransformCache.invalidate();
    }
}
