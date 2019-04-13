"""
Reinforcement learning robot path planning for small grid.

Red rectangle:          UGV.
Black rectangles:       IoT regions       [reward = 5].
Yellow bin circle:      goal    [reward = 10 + x*5 where x is the number of users].
All other states:       ground      [reward = -1].
This script is the main run part. The RL is in RL_brain.py.
"""

import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
from biggest_maze_env import Maze
from RL_brain import DeepQNetwork


def run_maze():

    step = 0
    total_paths = [] # sum of paths calculated after each training episode
    total_energy = [] # total energy consumption for the complete training
    for episode in range(300):
        # initial observation
        current_path = []
        observation = env.reset()

        while True:
            # fresh env
            env.render()

            # RL choose action based on observation
            action = RL.choose_action(observation)

            # RL take action and get next observation and reward
            observation_, reward, done = env.step(action)

            #store in memory buffer
            RL.store_transition(observation, action, reward, observation_)

            #learning from memory only after certain number of steps
            if (step > 200) and (step % 5 == 0):
                RL.learn()

            #add the path
            current_path.append(str(observation))

            # swap observation
            observation = observation_

            # break while loop when end of this episode
            if done:
                break
            step += 1

        total_paths.append(len(current_path) + 1)
        # the energy calculation process can be referenced from the MINLP code
        total_energy.append(((((len(current_path) + 1) * 2) / 2) * (0.29 + 7.4 * 2)) + 1 * env._not_charged())


    # end of game
    print('game over')

    # running it after training
    final = []
    observation = env.reset()
    while True:
        # fresh env
        env.render()

        # RL greedy action based on observation
        action = RL.greedy_action(observation)
        # action = RL.choose_action(str(observation))

        # RL take action and get next observation and reward
        observation_, reward, done = env.step(action)

        # swap observation
        final.append(str(observation))

        #create path
        env._create_line(observation, observation_)
        observation = observation_

        # break while loop when end of this episode
        if done:
            env._save()
            break

    env.destroy()

    # comparsion plot of energy from DQN with MINLP
    x = []
    for i in range(300):
        x.append(i)

    minlp = []
    for i in range(300):
        minlp.append(241)

    plt.plot(x, total_energy, 'b')
    plt.plot(x, minlp, 'r')
    plt.xlabel('Number of Epochs')
    plt.ylabel('Moving Energy of UGV')
    plt.show()


if __name__ == "__main__":
    # maze game
    env = Maze()
    RL = DeepQNetwork(env.n_actions, env.n_features,
                      learning_rate=0.01,
                      reward_decay=0.9,
                      e_greedy=0.6,
                      replace_target_iter=200,
                      memory_size=2000,
                      output_graph=True
                      )
    env.after(100, run_maze)
    env.mainloop()
    RL.plot_cost()