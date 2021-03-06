import gym
# from nes_py.wrappers import BinarySpaceToDiscreteSpaceEnv
# import gym_super_mario_bros
# from gym_super_mario_bros.actions import SIMPLE_MOVEMENT

import env_wrappers

import argparse
import time
import numpy as np
import collections

import tensorflow as tf
import tensorflow.keras.layers as layers

tf.enable_eager_execution()

DEFAULT_ENV_NAME = "PongNoFrameskip-v4"

def play_and_visualize_game(env, net):
    state = env.reset()
    is_done = False

    FPS = 25
    while not is_done:
        start_ts = time.time()
        env.render()
        if False:
            action = env.action_space.sample()
        else:
            state_a = np.expand_dims(state, axis=0)
            q_vals_v = net(state_a)
            act_v = tf.argmax(q_vals_v, axis = 1)
            action = act_v.numpy()[0]

        state, reward, is_done, _ = env.step(action)
        delta = 1/FPS - (time.time() - start_ts)
        if delta > 0:
            time.sleep(delta)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", default=DEFAULT_ENV_NAME,
                        help="Name of the environment, default=" + DEFAULT_ENV_NAME)
    args = parser.parse_args()

    env = env_wrappers.make_env(args.env)
    # env = gym_super_mario_bros.make('SuperMarioBros-v0')
    # env = BinarySpaceToDiscreteSpaceEnv(env, SIMPLE_MOVEMENT)
    # env = gym.wrappers.Monitor(env, 'video/')

    net = tf.keras.models.load_model('PongNoFrameskip-v4-best.dat') 

    print(net.summary())
    print(net.inputs)

    play_and_visualize_game(env, net)