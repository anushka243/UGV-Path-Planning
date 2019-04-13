import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
from maze_env import Maze
from RL_brain import DeepQNetwork


def run_maze():
    step = 0
    t =0
    total_paths = []
    total_energy = []
    for episode in range(800):
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

            RL.store_transition(observation, action, reward, observation_)

            if (step > 200) and (step % 5 == 0):
                RL.learn()

            
            current_path.append(str(observation))

            # swap observation
            observation = observation_

            # break while loop when end of this episode
            if done:
                break
            step += 1

        total_paths.append(len(current_path) + 1)
            # total_energy.append((((len(current_path) + 1) * 2) / 2) * (0.29 + 7.4 * 2))
        # the energy calculation process can be referenced from the MINLP code
        total_energy.append(((((len(current_path) + 1) * 2) / 2) * (0.29 + 7.4 * 2)) + 1 * env._not_charged())


    # end of game
    print('game over')
    #env.destroy()

    # running it after training
    final = []
    observation = env.reset()
    while True:
        # fresh env
        env.render()
        # RL choose action based on observation
        action = RL.greedy_action(observation)
        # action = RL.choose_action(str(observation))

        # RL take action and get next observation and reward
        observation_, reward, done = env.step(action)
        # RL learn from this transition
        #RL.learn()

        # swap observation
        final.append(str(observation))
        env._create_line(observation, observation_)
        observation = observation_

        # env._save()

        # break while loop when end of this episode
        if done:
            env._save()
            break
            
    #print(total_paths)
    #print(total_energy)
    env.destroy()
    x = []
    for i in range(800):
        x.append(i)

    minlp = []
    for i in range(800):
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