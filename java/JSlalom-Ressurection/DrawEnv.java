/*
 * Decompiled with CFR 0.152.
 */
import java.awt.Color;
import java.awt.Graphics;

public class DrawEnv {
    static final double T = 0.6;
    private int[] polyX = new int[8];
    private int[] polyY = new int[8];
    private DPoint3[] dp3 = new DPoint3[3];
    double nowSin;
    double nowCos;
    int width;
    int height;

    synchronized void drawPolygon(Graphics graphics, Face face) {
        int n = face.numPoints;
        DPoint3[] dPoint3Array = face.points;
        double d = dPoint3Array[1].x - dPoint3Array[0].x;
        double d2 = dPoint3Array[1].y - dPoint3Array[0].y;
        DPoint3 cfr_ignored_0 = dPoint3Array[1];
        DPoint3 cfr_ignored_1 = dPoint3Array[0];
        double d3 = dPoint3Array[2].x - dPoint3Array[0].x;
        double d4 = dPoint3Array[2].y - dPoint3Array[0].y;
        DPoint3 cfr_ignored_2 = dPoint3Array[2];
        DPoint3 cfr_ignored_3 = dPoint3Array[0];
        float f = (float)(Math.abs(d * d4 - d2 * d3) / face.maxZ);
        graphics.setColor(new Color(face.red * f, face.green * f, face.blue * f));
        double d5 = (double)this.width / 320.0;
        double d6 = (double)this.height / 200.0;
        int n2 = 0;
        while (n2 < n) {
            DPoint3 dPoint3 = dPoint3Array[n2];
            double d7 = 120.0 / (1.0 + 0.6 * dPoint3.z);
            double d8 = this.nowCos * dPoint3.x + this.nowSin * (dPoint3.y - 2.0);
            double d9 = -this.nowSin * dPoint3.x + this.nowCos * (dPoint3.y - 2.0) + 2.0;
            this.polyX[n2] = (int)(d8 * d5 * d7) + this.width / 2;
            this.polyY[n2] = (int)(d9 * d6 * d7) + this.height / 2;
            ++n2;
        }
        graphics.fillPolygon(this.polyX, this.polyY, n);
    }

    synchronized void drawPolygon(Graphics graphics, DPoint3[] dPoint3Array) {
        int n = dPoint3Array.length;
        double d = (double)this.width / 320.0;
        double d2 = (double)this.height / 200.0;
        int n2 = 0;
        while (n2 < n) {
            DPoint3 dPoint3 = dPoint3Array[n2];
            double d3 = 120.0 / (1.0 + 0.6 * dPoint3.z);
            double d4 = this.nowCos * dPoint3.x + this.nowSin * (dPoint3.y - 2.0);
            double d5 = -this.nowSin * dPoint3.x + this.nowCos * (dPoint3.y - 2.0) + 2.0;
            this.polyX[n2] = (int)(d4 * d * d3) + this.width / 2;
            this.polyY[n2] = (int)(d5 * d2 * d3) + this.height / 2;
            ++n2;
        }
        graphics.fillPolygon(this.polyX, this.polyY, n);
    }
}
