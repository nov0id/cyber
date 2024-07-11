/*
 * Decompiled with CFR 0.152.
 */
import java.awt.Color;
import java.awt.Graphics;

public class Obstacle
extends DrawObject {
    DPoint3[] points = new DPoint3[]{new DPoint3(), new DPoint3(), new DPoint3(), new DPoint3()};
    Face[] faces = new Face[]{new Face(), new Face(), new Face()};
    Obstacle next = null;
    Obstacle prev = null;
    Color color;
    private static Obstacle head = null;

    static synchronized void releaseObstacle(Obstacle obstacle) {
        if (obstacle == null) {
            return;
        }
        obstacle.next = head;
        head = obstacle;
    }

    void release() {
        this.prev.next = this.next;
        this.next.prev = this.prev;
        Obstacle.releaseObstacle(this);
    }

    void draw(Graphics graphics, DrawEnv drawEnv) {
        drawEnv.drawPolygon(graphics, this.faces[0]);
        drawEnv.drawPolygon(graphics, this.faces[1]);
    }

    Obstacle() {
        this.faces[0].points = new DPoint3[]{this.points[3], this.points[0], this.points[1]};
        this.faces[0].numPoints = 3;
        this.faces[1].points = new DPoint3[]{this.points[3], this.points[2], this.points[1]};
        this.faces[1].numPoints = 3;
    }

    static {
        int n = 0;
        do {
            Obstacle obstacle = new Obstacle();
            obstacle.next = head;
            head = obstacle;
        } while (++n < 16);
    }

    static synchronized Obstacle newObstacle() {
        Obstacle obstacle = head;
        if (obstacle == null) {
            obstacle = new Obstacle();
        } else {
            head = Obstacle.head.next;
        }
        obstacle.next = null;
        return obstacle;
    }

    void prepareNewObstacle() {
        this.faces[0].setColor(this.color.brighter());
        this.faces[0].calcMaxZ();
        this.faces[1].setColor(this.color);
        this.faces[1].calcMaxZ();
    }

    void move(double d, double d2, double d3) {
        int n = 0;
        do {
            DPoint3 dPoint3 = this.points[n];
            dPoint3.x += d;
            dPoint3.y += d2;
            dPoint3.z += d3;
        } while (++n < 4);
    }
}
