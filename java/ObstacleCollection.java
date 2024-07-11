/*
 * Decompiled with CFR 0.152.
 */
import java.awt.Graphics;

public class ObstacleCollection {
    Obstacle head = new Obstacle();
    Obstacle tail;

    synchronized void removeAll() {
        Obstacle obstacle = this.head.next;
        while (obstacle != this.tail) {
            Obstacle obstacle2 = obstacle.next;
            obstacle.release();
            obstacle = obstacle2;
        }
    }

    synchronized void draw(Graphics graphics, DrawEnv drawEnv) {
        Obstacle obstacle = this.head.next;
        while (obstacle != this.tail) {
            obstacle.draw(graphics, drawEnv);
            obstacle = obstacle.next;
        }
    }

    ObstacleCollection() {
        this.head.next = this.tail = new Obstacle();
        this.tail.prev = this.head;
    }

    synchronized void add(Obstacle obstacle) {
        obstacle.prev = this.head;
        obstacle.next = this.head.next;
        this.head.next.prev = obstacle;
        this.head.next = obstacle;
    }
}
