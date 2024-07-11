/*
 * Decompiled with CFR 0.152.
 */
import java.applet.Applet;
import java.awt.Frame;
import java.awt.event.WindowEvent;
import java.awt.event.WindowListener;

public class AppFrame
extends Frame
implements WindowListener {
    Applet applet;

    public AppFrame(Applet applet, String string) {
        super(string);
        this.addWindowListener(this);
        this.applet = applet;
    }

    public void windowDeactivated(WindowEvent windowEvent) {
    }

    public void windowClosing(WindowEvent windowEvent) {
        this.applet.stop();
        System.exit(0);
    }

    public void windowOpened(WindowEvent windowEvent) {
    }

    public void windowClosed(WindowEvent windowEvent) {
    }

    public void windowDeiconified(WindowEvent windowEvent) {
    }

    public void windowActivated(WindowEvent windowEvent) {
    }

    public void windowIconified(WindowEvent windowEvent) {
    }
}
