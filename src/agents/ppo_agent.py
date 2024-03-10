from stable_baselines3 import PPO
import numpy as np
from .agent import Agent
import fastfiz as ff
from typing import Optional


class PPOAgent(Agent):
    def __init__(self, model: PPO) -> None:
        self.model = model

    def decide_shot(self, table_state: ff.TableState) -> Optional[ff.ShotParams]:
        obs = self.get_observation(table_state)
        if any(not (ball[0] == -1) for ball in obs[1:,]):
            while True:
                action, _ = self.model.predict(obs)
                sp = ff.ShotParams(
                    *self.interpolate_action(table_state, action))
                if table_state.isPhysicallyPossible(sp) == ff.TableState.OK_PRECONDITION:
                    return sp

        print("WIN!")
        return None

    @staticmethod
    def get_ball_positions(table_state: ff.TableState):
        balls = []
        for i in range(16):
            b = table_state.getBall(i)
            pos = b.getPos()
            balls.append((pos.x, pos.y))

        balls = np.array(balls)
        return balls

    @staticmethod
    def get_observation(table_state: ff.TableState):
        observation = PPOAgent.get_ball_positions(table_state)
        for i, _ in enumerate(observation):
            if not table_state.getBall(i).isInPlay():
                observation[i] = [-1, -1]

        return observation

    @staticmethod
    def interpolate_action(table_state: ff.TableState, action):
        a = np.interp(action[0], [0, 0], [0, 0])
        b = np.interp(action[1], [0, 0], [0, 0])
        theta = np.interp(
            action[2], [0, 1], [table_state.MIN_THETA,
                                table_state.MAX_THETA - 0.001]
        )
        phi = np.interp(action[3], [0, 1], [0, 360])
        v = np.interp(action[4], [0, 1], [0, table_state.MAX_VELOCITY])
        return [a, b, theta, phi, v]
