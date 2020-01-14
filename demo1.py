import numpy as np
from kaggle_environments import make, evaluate
from util import show_html
import not_my_tree
import score_agent

cx_env = make("connectx", debug=True)

print('Configuration is ', cx_env.configuration)


def hello_world_agent(observation, configuration):
    rows = configuration.rows
    columns = configuration.columns
    current_board = observation.board
    # print('configuration:', configuration)
    print('observation:', observation)

    def at(row, col):
        return observation.board[col + row * configuration.columns]

    if at(0, 0) == 0:
        return 0

    from random import choice
    r = choice([c for c in range(configuration.columns) if observation.board[c] == 0])
    print(r)
    return r


def not_my(observation, configuration):
    return not_my_tree.my_agent(observation, configuration, max_depth=5 )


def play_one_and_show(agent):
    cx_env = make("connectx", debug=True, configuration={
        'timeout': 1000
    })
    cx_env.reset()

    cx_env.run([agent, 'negamax'])

    # print(cx_env.render())

    r = cx_env.render(mode="html", width=650, height=650)
    show_html(r)


def agent_reward(rewards):
    return sum(r[0] for r in rewards) / sum(r[0] + r[1] for r in rewards)


def eval(agent):
    results = evaluate("connectx", [agent, "negamax"], num_episodes=10)
    final_result = agent_reward(results)
    print("CX Agent vs Negamax Agent:", final_result)


# play_one_and_show(score_agent.agent)
eval(score_agent.agent)