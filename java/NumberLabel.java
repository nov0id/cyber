/*
 * Decompiled with CFR 0.152.
 */
import java.awt.Canvas;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;

public class NumberLabel
extends Canvas {
    char[] data = new char[6];
    Graphics gra;
    int width;
    int height;

    public void setNum(int n) {
        int n2 = 0;
        do {
            this.data[5 - n2] = (char)(n % 10 + 48);
            n /= 10;
        } while (++n2 < 6);
        if (this.gra == null) {
            this.gra = this.getGraphics();
        }
        this.gra.clearRect(0, 0, this.width, this.height);
        this.paint(this.gra);
    }

    public NumberLabel(int n, int n2) {
        int n3 = 0;
        do {
            this.data[n3] = 48;
        } while (++n3 < 6);
        this.width = n;
        this.height = n2;
        this.setSize(n, n2);
    }

    public void paint(Graphics graphics) {
        graphics.setColor(Color.white);
        graphics.drawChars(this.data, 0, 6, 4, 14);
    }

    public Dimension getPreferredSize() {
        return new Dimension(this.width, this.height);
    }
}
