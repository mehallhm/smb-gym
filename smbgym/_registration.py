from gym.envs.registration import register

register(
    id='gym_examples/GridWorld-v0',
    entry_point='smbgym.env:Env',
    max_episode_steps=999999,
)