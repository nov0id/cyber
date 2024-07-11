/*
 * Decompiled with CFR 0.152.
 */
import java.awt.Color;

public class Face {
    DPoint3[] points;
    int numPoints;
    double maxZ;
    float red;
    float green;
    float blue;

    void setColor(Color color) {
        this.red = (float)color.getRed() / 255.0f;
        this.green = (float)color.getGreen() / 255.0f;
        this.blue = (float)color.getBlue() / 255.0f;
    }

    void calcMaxZ() {
        double d = this.points[1].x - this.points[0].x;
        double d2 = this.points[1].y - this.points[0].y;
        double d3 = this.points[1].z - this.points[0].z;
        double d4 = this.points[2].x - this.points[0].x;
        double d5 = this.points[2].y - this.points[0].y;
        double d6 = this.points[2].z - this.points[0].z;
        this.maxZ = Math.sqrt(this.two(d2 * d6 - d3 * d5) + this.two(d * d6 - d3 * d4) + this.two(d * d5 - d2 * d4));
    }

    private final double two(double d) {
        return d * d;
    }
}
