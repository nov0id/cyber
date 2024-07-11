/*
 * Decompiled with CFR 0.152.
 */
import java.awt.Color;

public class RoadRound
extends RoundManager {
    private double OX1;
    private double OX2;
    private double OVX;
    private double WX;
    private int direction;
    private int roadCounter;
    private boolean isBrokenRoad;

    public RoadRound(int n, Color color, Color color2, boolean bl) {
        this.nextRoundScore = n;
        this.skyColor = color;
        this.groundColor = color2;
        this.isBrokenRoad = bl;
    }

    public void generateObstacle(ObstacleCollection obstacleCollection, GameRecorder gameRecorder) {
        double d;
        ++this.gameTime;
        this.roadCounter += -1;
        double d2 = 1.1;
        if (this.isBrokenRoad && this.roadCounter % 13 < 7) {
            d2 = 0.7;
            d = (double)(gameRecorder.getRandom() % 256) / 8.0 - 16.0;
            if (d < this.OX2 && d > this.OX1) {
                d2 = 1.2;
                d = gameRecorder.getRandom() % 256 > 128 ? this.OX1 : this.OX2;
            }
        } else {
            d = this.roadCounter % 2 == 0 ? this.OX1 : this.OX2;
        }
        if (this.OX2 - this.OX1 > 9.0) {
            this.OX1 += 0.6;
            this.OX2 -= 0.6;
            if (this.OX2 - this.OX1 > 10.0) {
                d2 = 2.0;
            }
        } else if (this.OX1 > 18.0) {
            this.OX2 -= 0.6;
            this.OX1 -= 0.6;
        } else if (this.OX2 < -18.0) {
            this.OX2 += 0.6;
            this.OX1 += 0.6;
        } else {
            if (this.roadCounter < 0) {
                this.direction = -this.direction;
                this.roadCounter += 2 * (gameRecorder.getRandom() % 8 + 4);
            }
            this.OVX = this.direction > 0 ? (this.OVX += 0.125) : (this.OVX -= 0.125);
            if (this.OVX > 0.7) {
                this.OVX = 0.7;
            }
            if (this.OVX < -0.7) {
                this.OVX = -0.7;
            }
            this.OX1 += this.OVX;
            this.OX2 += this.OVX;
        }
        Obstacle obstacle = this.createObstacle(gameRecorder, d, d2);
        obstacleCollection.add(obstacle);
    }

    public void init() {
        this.OX1 = -17.0;
        this.OX2 = 17.0;
        this.OVX = 0.0;
        this.roadCounter = 0;
        this.direction = 1;
        this.gameTime = 0;
    }

    public void move(double d) {
        this.OX1 += d;
        this.OX2 += d;
    }
}
