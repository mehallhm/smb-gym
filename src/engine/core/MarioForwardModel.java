package engine.core;

import java.util.ArrayList;

import engine.helper.EventType;
import engine.helper.GameStatus;
import engine.helper.SpriteType;

public class MarioForwardModel {
    private static final int OBS_SCENE_SHIFT = 16;

    // Generic values
    public static final int OBS_NONE = 0;
    public static final int OBS_UNDEF = -42;

    // Common between scene detail level 0 and scene detail level 1
    public static final int OBS_SOLID = OBS_SCENE_SHIFT + 1;
    public static final int OBS_BRICK = OBS_SCENE_SHIFT + 6;
    public static final int OBS_QUESTION_BLOCK = OBS_SCENE_SHIFT + 8;
    public static final int OBS_COIN = OBS_SCENE_SHIFT + 15;
    // Scene detail level 0
    public static final int OBS_PYRAMID_SOLID = OBS_SCENE_SHIFT + 2;
    public static final int OBS_PIPE_BODY_RIGHT = OBS_SCENE_SHIFT + 21;
    public static final int OBS_PIPE_BODY_LEFT = OBS_SCENE_SHIFT + 20;
    public static final int OBS_PIPE_TOP_RIGHT = OBS_SCENE_SHIFT + 19;
    public static final int OBS_PIPE_TOP_LEFT = OBS_SCENE_SHIFT + 18;
    public static final int OBS_USED_BLOCK = OBS_SCENE_SHIFT + 14;
    public static final int OBS_BULLET_BILL_BODY = OBS_SCENE_SHIFT + 5;
    public static final int OBS_BULLET_BILL_NECT = OBS_SCENE_SHIFT + 4;
    public static final int OBS_BULLET_BILL_HEAD = OBS_SCENE_SHIFT + 3;
    public static final int OBS_BACKGROUND = OBS_SCENE_SHIFT + 47;
    public static final int OBS_PLATFORM_SINGLE = OBS_SCENE_SHIFT + 43;
    public static final int OBS_PLATFORM_LEFT = OBS_SCENE_SHIFT + 44;
    public static final int OBS_PLATFORM_RIGHT = OBS_SCENE_SHIFT + 45;
    public static final int OBS_PLATFORM_CENTER = OBS_SCENE_SHIFT + 46;
    // Scene detail level 1
    public static final int OBS_PLATFORM = OBS_SCENE_SHIFT + 43;
    public static final int OBS_CANNON = OBS_SCENE_SHIFT + 3;
    public static final int OBS_PIPE = OBS_SCENE_SHIFT + 18;
    // Scene detail level 2
    public static final int OBS_SCENE_OBJECT = OBS_SCENE_SHIFT + 84;

    // Common between enemies detail level 0 and 1
    public static final int OBS_FIREBALL = 16;
    // Enemies Detail 0
    public static final int OBS_GOOMBA = 2;
    public static final int OBS_GOOMBA_WINGED = 3;
    public static final int OBS_RED_KOOPA = 4;
    public static final int OBS_RED_KOOPA_WINGED = 5;
    public static final int OBS_GREEN_KOOPA = 6;
    public static final int OBS_GREEN_KOOPA_WINGED = 7;
    public static final int OBS_SPIKY = 8;
    public static final int OBS_SPIKY_WINGED = 9;
    public static final int OBS_BULLET_BILL = 10;
    public static final int OBS_ENEMY_FLOWER = 11;
    public static final int OBS_MUSHROOM = 12;
    public static final int OBS_FIRE_FLOWER = 13;
    public static final int OBS_SHELL = 14;
    public static final int OBS_LIFE_MUSHROOM = 15;
    // Enemies Detail 1
    public static final int OBS_STOMPABLE_ENEMY = 2;
    public static final int OBS_NONSTOMPABLE_ENEMY = 8;
    public static final int OBS_SPECIAL_ITEM = 12;
    // Enemies Detail 2
    public static final int OBS_ENEMY = 1;

    public static int getSpriteTypeGeneralization(SpriteType sprite) {
        switch (sprite) {
            case MARIO:
                return OBS_NONE;
            default:
                return sprite.getValue();
        }
    }

    public static int getBlockValueGeneralization(int tile) {
        if (tile == 0) {
            return OBS_NONE;
        }
        switch (tile) {
            // invisble blocks
            case 48:
            case 49:
                // body for jumpthrough platform
            case 47:
                return OBS_NONE;
            // solid blocks
            case 1:
            case 2:
            case 14:
            case 4:
            case 5:
                return OBS_SOLID;
            // bullet bill blocks
            case 3:
                return OBS_CANNON;
            // pipe blocks
            case 18:
            case 19:
            case 20:
            case 21:
                return OBS_PIPE;
            // brick blocks
            case 6:
            case 7:
            case 50:
            case 51:
                return OBS_BRICK;
            // ? blocks
            case 8:
            case 11:
                return OBS_QUESTION_BLOCK;
            // coin
            case 15:
                return OBS_COIN;
            // Jump through platforms
            case 44:
            case 45:
            case 46:
                return OBS_PLATFORM;
            case 39:
            case 40:
                return tile + OBS_SCENE_SHIFT;
        }
        return OBS_NONE;
        // return tile + OBS_SCENE_SHIFT;
    }

    /**
     * The width of the observation grid
     */
    public final int obsGridWidth = MarioGame.tileWidth;
    /**
     * The height of the observation grid
     */
    public final int obsGridHeight = MarioGame.tileHeight;

    private MarioWorld world;

    // stats
    private int fallKill;
    private int stompKill;
    private int fireKill;
    private int shellKill;
    private int mushrooms;
    private int flowers;
    private int breakBlock;

    /**
     * Create a forward model object
     *
     * @param world the current level world that is being used. This class hides the
     *              world object so the agents won't cheat.
     */
    public MarioForwardModel(MarioWorld world) {
        this.world = world;
    }

    /**
     * Create a clone from the current forward model state
     *
     * @return a clone from the current forward model state
     */
    public MarioForwardModel clone() {
        MarioForwardModel model = new MarioForwardModel(this.world.clone());
        model.fallKill = this.fallKill;
        model.stompKill = this.stompKill;
        model.fireKill = this.fireKill;
        model.shellKill = this.shellKill;
        model.mushrooms = this.mushrooms;
        model.flowers = this.flowers;
        model.breakBlock = this.breakBlock;
        return model;
    }

    /**
     * Advance the forward model using the action array
     *
     * @param actions a list of all the button states
     */
    public void advance(boolean[] actions) {
        this.world.update(actions);
        for (MarioEvent e : this.world.lastFrameEvents) {
            if (e.getEventType() == EventType.FIRE_KILL.getValue()) {
                this.fireKill += 1;
            }
            if (e.getEventType() == EventType.STOMP_KILL.getValue()) {
                this.stompKill += 1;
            }
            if (e.getEventType() == EventType.FALL_KILL.getValue()) {
                this.fallKill += 1;
            }
            if (e.getEventType() == EventType.SHELL_KILL.getValue()) {
                this.shellKill += 1;
            }
            if (e.getEventType() == EventType.COLLECT.getValue()) {
                if (e.getEventParam() == SpriteType.FIRE_FLOWER.getValue()) {
                    this.flowers += 1;
                }
                if (e.getEventParam() == SpriteType.MUSHROOM.getValue()) {
                    this.mushrooms += 1;
                }
            }
            if (e.getEventType() == EventType.BUMP.getValue() && e.getEventParam() == OBS_BRICK
                    && e.getMarioState() > 0) {
                this.breakBlock += 1;
            }
        }
    }

    /**
     * Get the current state of the running game
     *
     * @return GameStatus the current state (WIN, LOSE, TIME_OUT, RUNNING)
     */
    public GameStatus getGameStatus() {
        return this.world.gameStatus;
    }

    /**
     * The percentage of distance traversed between mario and the goal
     *
     * @return value between 0 to 1 to indicate the percentage of distance traversed
     */
    public float getCompletionPercentage() {
        return this.world.mario.x / (this.world.level.exitTileX * 16);
    }

    /**
     * Get the current level dimensions
     *
     * @return the first value is level width and second is level height
     */
    public float[] getLevelFloatDimensions() {
        return new float[]{this.world.level.width, this.world.level.height};
    }

    /**
     * Get the remaining time before the game timesout
     *
     * @return the number of time ticks before timeout each frame removes 30 frames
     */
    public int getRemainingTime() {
        return this.world.currentTimer;
    }

    /**
     * Get mario position
     *
     * @return the actual mario position in the current state
     */
    public float[] getMarioFloatPos() {
        return new float[]{this.world.mario.x, this.world.mario.y};
    }

    /**
     * Get mario velocity
     *
     * @return the actual mario velocity in the current state
     */
    public float[] getMarioFloatVelocity() {
        return new float[]{this.world.mario.xa, this.world.mario.ya};
    }

    /**
     * If mario can press the jump button while in the air to reach higher areas
     *
     * @return true if the agent can press the button longer and false otherwise
     */
    public boolean getMarioCanJumpHigher() {
        return this.world.mario.jumpTime > 0;
    }

    /**
     * Get the current mario mode
     *
     * @return the current mario mode (0-small, 1-large, 2-fire)
     */
    public int getMarioMode() {
        int value = 0;
        if (this.world.mario.isLarge) {
            value = 1;
        }
        if (this.world.mario.isFire) {
            value = 2;
        }
        return value;
    }

    /**
     * Get to know if mario is touching the ground.
     *
     * @return true if mario is touching the ground and false otherwise
     */
    public boolean isMarioOnGround() {
        return this.world.mario.onGround;
    }

    /**
     * Get to know if mario is able to jump
     *
     * @return true if mario can jump and false otherwise
     */
    public boolean mayMarioJump() {
        return this.world.mario.mayJump;
    }

    /**
     * Get a 3x float list that contain the type of enemies, x position, y position
     *
     * @return an array of 3 floats that contain the enemy type, x position, y
     * position for each enemy sprite
     */
    public float[] getEnemiesFloatPos() {
        ArrayList<MarioSprite> enemiesAlive = this.world.getEnemies();
        float[] enemyPos = new float[enemiesAlive.size() * 3];
        for (int i = 0; i < enemiesAlive.size(); i++) {
            enemyPos[3 * i] = enemiesAlive.get(i).type.getValue();
            enemyPos[3 * i + 1] = enemiesAlive.get(i).x;
            enemyPos[3 * i + 2] = enemiesAlive.get(i).y;
        }
        return enemyPos;
    }

    /**
     * get the number of enemies killed in the game
     *
     * @return number of enemies killed in the game
     */
    public int getKillsTotal() {
        return this.fallKill + this.fireKill + this.shellKill + this.stompKill;
    }

    /**
     * get the number of enemies killed by fireballs
     *
     * @return number of enemies killed by fireballs
     */
    public int getKillsByFire() {
        return this.fireKill;
    }

    /**
     * get the number of enemies killed by stomping
     *
     * @return number of enemies killed by stomping
     */
    public int getKillsByStomp() {
        return this.stompKill;
    }

    /**
     * get the number of enemies killed by a koopa shell
     *
     * @return number of enemies killed by a koopa shell
     */
    public int getKillsByShell() {
        return this.shellKill;
    }

    /**
     * get the number of enemies that fell from the game screen
     *
     * @return the number of enemies that fell from the game screen
     */
    public int getKillsByFall() {
        return this.fallKill;
    }

    /**
     * get the number 100 coins collected by mario
     *
     * @return number of 100 coins collected by mario
     */
    public int getNumLives() {
        return this.world.lives;
    }

    /**
     * get the number of mushroom collected by mario
     *
     * @return the number of collected mushrooms by mario
     */
    public int getNumCollectedMushrooms() {
        return this.mushrooms;
    }

    /**
     * get the number of fire flowers collected by mario
     *
     * @return the number of collected fire flowers by mario
     */
    public int getNumCollectedFireflower() {
        return this.flowers;
    }

    /**
     * get the number of coins collected by mario
     *
     * @return the number of collected coins by mario
     */
    public int getNumCollectedCoins() {
        return this.world.coins;
    }

    /**
     * get the number of destroyed bricks by large or fire mario
     *
     * @return the number of destroyed bricks by large or fire mario
     */
    public int getNumDestroyedBricks() {
        return this.breakBlock;
    }

    /**
     * Get the tile location of mario with respect to the screen
     *
     * @return the x and y location of mario on the screen as tile values
     */
    public int[] getMarioScreenTilePos() {
        return new int[]{(int) ((this.world.mario.x - this.world.cameraX) / 16), (int) (this.world.mario.y / 16)};
    }
}
