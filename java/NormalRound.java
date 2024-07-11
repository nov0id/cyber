/*
 * Decompiled with CFR 0.152.
 */
import java.awt.Color;

public class NormalRound
extends RoundManager {
    private int interval;
    private int counter;

    public NormalRound(int n, Color color, Color color2, int n2) {
        this.nextRoundScore = n;
        this.skyColor = color;
        this.groundColor = color2;
        this.interval = n2;
    }

    public void generateObstacle(ObstacleCollection obstacleCollection, GameRecorder gameRecorder) {
        ++this.gameTime;
        ++this.counter;
        if (this.counter < this.interval) {
            return;
        }
        this.counter = 0;
        Obstacle obstacle = this.createObstacle(gameRecorder, 0.6);
        obstacleCollection.add(obstacle);
    }

    public void init() {
        this.counter = 0;
        this.gameTime = 0;
    }
}
