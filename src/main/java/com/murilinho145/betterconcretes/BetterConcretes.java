package com.murilinho145.betterconcretes;

import com.murilinho145.betterconcretes.impl.events.WaterTransformHandler;
import com.murilinho145.betterconcretes.impl.registers.ConcreteRegister;
import net.neoforged.neoforge.common.NeoForge;
import org.slf4j.Logger;
import com.mojang.logging.LogUtils;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;
import net.neoforged.fml.ModContainer;

@Mod(BetterConcretes.MODID)
public class BetterConcretes {
    public static final String MODID = "betterconcretes";
    public static final Logger LOGGER = LogUtils.getLogger();

    public BetterConcretes(IEventBus modEventBus, ModContainer modContainer) {
        ConcreteRegister.BLOCKS.register(modEventBus);
        ConcreteRegister.ITEMS.register(modEventBus);
        ConcreteRegister.CTAB.register(modEventBus);
        ConcreteRegister.RECIPE_TYPES.register(modEventBus);
        ConcreteRegister.RECIPE_SERIALIZERS.register(modEventBus);
        ConcreteRegister.MENU_TYPES.register(modEventBus);
        NeoForge.EVENT_BUS.register(new WaterTransformHandler());
    }
}
