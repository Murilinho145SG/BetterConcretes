package com.murilinho145.betterconcretes.impl.chisel;

import com.murilinho145.betterconcretes.BetterConcretes;
import net.minecraft.client.gui.GuiGraphicsExtractor;
import net.minecraft.client.gui.screens.inventory.AbstractContainerScreen;
import net.minecraft.client.input.MouseButtonEvent;
import net.minecraft.client.renderer.RenderPipelines;
import net.minecraft.client.resources.sounds.SimpleSoundInstance;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.item.DyeColor;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;

public class ChiselScreen extends AbstractContainerScreen<ChiselMenu> {

    private static final int BUTTON_Y = 23;
    private static final int BUTTON_SIZE = 20;
    private static final int BUTTON_GAP = 2;
    private static final int BUTTON_X_START = 30;
    private static final int BUTTON_ICON_INSET = 2;
    private static final int LABEL_STRIP_Y = 49;

    private static final String[] VARIANT_KEYS = {
            "betterconcretes.variant.vanilla",
            "betterconcretes.variant.smooth",
            "betterconcretes.variant.chiseled",
            "betterconcretes.variant.polished",
            "betterconcretes.variant.brick",
    };

    private static final Identifier BG_TEXTURE = Identifier.fromNamespaceAndPath(BetterConcretes.MODID, "textures/gui/chisel.png");
    private static final int GUI_WIDTH = 176;
    private static final int GUI_HEIGHT = 146;

    public ChiselScreen(ChiselMenu menu, Inventory playerInv, Component title) {
        super(menu, playerInv, title, GUI_WIDTH, GUI_HEIGHT);
        this.titleLabelX = 8;
        this.titleLabelY = 5;
        this.inventoryLabelY = this.imageHeight - 94;
    }

    @Override
    public void extractBackground(GuiGraphicsExtractor graphics, int mouseX, int mouseY, float partialTicks) {
        super.extractBackground(graphics, mouseX, mouseY, partialTicks);
        graphics.blit(RenderPipelines.GUI_TEXTURED, BG_TEXTURE, this.leftPos, this.topPos,
                0f, 0f, this.imageWidth, this.imageHeight, 256, 256);
    }

    @Override
    public void extractRenderState(GuiGraphicsExtractor graphics, int mouseX, int mouseY, float partialTicks) {
        super.extractRenderState(graphics, mouseX, mouseY, partialTicks);
        renderVariantButtons(graphics, mouseX, mouseY);
        renderVariantLabel(graphics, mouseX, mouseY);
    }

    @Override
    protected void extractLabels(GuiGraphicsExtractor graphics, int mouseX, int mouseY) {
        graphics.text(this.font, this.title, this.titleLabelX + 1, this.titleLabelY + 1, 0xFF2B1B0A, false);
        graphics.text(this.font, this.title, this.titleLabelX, this.titleLabelY, 0xFFF8E4B8, false);
    }

    private DyeColor activeColor() {
        ItemStack input = menu.getInput();
        if (input.isEmpty()) return null;
        ChiselConversions.Entry entry = ChiselConversions.entryFor(input.getItem());
        return entry == null ? null : entry.color();
    }

    private int currentVariant() {
        ItemStack input = menu.getInput();
        if (input.isEmpty()) return -1;
        ChiselConversions.Entry entry = ChiselConversions.entryFor(input.getItem());
        return entry == null ? -1 : entry.variantIndex();
    }

    private int hoveredVariant(int mouseX, int mouseY) {
        for (int i = 0; i < ChiselConversions.VARIANT_COUNT; i++) {
            int bx = this.leftPos + BUTTON_X_START + i * (BUTTON_SIZE + BUTTON_GAP);
            int by = this.topPos + BUTTON_Y;
            if (mouseX >= bx && mouseX < bx + BUTTON_SIZE && mouseY >= by && mouseY < by + BUTTON_SIZE) {
                return i;
            }
        }
        return -1;
    }

    private void renderVariantButtons(GuiGraphicsExtractor graphics, int mouseX, int mouseY) {
        DyeColor color = activeColor();
        int selected = menu.getSelectedVariant();
        int current = currentVariant();
        int hovered = hoveredVariant(mouseX, mouseY);

        for (int i = 0; i < ChiselConversions.VARIANT_COUNT; i++) {
            int bx = this.leftPos + BUTTON_X_START + i * (BUTTON_SIZE + BUTTON_GAP);
            int by = this.topPos + BUTTON_Y;

            Item variantItem = color == null ? null : ChiselConversions.variantOf(color, i);
            boolean isSelected = (selected == i);

            if (isSelected) {
                graphics.fill(bx + 1, by + 1, bx + BUTTON_SIZE - 1, by + 2, 0xFF555555);
                graphics.fill(bx + 1, by + 1, bx + 2, by + BUTTON_SIZE - 1, 0xFF555555);
                graphics.fill(bx + 2, by + BUTTON_SIZE - 2, bx + BUTTON_SIZE - 1, by + BUTTON_SIZE - 1, 0xFFDDDDDD);
                graphics.fill(bx + BUTTON_SIZE - 2, by + 2, bx + BUTTON_SIZE - 1, by + BUTTON_SIZE - 1, 0xFFDDDDDD);
                graphics.fill(bx + 2, by + 2, bx + BUTTON_SIZE - 2, by + BUTTON_SIZE - 2, 0xFF808080);
            }

            if (variantItem != null) {
                int iconOffset = isSelected ? 1 : 0;
                graphics.item(new ItemStack(variantItem),
                        bx + BUTTON_ICON_INSET + iconOffset,
                        by + BUTTON_ICON_INSET + iconOffset);
            }

            if (current == i && color != null && !isSelected) {
                graphics.fill(bx + BUTTON_ICON_INSET, by + BUTTON_ICON_INSET,
                        bx + BUTTON_ICON_INSET + 16, by + BUTTON_ICON_INSET + 16, 0x55000000);
            }
            if (hovered == i && variantItem != null && !isSelected) {
                int outline = 0xFFFFEE88;
                graphics.fill(bx, by, bx + BUTTON_SIZE, by + 1, outline);
                graphics.fill(bx, by + BUTTON_SIZE - 1, bx + BUTTON_SIZE, by + BUTTON_SIZE, outline);
                graphics.fill(bx, by, bx + 1, by + BUTTON_SIZE, outline);
                graphics.fill(bx + BUTTON_SIZE - 1, by, bx + BUTTON_SIZE, by + BUTTON_SIZE, outline);
            }
        }
    }

    private void renderVariantLabel(GuiGraphicsExtractor graphics, int mouseX, int mouseY) {
        DyeColor color = activeColor();
        if (color == null) return;

        int hovered = hoveredVariant(mouseX, mouseY);
        int selected = menu.getSelectedVariant();
        int current = currentVariant();
        int show = hovered >= 0 ? hovered : (selected >= 0 ? selected : current);
        if (show < 0) return;

        Item variantItem = ChiselConversions.variantOf(color, show);
        if (variantItem == null) return;

        Component label = Component.translatable(VARIANT_KEYS[show]);
        int labelW = this.font.width(label);
        int labelX = this.leftPos + (this.imageWidth - labelW) / 2;
        int labelY = this.topPos + LABEL_STRIP_Y;

        int textColor = hovered >= 0 ? 0xFFFFEE88 : 0xFFE0E0E0;
        graphics.text(this.font, label, labelX, labelY, textColor, false);
    }

    @Override
    public boolean mouseClicked(MouseButtonEvent event, boolean doubleClick) {
        if (event.button() == 0) {
            int i = hoveredVariant((int) event.x(), (int) event.y());
            if (i >= 0 && this.minecraft != null && this.minecraft.gameMode != null) {
                this.minecraft.gameMode.handleInventoryButtonClick(menu.containerId, i);
                this.minecraft.getSoundManager().play(
                        SimpleSoundInstance.forUI(SoundEvents.UI_BUTTON_CLICK.value(), 1.0f)
                );
                return true;
            }
        }
        return super.mouseClicked(event, doubleClick);
    }
}
