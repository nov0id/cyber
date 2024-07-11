/*
 * Decompiled with CFR 0.152.
 */
import java.awt.Color;
import java.awt.Font;
import java.awt.FontMetrics;
import java.awt.Graphics;

class StringObject
extends DrawObject {
    private Graphics currentGra = null;
    private Font font;
    private String str;
    private Color color;
    private int x;
    private int y;
    boolean isUnderLine = false;
    private int strWidth;
    private int strHeight;

    void draw(Graphics graphics, DrawEnv drawEnv) {
        graphics.setColor(this.color);
        graphics.setFont(this.font);
        if (graphics != this.currentGra) {
            this.currentGra = graphics;
            this.setStrSize();
        }
        graphics.drawString(this.str, this.x - this.strWidth / 2, this.y + this.strHeight / 2);
        if (this.isUnderLine) {
            graphics.drawLine(this.x - this.strWidth / 2, this.y + this.strHeight / 2 + 1, this.x + this.strWidth / 2, this.y + this.strHeight / 2 + 1);
        }
    }

    StringObject(Font font, Color color, String string, int n, int n2) {
        this.font = font;
        this.str = string;
        this.color = color;
        this.x = n;
        this.y = n2;
    }

    void setColor(Color color) {
        this.color = color;
    }

    boolean hitTest(int n, int n2) {
        if (this.currentGra == null) {
            return false;
        }
        return this.x - this.strWidth / 2 < n && n < this.x + this.strWidth / 2 && this.y - this.strHeight / 2 < n2 && n2 < this.y + this.strHeight / 2;
    }

    private void setStrSize() {
        FontMetrics fontMetrics = this.currentGra.getFontMetrics();
        this.strWidth = fontMetrics.stringWidth(this.str);
        this.strHeight = fontMetrics.getHeight();
    }
}
