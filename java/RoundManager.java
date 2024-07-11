/*
 * Decompiled with CFR 0.152.
 */
import java.awt.Color;

public abstract class RoundManager {
    private RoundManager prevRound;
    static final Color[] colors = new Color[]{Color.lightGray, new Color(96, 160, 240), new Color(200, 128, 0), new Color(240, 210, 100)};
    protected int nextRoundScore;
    protected Color skyColor;
    protected Color groundColor;
    protected int gameTime;

    protected final Obstacle createObstacle(GameRecorder gameRecorder, double d, double d2) {
        Obstacle obstacle = Obstacle.newObstacle();
        DPoint3[] dPoint3Array = obstacle.points;
        dPoint3Array[0].setXYZ(d - d2, 2.0, 25.5);
        dPoint3Array[1].setXYZ(d, -1.4, 25.0);
        dPoint3Array[2].setXYZ(d + d2, 2.0, 25.5);
        dPoint3Array[3].setXYZ(d, 2.0, 24.5);
        obstacle.color = colors[gameRecorder.getRandom() % 4];
        obstacle.prepareNewObstacle();
        return obstacle;
    }

    protected final Obstacle createObstacle(GameRecorder gameRecorder, double d) {
        double d2 = (double)(gameRecorder.getRandom() % 256) / 8.0 - 16.0;
        return this.createObstacle(gameRecorder, d2, 0.6);
    }

    public abstract void generateObstacle(ObstacleCollection var1, GameRecorder var2);

    public boolean isNextRound(int n) {
        return n >= this.nextRoundScore;
    }

    public void setPrevRound(RoundManager roundManager) {
        this.prevRound = roundManager;
    }

    public Color getGroundColor() {
        return this.groundColor;
    }

    public int getNextRoundScore() {
        return this.nextRoundScore;
    }

    public void init() {
    }

    public Color getSkyColor() {
        if (this.prevRound == null || this.gameTime > 32) {
            return this.skyColor;
        }
        int n = this.gameTime;
        int n2 = 32 - n;
        Color color = this.prevRound.skyColor;
        int n3 = color.getRed() * n2 + this.skyColor.getRed() * n;
        int n4 = color.getGreen() * n2 + this.skyColor.getGreen() * n;
        int n5 = color.getBlue() * n2 + this.skyColor.getBlue() * n;
        return new Color(n3 / 32, n4 / 32, n5 / 32);
    }

    public void move(double d) {
    }
}
