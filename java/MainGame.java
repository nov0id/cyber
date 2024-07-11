/*
 * Decompiled with CFR 0.152.
 */
import java.applet.AudioClip;
import java.awt.Canvas;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.Image;
import java.awt.MediaTracker;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.awt.event.MouseMotionListener;
import java.net.MalformedURLException;
import java.net.URL;

class MainGame
extends Canvas
implements Runnable,
MouseListener,
MouseMotionListener,
KeyListener {
    static double[] si = new double[128];
    static double[] co = new double[128];
    DrawEnv env = new DrawEnv();
    Ground ground = new Ground();
    TimerNotifier timer;
    GameRecorder recorder = new GameRecorder();
    GameRecorder hiscoreRec = null;
    ObstacleCollection obstacles = new ObstacleCollection();
    double vx = 0.0;
    double mywidth = 0.7;
    int mywidth2;
    int score;
    int prevScore;
    int hiscore;
    int shipCounter;
    int contNum;
    int gameMode = 2;
    static final int PLAY_MODE = 0;
    static final int TITLE_MODE = 1;
    static final int DEMO_MODE = 2;
    boolean isContinue = false;
    boolean registMode = false;
    int width;
    int height;
    int centerX;
    int centerY;
    int mouseX = 0;
    int mouseY = 0;
    boolean isInPage = false;
    Thread gameThread;
    Image img;
    Image myImg;
    Image myImg2;
    Image myRealImg;
    Image myRealImg2;
    Graphics gra;
    Graphics thisGra;
    MediaTracker tracker;
    AudioClip auBomb = null;
    boolean isLoaded = false;
    int round;
    RoundManager[] rounds = new RoundManager[]{new NormalRound(8000, new Color(0, 160, 255), new Color(0, 200, 64), 4), new NormalRound(12000, new Color(240, 160, 160), new Color(64, 180, 64), 3), new NormalRound(25000, Color.black, new Color(0, 128, 64), 2), new RoadRound(40000, new Color(0, 180, 240), new Color(0, 200, 64), false), new RoadRound(100000, Color.lightGray, new Color(64, 180, 64), true), new NormalRound(1000000, Color.black, new Color(0, 128, 64), 1)};
    boolean rFlag = false;
    boolean lFlag = false;
    boolean spcFlag = false;
    Game3D parent;
    boolean isFocus = true;
    boolean isFocus2 = true;
    boolean scFlag = true;
    Font titleFont;
    Font normalFont;
    StringObject title;
    StringObject author;
    StringObject startMsg;
    StringObject contMsg;
    StringObject clickMsg;
    StringObject hpage;
    int damaged;
    private char[] memInfo = new char[8];
    private Runtime runtime = Runtime.getRuntime();

    public void stop() {
        if (this.gameThread != null) {
            this.gameThread.stop();
        }
        this.gameThread = null;
        this.registMode = false;
        this.gameMode = 1;
        this.timer.interrupt();
    }

    void keyEvent(int n, boolean bl) {
        if (n == 39 || n == 76) {
            this.rFlag = bl;
        }
        if (n == 37 || n == 74) {
            this.lFlag = bl;
        }
        if (n == 65) {
            this.spcFlag = bl;
        }
        if (!bl) {
            return;
        }
        if (n == 71) {
            System.gc();
        }
        if (this.gameMode != 0 && (n == 32 || n == 67)) {
            this.startGame(0, n == 67);
        }
        if (this.gameMode == 1 && n == 68 && this.hiscoreRec != null) {
            this.startGame(2, false);
        }
        if (this.gameMode != 0 && n == 84) {
            this.prevScore = 110000;
            this.contNum = 100;
            this.startGame(0, true);
        }
    }

    public void mouseClicked(MouseEvent mouseEvent) {
    }

    public void mousePressed(MouseEvent mouseEvent) {
        int n = mouseEvent.getModifiers();
        if ((n & 4) != 0) {
            this.rFlag = true;
            this.lFlag = false;
        } else if ((n & 0x10) != 0) {
            this.rFlag = false;
            this.lFlag = true;
        }
        if (this.gameMode == 0) {
            return;
        }
        if (!this.isFocus2) {
            this.isFocus2 = true;
            return;
        }
        if (this.isInPage && this.gameMode == 1) {
            try {
                this.parent.getAppletContext().showDocument(new URL("http://www.kdn.gr.jp/~shii/"));
                return;
            }
            catch (MalformedURLException malformedURLException) {
                return;
            }
        }
        this.startGame(0, false);
    }

    public void mouseDragged(MouseEvent mouseEvent) {
    }

    void keyOperate() {
        boolean bl = this.rFlag;
        boolean bl2 = this.lFlag;
        if (this.gameMode == 0) {
            int n = 0;
            if (bl) {
                n |= 2;
            }
            if (bl2) {
                n |= 1;
            }
            this.recorder.writeStatus(n);
        } else if (this.gameMode == 2) {
            int n = this.hiscoreRec.readStatus();
            bl = (n & 2) != 0;
            boolean bl3 = bl2 = (n & 1) != 0;
        }
        if (this.damaged == 0 && (this.gameMode == 0 || this.gameMode == 2)) {
            if (bl) {
                this.vx -= 0.1;
            }
            if (bl2) {
                this.vx += 0.1;
            }
            if (this.vx < -0.6) {
                this.vx = -0.6;
            }
            if (this.vx > 0.6) {
                this.vx = 0.6;
            }
        }
        if (!bl2 && !bl) {
            if (this.vx < 0.0) {
                this.vx += 0.025;
                if (this.vx > 0.0) {
                    this.vx = 0.0;
                }
            }
            if (this.vx > 0.0) {
                this.vx -= 0.025;
                if (this.vx < 0.0) {
                    this.vx = 0.0;
                }
            }
        }
    }

    public MainGame(Game3D game3D) {
        this.parent = game3D;
        this.addKeyListener(this);
        this.addMouseListener(this);
        this.addMouseMotionListener(this);
        int n = 1;
        while (n < this.rounds.length) {
            this.rounds[n].setPrevRound(this.rounds[n - 1]);
            ++n;
        }
    }

    public void mouseReleased(MouseEvent mouseEvent) {
        this.rFlag = false;
        this.lFlag = false;
    }

    public void mouseMoved(MouseEvent mouseEvent) {
        this.mouseX = mouseEvent.getX();
        this.mouseY = mouseEvent.getY();
    }

    public void keyTyped(KeyEvent keyEvent) {
    }

    public void keyPressed(KeyEvent keyEvent) {
        this.keyEvent(keyEvent.getKeyCode(), true);
    }

    public void paint(Graphics graphics) {
        if (this.registMode) {
            graphics.setColor(Color.lightGray);
            graphics.fill3DRect(0, 0, this.width, this.height, true);
            graphics.setColor(Color.black);
            graphics.drawString("Wait a moment!!", this.centerX - 32, this.centerY + 8);
            return;
        }
        if (this.img != null) {
            graphics.drawImage(this.img, 0, 0, this);
        }
    }

    private void drawMemInfo(Graphics graphics) {
        int n = (int)this.runtime.freeMemory();
        int n2 = 7;
        do {
            int n3 = n % 10;
            n /= 10;
            this.memInfo[n2] = (char)(48 + n3);
        } while (--n2 >= 0);
        graphics.setColor(Color.red);
        graphics.drawChars(this.memInfo, 0, 8, 0, 32);
    }

    void moveObstacle() {
        GameRecorder gameRecorder = this.recorder;
        if (this.gameMode == 2) {
            gameRecorder = this.hiscoreRec;
        }
        int n = (int)(Math.abs(this.vx) * 100.0);
        this.env.nowSin = si[n];
        this.env.nowCos = co[n];
        if (this.vx > 0.0) {
            this.env.nowSin = -this.env.nowSin;
        }
        Obstacle obstacle = this.obstacles.head.next;
        while (obstacle != this.obstacles.tail) {
            Obstacle obstacle2 = obstacle.next;
            obstacle.move(this.vx, 0.0, -1.0);
            DPoint3[] dPoint3Array = obstacle.points;
            if (dPoint3Array[0].z <= 1.1) {
                double d = this.mywidth * this.env.nowCos;
                if (-d < dPoint3Array[2].x && dPoint3Array[0].x < d) {
                    ++this.damaged;
                }
                obstacle.release();
            }
            obstacle = obstacle2;
        }
        this.rounds[this.round].move(this.vx);
        this.rounds[this.round].generateObstacle(this.obstacles, gameRecorder);
    }

    void putbomb() {
        if (this.damaged > 20) {
            this.endGame();
            return;
        }
        if (this.damaged == 1 && this.auBomb != null) {
            this.auBomb.play();
        }
        this.gra.setColor(new Color(255, 255 - this.damaged * 12, 240 - this.damaged * 12));
        int n = this.damaged * 8 * this.width / 320;
        int n2 = this.damaged * 4 * this.height / 200;
        this.gra.fillOval(this.centerX - n, 186 * this.height / 200 - n2, n * 2, n2 * 2);
        ++this.damaged;
    }

    void putExtra() {
    }

    void demo() {
        this.vx = 0.0;
        this.hpage.isUnderLine = true;
        this.title.draw(this.gra, null);
        this.startMsg.draw(this.gra, null);
        this.author.draw(this.gra, null);
        if (this.hpage.hitTest(this.mouseX, this.mouseY)) {
            this.hpage.setColor(Color.white);
            this.isInPage = true;
        } else {
            this.isInPage = false;
            this.hpage.setColor(Color.black);
        }
        this.hpage.draw(this.gra, null);
        if (this.rounds[0].isNextRound(this.prevScore)) {
            this.contMsg.draw(this.gra, null);
        }
        if (!this.isFocus) {
            this.clickMsg.draw(this.gra, null);
        }
    }

    private Image loadImage(String string) {
        Image image = Game3D.isLocal ? this.getToolkit().getImage(ClassLoader.getSystemResource(string)) : this.parent.getImage(this.parent.getCodeBase(), string);
        this.tracker.addImage(image, 0);
        return image;
    }

    public void mouseEntered(MouseEvent mouseEvent) {
    }

    public void mouseExited(MouseEvent mouseEvent) {
    }

    public void keyReleased(KeyEvent keyEvent) {
        this.keyEvent(keyEvent.getKeyCode(), false);
    }

    void gotoRank() {
    }

    public void start() {
        this.timer = new TimerNotifier(55);
        this.gameThread = new Thread(this);
        this.gameThread.start();
    }

    public Dimension getPreferredSize() {
        return new Dimension(this.width, this.height);
    }

    public void startGame(int n, boolean bl) {
        if (this.gameMode == 0) {
            return;
        }
        this.vx = 0.0;
        if (n == 0 || n == 2) {
            if (n == 2 && this.hiscoreRec == null) {
                return;
            }
            this.gameMode = n;
            if (n == 0) {
                this.recorder = new GameRecorder();
            } else {
                this.hiscoreRec.toStart();
            }
        } else {
            this.gameMode = 1;
        }
        this.obstacles.removeAll();
        int n2 = 0;
        while (n2 < this.rounds.length) {
            this.rounds[n2].init();
            ++n2;
        }
        this.damaged = 0;
        this.round = 0;
        this.score = 0;
        this.vx = 0.0;
        if (bl) {
            while (this.prevScore >= this.rounds[this.round].getNextRoundScore()) {
                ++this.round;
            }
            if (this.round > 0) {
                this.score = this.rounds[this.round - 1].getNextRoundScore();
                ++this.contNum;
            }
        } else {
            this.contNum = 0;
        }
        if (n == 2) {
            this.round = this.hiscoreRec.startRound;
            this.score = this.hiscoreRec.startScore;
        } else {
            this.recorder.startRound = this.round;
            this.recorder.startScore = this.score;
        }
        this.parent.lblContinue.setText("" + this.contNum * 1000);
    }

    public void run() {
        this.thisGra = this.getGraphics();
        this.obstacles.removeAll();
        int n = 0;
        while (n < this.rounds.length) {
            this.rounds[n].init();
            ++n;
        }
        this.damaged = 0;
        this.round = 0;
        this.score = 0;
        this.vx = 0.0;
        this.gameMode = 1;
        while (true) {
            if (this.rounds[this.round].isNextRound(this.score)) {
                ++this.round;
            }
            this.keyOperate();
            this.moveObstacle();
            this.prt();
            this.putExtra();
            this.thisGra.drawImage(this.img, 0, 0, null);
            this.getToolkit().sync();
            if (this.spcFlag) continue;
            this.timer.wait1step();
        }
    }

    public void init() {
        this.width = 320;
        this.height = 200;
        this.centerX = this.width / 2;
        this.centerY = this.height / 2;
        this.env.width = this.width;
        this.env.height = this.height;
        this.img = this.createImage(this.width, this.height);
        this.gra = this.img.getGraphics();
        this.gra.setColor(new Color(0, 128, 128));
        this.gra.fillRect(0, 0, this.width, this.height);
        int n = 0;
        do {
            MainGame.si[n] = Math.sin(Math.PI * (double)n / 75.0 / 6.0);
            MainGame.co[n] = Math.cos(Math.PI * (double)n / 75.0 / 6.0);
        } while (++n < 128);
        this.mywidth2 = (int)((double)this.width * this.mywidth * 120.0 / 1.6 / 320.0);
        if (!Game3D.isLocal) {
            this.auBomb = this.parent.getAudioClip(this.parent.getCodeBase(), "bomb.au");
        }
        this.tracker = new MediaTracker(this.parent);
        this.myImg = this.loadImage("jiki.gif");
        this.myImg2 = this.loadImage("jiki2.gif");
        try {
            this.tracker.waitForAll();
        }
        catch (InterruptedException interruptedException) {}
        this.myRealImg = this.myImg.getScaledInstance(this.mywidth2 * 2, this.mywidth2 * 16 / 52, 4);
        this.myRealImg2 = this.myImg2.getScaledInstance(this.mywidth2 * 2, this.mywidth2 * 16 / 52, 4);
        this.titleFont = new Font("TimesRoman", 1, this.width * 32 / 320 + 4);
        this.normalFont = new Font("TimesRoman", 0, 12);
        this.title = new StringObject(this.titleFont, Color.white, "Jet slalom", this.width / 2, this.centerY - 20 * this.width / 320);
        this.author = new StringObject(this.normalFont, Color.black, "Programed by MR-C", this.centerX, this.centerY + 68);
        this.startMsg = new StringObject(this.normalFont, Color.black, this.parent.toStartMsg[this.parent.lang], this.centerX, this.centerY + 24);
        this.contMsg = new StringObject(this.normalFont, Color.black, this.parent.contMsg[this.parent.lang], this.centerX, this.centerY + 44);
        this.clickMsg = new StringObject(this.normalFont, Color.red, this.parent.clickMsg[this.parent.lang], this.centerX, this.centerY);
        this.hpage = new StringObject(this.normalFont, Color.black, "http://www.kdn.gr.jp/~shii/", this.centerX, this.centerY + 86);
    }

    void prt() {
        this.gra.setColor(this.rounds[this.round].getSkyColor());
        this.gra.fillRect(0, 0, this.width, this.height);
        if (this.gameMode == 0) {
            this.score += 20;
            if (this.scFlag) {
                this.parent.scoreWin.setNum(this.score);
            }
        }
        this.scFlag = !this.scFlag;
        this.ground.color = this.rounds[this.round].getGroundColor();
        this.ground.draw(this.gra, this.env);
        this.obstacles.draw(this.gra, this.env);
        ++this.shipCounter;
        if (this.gameMode != 1) {
            int n = 24 * this.height / 200;
            Image image = this.myRealImg;
            if (this.shipCounter % 4 > 1) {
                image = this.myRealImg2;
            }
            if (this.shipCounter % 12 > 6) {
                n = 22 * this.height / 200;
            }
            if (this.score < 200) {
                n = (12 + this.score / 20) * this.height / 200;
            }
            this.gra.drawImage(image, this.centerX - this.mywidth2, this.height - n, null);
            if (this.damaged > 0) {
                this.putbomb();
            }
        }
        if (this.gameMode == 1) {
            this.demo();
        }
    }

    void endGame() {
        this.parent.scoreWin.setNum(this.score);
        if (this.gameMode == 0) {
            this.prevScore = this.score;
        }
        if (this.score - this.contNum * 1000 > this.hiscore && this.gameMode == 0) {
            this.hiscore = this.score - this.contNum * 1000;
            this.hiscoreRec = this.recorder;
        }
        this.parent.hiScoreLabel.setText("Your Hi-score:" + this.hiscore);
        this.gameMode = 1;
    }
}
