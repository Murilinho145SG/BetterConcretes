package com.murilinho145.betterconcretes.impl.chisel;

import com.murilinho145.betterconcretes.impl.registers.ConcreteRegister;
import net.minecraft.world.Container;
import net.minecraft.world.SimpleContainer;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.AbstractContainerMenu;
import net.minecraft.world.inventory.ContainerLevelAccess;
import net.minecraft.world.inventory.DataSlot;
import net.minecraft.world.inventory.Slot;
import net.minecraft.world.item.ItemStack;

public class ChiselMenu extends AbstractContainerMenu {

    public static final int INPUT_SLOT = 0;
    public static final int OUTPUT_SLOT = 1;
    private static final int INV_START = 2;
    private static final int INV_END = INV_START + 27;
    private static final int HOTBAR_END = INV_END + 9;

    private final Container container;
    private final ContainerLevelAccess access;
    private final DataSlot selectedVariant = DataSlot.standalone();
    private final Player player;

    /** Client constructor. */
    public ChiselMenu(int containerId, Inventory playerInv) {
        this(containerId, playerInv, new SimpleContainer(2), ContainerLevelAccess.NULL);
    }

    /** Server constructor. */
    public ChiselMenu(int containerId, Inventory playerInv, Container container, ContainerLevelAccess access) {
        super(ConcreteRegister.CHISEL_MENU.get(), containerId);
        this.container = container;
        this.access = access;
        this.player = playerInv.player;
        checkContainerSize(container, 2);

        this.addSlot(new Slot(container, INPUT_SLOT, 9, 25) { // frame at (8,24)
            @Override
            public boolean mayPlace(ItemStack stack) {
                return ChiselConversions.canChisel(stack.getItem());
            }

            @Override
            public void setChanged() {
                super.setChanged();
                ChiselMenu.this.slotsChanged(container);
            }
        });

        this.addSlot(new Slot(container, OUTPUT_SLOT, 153, 25) { // frame at (152,24)
            @Override
            public boolean mayPlace(ItemStack stack) {
                return false;
            }

            @Override
            public void onTake(Player p, ItemStack taken) {
                ItemStack input = container.getItem(INPUT_SLOT);
                if (!input.isEmpty()) {
                    input.shrink(taken.getCount());
                    container.setItem(INPUT_SLOT, input);
                }
                ChiselMenu.this.updateOutput();
                super.onTake(p, taken);
            }
        });

        // Player inventory (3x9) — rows TOUCH (no gap) at y=65, 83, 101 (frames 64, 82, 100)
        for (int row = 0; row < 3; row++) {
            for (int col = 0; col < 9; col++) {
                this.addSlot(new Slot(playerInv, col + row * 9 + 9, 8 + col * 18, 65 + row * 18));
            }
        }
        // Hotbar at y=123 (frame 122) — 4px gap from inventory
        for (int col = 0; col < 9; col++) {
            this.addSlot(new Slot(playerInv, col, 8 + col * 18, 123));
        }

        this.addDataSlot(selectedVariant);
        selectedVariant.set(-1);
    }

    public int getSelectedVariant() {
        return selectedVariant.get();
    }

    public ItemStack getInput() {
        return container.getItem(INPUT_SLOT);
    }

    public ItemStack getOutput() {
        return container.getItem(OUTPUT_SLOT);
    }

    @Override
    public boolean clickMenuButton(Player player, int buttonId) {
        if (buttonId < 0 || buttonId >= ChiselConversions.VARIANT_COUNT) return false;
        ItemStack input = container.getItem(INPUT_SLOT);
        if (input.isEmpty()) return false;
        ChiselConversions.Entry entry = ChiselConversions.entryFor(input.getItem());
        if (entry == null) return false;
        if (entry.variantIndex() == buttonId) return false;
        if (ChiselConversions.variantOf(entry.color(), buttonId) == null) return false;

        selectedVariant.set(buttonId);
        updateOutput();
        return true;
    }

    @Override
    public void slotsChanged(Container changed) {
        if (changed == this.container) {
            ItemStack input = container.getItem(INPUT_SLOT);
            if (input.isEmpty()) {
                selectedVariant.set(-1);
            } else {
                ChiselConversions.Entry entry = ChiselConversions.entryFor(input.getItem());
                if (entry != null && selectedVariant.get() == entry.variantIndex()) {
                    selectedVariant.set(-1);
                }
            }
            updateOutput();
        }
        super.slotsChanged(changed);
    }

    private void updateOutput() {
        ItemStack input = container.getItem(INPUT_SLOT);
        int variant = selectedVariant.get();
        if (input.isEmpty() || variant < 0) {
            container.setItem(OUTPUT_SLOT, ItemStack.EMPTY);
            return;
        }
        ChiselConversions.Entry entry = ChiselConversions.entryFor(input.getItem());
        if (entry == null || entry.variantIndex() == variant) {
            container.setItem(OUTPUT_SLOT, ItemStack.EMPTY);
            return;
        }
        ItemStack out = ChiselConversions.result(entry.color(), variant, input.getCount());
        container.setItem(OUTPUT_SLOT, out);
    }

    @Override
    public ItemStack quickMoveStack(Player player, int index) {
        ItemStack result = ItemStack.EMPTY;
        Slot slot = this.slots.get(index);
        if (slot.hasItem()) {
            ItemStack stack = slot.getItem();
            result = stack.copy();
            if (index == OUTPUT_SLOT) {
                // Output -> inventory: consume input proportionally
                if (!this.moveItemStackTo(stack, INV_START, HOTBAR_END, true)) return ItemStack.EMPTY;
                slot.onQuickCraft(stack, result);
                ItemStack input = container.getItem(INPUT_SLOT);
                input.shrink(result.getCount());
                container.setItem(INPUT_SLOT, input);
                updateOutput();
            } else if (index == INPUT_SLOT) {
                if (!this.moveItemStackTo(stack, INV_START, HOTBAR_END, false)) return ItemStack.EMPTY;
            } else if (ChiselConversions.canChisel(stack.getItem())) {
                if (!this.moveItemStackTo(stack, INPUT_SLOT, INPUT_SLOT + 1, false)) return ItemStack.EMPTY;
            } else if (index < INV_END) {
                // Main inventory -> hotbar
                if (!this.moveItemStackTo(stack, INV_END, HOTBAR_END, false)) return ItemStack.EMPTY;
            } else {
                // Hotbar -> main inventory
                if (!this.moveItemStackTo(stack, INV_START, INV_END, false)) return ItemStack.EMPTY;
            }

            if (stack.isEmpty()) slot.set(ItemStack.EMPTY);
            else slot.setChanged();
            if (stack.getCount() == result.getCount()) return ItemStack.EMPTY;
            slot.onTake(player, stack);
        }
        return result;
    }

    @Override
    public void removed(Player player) {
        super.removed(player);
        // Drop input back to player so items aren't lost.
        this.access.execute((level, pos) -> {
            ItemStack input = container.getItem(INPUT_SLOT);
            if (!input.isEmpty()) {
                player.getInventory().placeItemBackInInventory(input);
                container.setItem(INPUT_SLOT, ItemStack.EMPTY);
            }
        });
    }

    @Override
    public boolean stillValid(Player player) {
        return true;
    }
}
