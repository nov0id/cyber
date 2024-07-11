/*
 * Decompiled with CFR 0.152.
 */
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;

public class GameRecorder {
    public static final int LEFT = 1;
    public static final int RIGHT = 2;
    private RandomGenerator random;
    private int seed;
    private int[] data = new int[2048];
    private int pos;
    private int maxpos = 0;
    public int startScore;
    public int startRound;

    public void writeStatus(int n) {
        if (this.pos >= this.data.length * 16) {
            return;
        }
        int n2 = this.pos / 16;
        this.data[n2] = this.data[n2] | n << this.pos % 16 * 2;
        ++this.pos;
        if (this.pos > this.maxpos) {
            this.maxpos = this.pos;
        }
    }

    public int readStatus() {
        if (this.pos >= this.data.length * 16) {
            return 0;
        }
        int n = this.data[this.pos / 16] >>> this.pos % 16 * 2;
        ++this.pos;
        return n & 3;
    }

    public GameRecorder() {
        this.seed = (int)System.currentTimeMillis();
        this.random = new RandomGenerator(this.seed);
    }

    public void load(InputStream inputStream) throws IOException {
        DataInputStream dataInputStream = new DataInputStream(inputStream);
        this.seed = dataInputStream.readInt();
        this.maxpos = dataInputStream.readInt();
        this.startRound = dataInputStream.readInt();
        this.startScore = dataInputStream.readInt();
        int n = 0;
        while (n < this.maxpos) {
            this.data[n] = dataInputStream.readInt();
            ++n;
        }
    }

    public void save(OutputStream outputStream) throws IOException {
        DataOutputStream dataOutputStream = new DataOutputStream(outputStream);
        dataOutputStream.writeInt(this.seed);
        dataOutputStream.writeInt(this.maxpos);
        dataOutputStream.writeInt(this.startRound);
        dataOutputStream.writeInt(this.startScore);
        int n = 0;
        while (n < this.maxpos) {
            dataOutputStream.writeInt(this.data[n]);
            ++n;
        }
    }

    public int getRandom() {
        return this.random.nextInt() & Integer.MAX_VALUE;
    }

    public void toStart() {
        this.pos = 0;
        this.random.setSeed(this.seed);
    }
}
