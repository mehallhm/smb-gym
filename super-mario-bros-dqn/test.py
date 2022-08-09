import numpy as np
import torch
from core.constants import PRETRAINED_MODELS
from core.model import CNNDQN
from core.wrappers import wrap_environment
from os.path import join

import sys

def test(environment, action_space, iteration):
    flag = False
    env = wrap_environment(environment, action_space, iteration=iteration)
    net = CNNDQN(env.observation_space.shape, env.action_space.n)
    net.load_state_dict(torch.load(join(PRETRAINED_MODELS,
                                        '%s.dat' % environment)))

    total_reward = 0.0
    state = env.reset()
    while True:
        state_v = torch.tensor(np.array([state], copy=False))
        q_vals = net(state_v).data.numpy()[0]
        action = np.argmax(q_vals)
        print(f'Action: {action}')
        state, reward, done, info = env.step(action)
        # print(f'State: {state} \nReward: {reward} \nDone? {done} \nExtra Info: {info}')
        # del state
        # f = open("state.txt", "a")
        # f.write(f'{state}')
        # f.close()
        # np.set_printoptions(threshold=sys.maxsize)

        # reshaping the array from 3D
        # matrice to 2D matrice.   
        # arr_reshaped = state.reshape(state.shape[0], -1)
        
        # saving reshaped array to file.
        # np.savetxt("state.txt", arr_reshaped)
        
        # retrieving data from file.
        # loaded_arr = np.loadtxt("state.txt")
        
        # This loadedArr is a 2D array, therefore
        # we need to convert it to the original
        # array shape.reshaping to get original
        # matrice with original shape.
        # load_original_arr = loaded_arr.reshape(loaded_arr.shape[0], loaded_arr.shape[1] // arr.shape[2], arr.shape[2])

        # np.savetxt("state.txt", state)
        # raise(TypeError)
        total_reward += reward
        if info['flag_get']:
            print('WE GOT THE FLAG!!!!!!!')
            flag = True
        if done:
            print(total_reward)
            break

    env.close()
    return flag
