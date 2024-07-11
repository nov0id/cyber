/*
 * Decompiled with CFR 0.152.
 */
public class RandomGenerator {
    private int seed;

    public RandomGenerator(int n) {
        this.seed = n;
    }

    public void setSeed(int n) {
        this.seed = n;
    }

    public int nextInt() {
        this.seed = this.seed * 1593227 + 13;
        return this.seed >>> 16;
    }
}
