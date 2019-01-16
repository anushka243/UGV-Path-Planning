"""
Reinforcement learning maze example.
Red rectangle:          explorer.
Black rectangles:       hells       [reward = 5].
Yellow bin circle:      paradise    [reward = 10 + x*5 where x is the number of users].
All other states:       ground      [reward = -1].
This script is the environment part of this example. The RL is in RL_brain.py.

"""

import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
from env import Maze
from RL_brain import QLearningTable


def update():
    # training
    total_paths = []
    total_energy = []
    for episode in range(100):
        # initial observation
        current_path = []
        observation = env.reset()

        while True:
            # fresh env
            env.render()

            # RL choose action based on observation
            action = RL.choose_action(str(observation))

            # RL take action and get next observation and reward
            observation_, reward, done = env.step(action)

            # RL learn from this transition
            RL.learn(str(observation), action, reward, str(observation_))

            # swap observation
            #if episode == 20 :
                #env._create_line(observation, observation_)
                #env._save()
            current_path.append(str(observation))
            observation = observation_

            # break while loop when end of this episode
            if done:
                break

        total_paths.append(len(current_path)+1)
        #total_energy.append((((len(current_path) + 1) * 2) / 2) * (0.29 + 7.4 * 2))
        total_energy.append(((((len(current_path)+1)*2)/2)*(0.29 + 7.4 * 2)) + 1 * env._not_charged())

    # end of game
    print('game over')

    # running it after training
    final = []
    observation = env.reset()
    while True:
        # fresh env
        env.render()

        # RL choose action based on observation
        action = RL.greedy_action(str(observation))
        #action = RL.choose_action(str(observation))

        # RL take action and get next observation and reward
        observation_, reward, done = env.step(action)

        # RL learn from this transition
        RL.learn(str(observation), action, reward, str(observation_))

        # swap observation
        final.append(str(observation))

        env._create_line(observation, observation_)

        observation = observation_
        #env._save()

        # break while loop when end of this episode
        if done:
            env._save()
            break

    #print(len(final))

    #Energy = (((len(final)+1)*2)/2)*(0.29 + 7.4 * 2)
    #print(Energy)
    #print(total_paths)
    #print(total_energy)
    env.destroy()
    x = []
    for i in range(100):
        x.append(i)

    minlp = []
    for i in range(100):
        minlp.append(241)

    plt.plot(x, total_energy, 'b')
    plt.plot(x, minlp, 'r')
    plt.xlabel('Number of Epochs')
    plt.ylabel('Moving Energy of UGV')
    plt.show()


if __name__ == "__main__":
    env = Maze()
    RL = QLearningTable(actions=list(range(env.n_actions)))

    env.after(100, update)
    env.mainloop()
