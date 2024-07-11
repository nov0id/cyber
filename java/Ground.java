/*
 * Decompiled with CFR 0.152.
 */
import java.awt.Color;
import java.awt.Graphics;

public class Ground
extends DrawObject {
    DPoint3[] points = new DPoint3[]{new DPoint3(-100.0, 2.0, 28.0), new DPoint3(-100.0, 2.0, 0.1), new DPoint3(100.0, 2.0, 0.1), new DPoint3(100.0, 2.0, 28.0)};
    Color color;

    void draw(Graphics graphics, DrawEnv drawEnv) {
        graphics.setColor(this.color);
        drawEnv.drawPolygon(graphics, this.points);
    }
}
