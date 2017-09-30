import sys
import time
import random
import multiprocessing

from qlearn import QLearn
from world import World

sim_name = 'route-choice'


class DriverWorld(World):
    agents = []

    def __init__(self, road_cap):
        self.road_cap = road_cap
        self.num_roads = len(road_cap)
        self.road_cnt = [0 for _ in range(self.num_roads)]

    def update(self):
        self.road_cnt = [0 for _ in range(self.num_roads)]

        for agent in self.agents:
            agent.do_action()
        # print()

        total_rewards = 0
        for agent in self.agents:
            total_rewards += agent.learn()

        print(str(total_rewards) + ' ' + ' '.join(map(str, self.road_cnt)))

class Driver:
    cell = (0, 0)
    
    def __init__(self, _world):
        self.world = _world
    
        self.ai = QLearn(actions=[0, 1, 2, 3])
        self.ai.agent = self

        self.last_action = None
        self.last_state = None

    def do_action(self):
        self.state = 0
        action = self.ai.chooseAction(self.state)

        self.last_state = self.state
        self.last_action = action

        self.world.road_cnt[action] += 1
        # print(action, end=" ")

    def learn(self):
        reward = self.calc_reward()
        self.ai.learn(self.last_state, self.last_action, reward, self.state)
        return reward

    def calc_reward(self):
        return self.world.road_cap[self.last_action] - \
               self.world.road_cnt[self.last_action]


def worker(params):
    pass


def process(params):
    return map(int, params)


def run(params):
    timesteps, num_drivers, *road_cap = process(params)
    # print(timesteps, num_drivers, "run nigger run")
    
    world = DriverWorld(road_cap)
    for _ in range(num_drivers):
        agent = Driver(world)
        world.agents.append(agent)
        
    for _ in range(timesteps):
        world.update()
