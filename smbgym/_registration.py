from gym.envs.registration import register
import gym

register(
    id='Mario-v0',
    entry_point='smbgym:Env',
    max_episode_steps=999999,
)

make = gym.make