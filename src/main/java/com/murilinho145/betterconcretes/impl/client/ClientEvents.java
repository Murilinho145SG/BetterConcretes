package com.murilinho145.betterconcretes.impl.client;

import com.murilinho145.betterconcretes.BetterConcretes;
import com.murilinho145.betterconcretes.impl.chisel.ChiselScreen;
import com.murilinho145.betterconcretes.impl.registers.ConcreteRegister;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.RecipesReceivedEvent;
import net.neoforged.neoforge.client.event.RegisterBlockStateModels;
import net.neoforged.neoforge.client.event.RegisterMenuScreensEvent;

@EventBusSubscriber(modid = BetterConcretes.MODID, value = Dist.CLIENT)
public class ClientEvents {

    // CTM model loader deferred to 2.1.1 — requires rewrite against the new UnbakedModelLoader API.

    @SubscribeEvent
    public static void registerScreens(RegisterMenuScreensEvent event) {
        event.register(ConcreteRegister.CHISEL_MENU.get(), ChiselScreen::new);
    }

    @SubscribeEvent
    public static void onRecipesReceived(RecipesReceivedEvent event) {
        ClientRecipeCache.set(event.getRecipeMap());
    }

    @SubscribeEvent
    public static void onRegisterBlockStateModels(RegisterBlockStateModels event) {
        event.registerModel(ConnectedBlockStateModel.LOADER_ID, ConnectedBlockStateModel.Unbaked.MAP_CODEC);
    }
}
