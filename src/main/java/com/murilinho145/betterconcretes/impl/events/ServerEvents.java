package com.murilinho145.betterconcretes.impl.events;

import com.murilinho145.betterconcretes.BetterConcretes;
import com.murilinho145.betterconcretes.impl.registers.ConcreteRegister;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.event.OnDatapackSyncEvent;

@EventBusSubscriber(modid = BetterConcretes.MODID)
public class ServerEvents {

    @SubscribeEvent
    public static void onDatapackSync(OnDatapackSyncEvent event) {
        event.sendRecipes(
                ConcreteRegister.WATER_TRANSFORM.get(),
                ConcreteRegister.CHISEL_RECIPE.get()
        );
    }
}
