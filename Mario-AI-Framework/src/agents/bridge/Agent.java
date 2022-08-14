package agents.bridge;

import engine.core.MarioAgent;
import engine.core.MarioForwardModel;
import engine.core.MarioTimer;
import engine.helper.MarioActions;

public class Agent implements MarioAgent {
	public boolean[] actions = null;

    public void left() {
        this.actions[MarioActions.LEFT.getValue()] = true;
    }

    public void right() {
        this.actions[MarioActions.RIGHT.getValue()] = true;
    }

    public void down() {
        this.actions[MarioActions.DOWN.getValue()] = true;
    }

    public void speed() {
        this.actions[MarioActions.SPEED.getValue()] = true;
    }

    public void jump() {
        this.actions[MarioActions.JUMP.getValue()] = true;
    }

    public void clear() {
        this.actions[MarioActions.LEFT.getValue()] = false;
        this.actions[MarioActions.RIGHT.getValue()] = false;
        this.actions[MarioActions.DOWN.getValue()] = false;
        this.actions[MarioActions.SPEED.getValue()] = false;
        this.actions[MarioActions.JUMP.getValue()] = false;
    }

    @Override
    public void initialize(MarioForwardModel model, MarioTimer timer) {
        actions = new boolean[MarioActions.numberOfActions()];
    }

    @Override
    public boolean[] getActions(MarioForwardModel model, MarioTimer timer) {
        return actions;
    }

    @Override
    public String getAgentName() {
        return "bridgeAgent";
    }
}
