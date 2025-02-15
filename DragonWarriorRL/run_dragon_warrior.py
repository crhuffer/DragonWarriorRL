from dragon_warrior_env import DragonWarriorEnv
from dumb_dw_env import DumbDragonWarriorEnv
from actions import dragon_warrior_actions
from nes_py.wrappers import JoypadSpace
from dqn_agent import DQNAgent
import time
import numpy as np
import pathlib
import pandas as pd

######
use_dumb_dw_env = True
loadcheckpoint = True
path_models = pathlib.Path('models/')
filename_model = str(path_models / 'model')
episodes = 50
frames_per_episode = 10001
# render = False
render = True
pause_after_action = False
# pause_after_action = True
# todo adjust cosine method, or change from boolean to variable controlling period of cosine
eps_method = 'cosine'
# eps_method = 'exp_decay'
eps_cosine_method_frames_per_cycle = 36000  # travels one wavelength in this
# print_stats_per_action = True
print_stats_per_action = False
frames_to_elapse_before_saving_agent = 20000
######

if use_dumb_dw_env == True:
    env = DumbDragonWarriorEnv()
else:
    env = DragonWarriorEnv()
env = JoypadSpace(env, dragon_warrior_actions)
env.reset()

# Parameters
'''Observation space (env.observation_space.shape) is 240x256x3, the height and width of the space with 3 (RBG)
color channels. The agent can take 256 different possible actions.'''
# todo add in RAM information
states = (240, 256, 3)
actions = env.action_space.n

dw_info_dict = env.state_info
dw_info_states = np.array(list(dw_info_dict.values()))

agent = DQNAgent(states=states, game_states=dw_info_states, actions=actions, max_memory=1000000,
                 double_q=True, eps_method=eps_method, agent_save=frames_to_elapse_before_saving_agent)
if loadcheckpoint:
    agent.restore_model(filename=filename_model)
    print('Checkpoint loaded')

# Episodes
rewards = []
episode_number = []
frames_in_episode = []
epsilon_at_end = []
key_found_in_episode = []
gold_found_in_episode = []
torch_found_in_episode = []

# Timing
start = time.time()
step = 0

def current_game_state(info_state):
    return np.array(list(info_state.values()))

# Main loop
for episode in range(episodes):

    # Reset env, returns screen values into np array
    state = env.reset()
    # Return values for RAM info into np array
    game_state = current_game_state(env.state_info)

    # Reward
    total_reward = 0

    # Play
    for episode_frame in range(frames_per_episode):

        if render == True:
            # Slows down learning by a factor of 3
            env.render()

        # Run agent
        action = agent.run(state=state, game_state=game_state, eps_method=eps_method,
                           eps_cos_frames=eps_cosine_method_frames_per_cycle)

        # Perform action
        next_state, reward, done, info = env.step(action=action)
        next_game_state = current_game_state(env.state_info)


        # Remember transition
        agent.add(experience=(state, next_state, game_state, next_game_state, action, reward, done))

        # Update agent
        agent.learn()

        # Total reward
        total_reward += reward
        if print_stats_per_action == True:
            print(np.round(total_reward, 4), dragon_warrior_actions[action],
                  episode_frame, np.round(agent.eps_now, 4))
        if pause_after_action == True:
            input('press any key to advance')

        # Update state and game_state
        state = next_state
        game_state = next_game_state

        # If done break loop
        if done or info['exit_throne_room']:
            break

    # todo change to average eps
    if eps_method == 'exp_decay':
        eps = agent.eps
    if eps_method == 'cosine':
        eps = agent.eps_now

    # Rewards
    rewards.append(total_reward / episode_frame)
    frames_in_episode.append(episode_frame)
    episode_number.append(episode)
    epsilon_at_end.append(eps)
    if info['throne_room_key'] == True:
        key_found_in_episode.append(1)
    if info['throne_room_key'] == False:
        key_found_in_episode.append(0)
    if info['throne_room_gold'] == True:
        gold_found_in_episode.append(1)
    if info['throne_room_gold'] == False:
        gold_found_in_episode.append(0)
    if info['throne_room_torch'] == True:
        torch_found_in_episode.append(1)
    if info['throne_room_torch'] == False:
        torch_found_in_episode.append(0)

    # Print
    # todo build lists/dictionaries with this info, export as csv
    if episode % 1 == 0:
        print('Episode {e} - +'
              'Frame {f} - +'
              'Frames/sec {fs} - +'
              'Epsilon {eps} - +'
              'Mean Reward {r} - +'
              'Total Reward {R} - +'
              'Key {k} - +'
              'Gold {g} - +'
              'Torch {t}'.format(e=episode,
                                 f=agent.step,
                                 fs=np.round((agent.step - step) / (time.time() - start)),
                                 eps=np.round(eps, 4),
                                 r=np.round(rewards[-1:], 4),
                                 # r=np.mean(rewards[-1:]),
                                 R=np.round(total_reward, 4),
                                 k = info['throne_room_key'],
                                 g = info['throne_room_gold'],
                                 t = info['throne_room_torch']))
        start = time.time()
        step = agent.step

episode_dict = {
    'episode' : episode_number,
    'end_epsilon' : epsilon_at_end,
    'frames' : frames_in_episode,
    'ave_reward' : rewards,
    'key_found' : key_found_in_episode,
    'gold_found' : gold_found_in_episode,
    'torch_found' : torch_found_in_episode,
}
results = pd.DataFrame(episode_dict).set_index('episode')

if use_dumb_dw_env == True:
    results.to_csv(f'dumb_DW_Bot_results.csv')
else:
    results.to_csv(f'DW_Bot_results.csv')

# Save rewards
np.save('rewards.npy', rewards)
