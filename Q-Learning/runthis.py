"""
Reinforcement learning maze example.
Red rectangle:          explorer.
Black rectangles:       hells       [reward = 5].
Yellow bin circle:      paradise    [reward = 10 + x*5 where x is the number of users].
All other states:       ground      [reward = -1].
This script is the environment part of this example. The RL is in RL_brain.py.

"""

from env import Maze
from RL_brain import QLearningTable


def update():
    # training
    for episode in range(10):
        # initial observation
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

            observation = observation_

            # break while loop when end of this episode
            if done:
                break

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

    print(len(final))
    Energy = ((len(final)*2)/2)*(0.29 + 0.74*2)
    print(Energy)
    env.destroy()


if __name__ == "__main__":
    env = Maze()
    RL = QLearningTable(actions=list(range(env.n_actions)))

    env.after(100, update)
    env.mainloop()
