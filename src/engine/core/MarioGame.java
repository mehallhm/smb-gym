package engine.core;

import java.awt.image.VolatileImage;
import java.util.ArrayList;
import java.awt.*;
import java.awt.event.KeyAdapter;

import javax.swing.JFrame;

// import agents.human.Agent;
// import engine.helper.GameStatus;
import engine.helper.MarioActions;

public class MarioGame {
    /**
     * the maximum time that agent takes for each step
     */
    public static final long maxTime = 40;
    /**
     * extra time before reporting that the agent is taking more time that it should
     */
    public static final long graceTime = 10;
    /**
     * Screen width
     */
    public static final int width = 256;
    /**
     * Screen height
     */
    public static final int height = 256;
    /**
     * Screen width in tiles
     */
    public static final int tileWidth = width / 16;
    /**
     * Screen height in tiles
     */
    public static final int tileHeight = height / 16;
    /**
     * print debug details
     */
    public static final boolean verbose = false;

    /**
     * pauses the whole game at any moment
     */
    public boolean pause = false;

    /**
     * events that kills the player when it happens only care about type and param
     */
    private MarioEvent[] killEvents;

    //visualization
    private JFrame window = null;
    private MarioRender render = null;
    private MarioAgent agent = null;
    public MarioWorld world = null;

    // per loop information to be stored
    public ArrayList<MarioEvent> gameEvents = null;
    public ArrayList<MarioAgentEvent> agentEvents = null;
    public MarioTimer agentTimer = null;
    public VolatileImage renderTarget = null;
    public Graphics backBuffer = null;
    public Graphics currentBuffer = null;
    public long currentTime = 0;

    public boolean visuals = true;




    /**
     * Create a mario game to be played
     */
    public MarioGame() {

    }

    /**
     * Create a mario game with a different forward model where the player on certain event
     *
     * @param killEvents events that will kill the player
     */
    public MarioGame(MarioEvent[] killEvents) {
        this.killEvents = killEvents;
    }

    // private int getDelay(int fps) {
    //     if (fps <= 0) {
    //         return 0;
    //     }
    //     return 1000 / fps;
    // }

    private void setAgent(MarioAgent agent) {
        this.agent = agent;
        if (agent instanceof KeyAdapter) {
            this.render.addKeyListener((KeyAdapter) this.agent);
        }
    }

    // /**
    //  * Play a certain mario level
    //  *
    //  * @param level a string that constitutes the mario level, it uses the same representation as the VGLC but with more details. for more details about each symbol check the json file in the levels folder.
    //  * @param timer number of ticks for that level to be played. Setting timer to anything &lt;=0 will make the time infinite
    //  * @return statistics about the current game
    //  */
    // public MarioResult playGame(String level, int timer) {
    //     return this.runGame(new Agent(), level, timer, 0, true, 30, 2);
    // }

    // /**
    //  * Play a certain mario level
    //  *
    //  * @param level      a string that constitutes the mario level, it uses the same representation as the VGLC but with more details. for more details about each symbol check the json file in the levels folder.
    //  * @param timer      number of ticks for that level to be played. Setting timer to anything &lt;=0 will make the time infinite
    //  * @param marioState the initial state that mario appears in. 0 small mario, 1 large mario, and 2 fire mario.
    //  * @return statistics about the current game
    //  */
    // public MarioResult playGame(String level, int timer, int marioState) {
    //     return this.runGame(new Agent(), level, timer, marioState, true, 30, 2);
    // }

    // /**
    //  * Play a certain mario level
    //  *
    //  * @param level      a string that constitutes the mario level, it uses the same representation as the VGLC but with more details. for more details about each symbol check the json file in the levels folder.
    //  * @param timer      number of ticks for that level to be played. Setting timer to anything &lt;=0 will make the time infinite
    //  * @param marioState the initial state that mario appears in. 0 small mario, 1 large mario, and 2 fire mario.
    //  * @param fps        the number of frames per second that the update function is following
    //  * @return statistics about the current game
    //  */
    // public MarioResult playGame(String level, int timer, int marioState, int fps) {
    //     return this.runGame(new Agent(), level, timer, marioState, true, fps, 2);
    // }

    // /**
    //  * Play a certain mario level
    //  *
    //  * @param level      a string that constitutes the mario level, it uses the same representation as the VGLC but with more details. for more details about each symbol check the json file in the levels folder.
    //  * @param timer      number of ticks for that level to be played. Setting timer to anything &lt;=0 will make the time infinite
    //  * @param marioState the initial state that mario appears in. 0 small mario, 1 large mario, and 2 fire mario.
    //  * @param fps        the number of frames per second that the update function is following
    //  * @param scale      the screen scale, that scale value is multiplied by the actual width and height
    //  * @return statistics about the current game
    //  */
    // public MarioResult playGame(String level, int timer, int marioState, int fps, float scale) {
    //     return this.runGame(new Agent(), level, timer, marioState, true, fps, scale);
    // }

    // /**
    //  * Run a certain mario level with a certain agent
    //  *
    //  * @param agent the current AI agent used to play the game
    //  * @param level a string that constitutes the mario level, it uses the same representation as the VGLC but with more details. for more details about each symbol check the json file in the levels folder.
    //  * @param timer number of ticks for that level to be played. Setting timer to anything &lt;=0 will make the time infinite
    //  * @return statistics about the current game
    //  */
    // public MarioResult runGame(MarioAgent agent, String level, int timer) {
    //     return this.runGame(agent, level, timer, 0, false, 0, 2);
    // }

    // /**
    //  * Run a certain mario level with a certain agent
    //  *
    //  * @param agent      the current AI agent used to play the game
    //  * @param level      a string that constitutes the mario level, it uses the same representation as the VGLC but with more details. for more details about each symbol check the json file in the levels folder.
    //  * @param timer      number of ticks for that level to be played. Setting timer to anything &lt;=0 will make the time infinite
    //  * @param marioState the initial state that mario appears in. 0 small mario, 1 large mario, and 2 fire mario.
    //  * @return statistics about the current game
    //  */
    // public MarioResult runGame(MarioAgent agent, String level, int timer, int marioState) {
    //     return this.runGame(agent, level, timer, marioState, false, 0, 2);
    // }

    // /**
    //  * Run a certain mario level with a certain agent
    //  *
    //  * @param agent      the current AI agent used to play the game
    //  * @param level      a string that constitutes the mario level, it uses the same representation as the VGLC but with more details. for more details about each symbol check the json file in the levels folder.
    //  * @param timer      number of ticks for that level to be played. Setting timer to anything &lt;=0 will make the time infinite
    //  * @param marioState the initial state that mario appears in. 0 small mario, 1 large mario, and 2 fire mario.
    //  * @param visuals    show the game visuals if it is true and false otherwise
    //  * @return statistics about the current game
    //  */
    // public MarioResult runGame(MarioAgent agent, String level, int timer, int marioState, boolean visuals) {
    //     return this.runGame(agent, level, timer, marioState, visuals, visuals ? 30 : 0, 2);
    // }

    // /**
    //  * Run a certain mario level with a certain agent
    //  *
    //  * @param agent      the current AI agent used to play the game
    //  * @param level      a string that constitutes the mario level, it uses the same representation as the VGLC but with more details. for more details about each symbol check the json file in the levels folder.
    //  * @param timer      number of ticks for that level to be played. Setting timer to anything &lt;=0 will make the time infinite
    //  * @param marioState the initial state that mario appears in. 0 small mario, 1 large mario, and 2 fire mario.
    //  * @param visuals    show the game visuals if it is true and false otherwise
    //  * @param fps        the number of frames per second that the update function is following
    //  * @return statistics about the current game
    //  */
    // public MarioResult runGame(MarioAgent agent, String level, int timer, int marioState, boolean visuals, int fps) {
    //     return this.runGame(agent, level, timer, marioState, visuals, fps, 2);
    // }

    // /**
    //  * Run a certain mario level with a certain agent
    //  *
    //  * @param agent      the current AI agent used to play the game
    //  * @param level      a string that constitutes the mario level, it uses the same representation as the VGLC but with more details. for more details about each symbol check the json file in the levels folder.
    //  * @param timer      number of ticks for that level to be played. Setting timer to anything &lt;=0 will make the time infinite
    //  * @param marioState the initial state that mario appears in. 0 small mario, 1 large mario, and 2 fire mario.
    //  * @param visuals    show the game visuals if it is true and false otherwise
    //  * @param fps        the number of frames per second that the update function is following
    //  * @param scale      the screen scale, that scale value is multiplied by the actual width and height
    //  * @return statistics about the current game
    //  */
    // public MarioResult runGame(MarioAgent agent, String level, int timer, int marioState, boolean visuals, int fps, float scale) {
    //     if (visuals) {
    //         this.window = new JFrame("Mario AI Framework");
    //         this.render = new MarioRender(scale);
    //         this.window.setContentPane(this.render);
    //         this.window.pack();
    //         this.window.setResizable(false);
    //         this.window.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    //         this.render.init();
    //         this.window.setVisible(true);
    //     }
    //     this.setAgent(agent);

    //     this.initial(level, timer, marioState, visual);
    //     return this.gameLoop(fps);
    // }

    /**
     * Run a certain mario level with a certain agent
     *
     * @param agent      the current AI agent used to play the game
     * @param level      a string that constitutes the mario level, it uses the same representation as the VGLC but with more details. for more details about each symbol check the json file in the levels folder.
     * @param timer      number of ticks for that level to be played. Setting timer to anything &lt;=0 will make the time infinite
     * @param marioState the initial state that mario appears in. 0 small mario, 1 large mario, and 2 fire mario.
     * @param visuals    show the game visuals if it is true and false otherwise
     * @param fps        the number of frames per second that the update function is following
     * @param scale      the screen scale, that scale value is multiplied by the actual width and height
     * @return statistics about the current game
     */
    public void runGameN(MarioAgent agent, String level, int timer, int marioState, boolean visuals) {
        float scale = 2;
        // int fps = 30;
        // this.visuals = true;
        this.visuals = visuals;
        if (this.window != null) {
            // this.window.dispatchEvent(new WindowEvent(this.window, WindowEvent.WINDOW_CLOSING));
            this.window.setVisible(false);
            this.window.dispose();
        };
        this.render = null;

        if (this.visuals) {
            this.window = new JFrame("Mario AI Framework");
            this.render = new MarioRender(scale);
            this.window.setContentPane(this.render);
            this.window.pack();
            this.window.setResizable(false);
            this.window.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            this.render.init();
            this.window.setVisible(true);
        }
        this.setAgent(agent);

        this.initial(level, timer, marioState);
    }

    // public MarioResult gameLoop(int fps) {

    //     while (this.world.gameStatus == GameStatus.RUNNING) {
    //         step();
    //         //check if delay needed
    //         if (this.getDelay(fps) > 0) {
    //             try {
    //                 this.currentTime += this.getDelay(fps);
    //                 Thread.sleep(Math.max(0, this.currentTime - System.currentTimeMillis()));
    //             } catch (InterruptedException e) {
    //                 break;
    //             }
    //         }
    //     }

    //     return new MarioResult(this.world, this.gameEvents, this.agentEvents);
    // }

    public void initial(String level, int timer, int marioState) {
        // setup world 
        this.world = new MarioWorld(this.killEvents);
        this.world.visuals = this.visuals;
        this.world.initializeLevel(level, 1000 * timer);
        if (this.visuals) {
            this.world.initializeVisuals(this.render.getGraphicsConfiguration());
        }
        this.world.mario.isLarge = marioState > 0;
        this.world.mario.isFire = marioState > 1;
        this.world.update(new boolean[MarioActions.numberOfActions()]);
        this.currentTime = System.currentTimeMillis();

        //initialize graphics
        if (this.visuals) {
            this.renderTarget = this.render.createVolatileImage(MarioGame.width, MarioGame.height);
            this.backBuffer = this.render.getGraphics();
            this.currentBuffer = this.renderTarget.getGraphics();
            this.render.addFocusListener(this.render);
        }

        this.agent.initialize(new MarioForwardModel(this.world.clone()), this.agentTimer);

        this.gameEvents = new ArrayList<>();
        this.agentEvents = new ArrayList<>();
    }

    public void step() {
        if (!this.pause) {
            //get actions
            this.agentTimer = new MarioTimer(MarioGame.maxTime);
            boolean[] actions = this.agent.getActions(new MarioForwardModel(this.world.clone()), this.agentTimer);
            if (MarioGame.verbose) {
                if (this.agentTimer.getRemainingTime() < 0 && Math.abs(this.agentTimer.getRemainingTime()) > MarioGame.graceTime) {
                    System.out.println("The Agent is slowing down the game by: "
                            + Math.abs(this.agentTimer.getRemainingTime()) + " msec.");
                }
            }
            // update world
            this.world.update(actions);
            this.gameEvents.addAll(this.world.lastFrameEvents);
            this.agentEvents.add(new MarioAgentEvent(actions, this.world.mario.x,
                    this.world.mario.y, (this.world.mario.isLarge ? 1 : 0) + (this.world.mario.isFire ? 1 : 0),
                    this.world.mario.onGround, this.world.currentTick));
        }

        //render world
        if (this.visuals) {
            this.render.renderWorld(this.world, this.renderTarget, this.backBuffer, this.currentBuffer);
        }
    }
}
