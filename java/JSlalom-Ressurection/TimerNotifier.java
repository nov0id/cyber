/*
 * Decompiled with CFR 0.152.
 */
public class TimerNotifier
extends Thread {
    private volatile int interval;
    private volatile boolean notifyFlag = false;

    public TimerNotifier(int n) {
        this.interval = n;
        this.setName("TimerNotifier");
        System.out.println(10);
        this.setPriority(10);
        this.start();
    }

    public void setInterval(int n) {
        this.interval = n;
    }

    public synchronized void wait1step() {
        try {
            if (!this.notifyFlag) {
                this.wait();
            }
        }
        catch (InterruptedException interruptedException) {}
        this.notifyFlag = false;
    }

    public void run() {
        while (true) {
            TimerNotifier timerNotifier = this;
            synchronized (timerNotifier) {
                this.notifyFlag = true;
                this.notifyAll();
                Object var2_2 = null;
            }
            try {
                Thread.sleep(this.interval);
            }
            catch (InterruptedException interruptedException) {
                return;
            }
        }
    }
}
