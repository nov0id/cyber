/*
 * Decompiled with CFR 0.152.
 */
import java.applet.Applet;
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Component;
import java.awt.Container;
import java.awt.FlowLayout;
import java.awt.Label;
import java.awt.Panel;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class Game3D
extends Applet
implements ActionListener {
    static final boolean isFreeware = true;
    MainGame game;
    Label hiScoreLabel;
    Label lblContinue;
    NumberLabel scoreWin;
    static boolean isLocal = false;
    int lang = 0;
    String[] bt1 = new String[]{"Regist your Hi-score", "\u81ea\u5206\u306e\u30cf\u30a4\u30b9\u30b3\u30a2\u306e\u767b\u9332"};
    String[] contMsg = new String[]{"Push [C] key to start from this stage!!", "\u9014\u4e2d\u304b\u3089\u59cb\u3081\u308b\u5834\u5408\u306f [C]key \u3092\u62bc\u3057\u3066\u4e0b\u3055\u3044!!"};
    String[] toStartMsg = new String[]{"Click this game screen or push [space] key!!", "\u30af\u30ea\u30c3\u30af\u3059\u308b\u304b\u3001[space]key\u3092\u62bc\u3057\u3066\u4e0b\u3055\u3044"};
    String[] clickMsg = new String[]{"Click!!", "\u30af\u30ea\u30c3\u30af\u3057\u3066\u4e0b\u3055\u3044"};

    public void stop() {
        this.game.stop();
    }

    public static void main(String[] stringArray) {
        isLocal = true;
        Game3D game3D = new Game3D();
        AppFrame appFrame = new AppFrame(game3D, "Jet slalom");
        appFrame.show();
        appFrame.setLayout(new BorderLayout());
        appFrame.add("Center", game3D);
        game3D.init();
        appFrame.validate();
        appFrame.pack();
        game3D.start();
    }

    public void actionPerformed(ActionEvent actionEvent) {
    }

    public void start() {
        this.game.start();
        this.game.startGame(1, false);
    }

    public void init() {
        Object object;
        if (!isLocal) {
            object = this.getParameter("LANG");
            if (!isLocal && object != null && ((String)object).equals("JP")) {
                this.lang = 1;
            }
        }
        this.setLayout(new BorderLayout());
        this.setBackground(new Color(0, 160, 160));
        this.setForeground(Color.white);
        this.scoreWin = new NumberLabel(64, 16);
        this.lblContinue = new Label("            ");
        object = new Panel();
        ((Component)object).setForeground(Color.white);
        ((Container)object).setLayout(new FlowLayout());
        ((Container)object).add(new Label("Score:"));
        ((Container)object).add(this.scoreWin);
        ((Container)object).add(new Label("Continue penalty:"));
        ((Container)object).add(this.lblContinue);
        this.add("North", (Component)object);
        this.hiScoreLabel = new Label("Your Hi-score:0         ");
        this.add("South", this.hiScoreLabel);
        this.game = new MainGame(this);
        this.add("Center", this.game);
        this.game.init();
        this.game.requestFocus();
    }
}
