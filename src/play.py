import fastfiz as ff
from fastfiz_renderer import GameHandler
from stable_baselines3 import PPO
from agent import PPOAgent, Agent
import json
from typing import Optional


def create_table(n_balls=5):
    ts = ff.TableState()
    for i in range(n_balls):
        ts.setBall(i, ff.Ball.STATIONARY, ff.Point(0.0, 0.0))
    ts.randomize()
    return ts


def get_config() -> dict:
    with open("src/play_config.json", "r") as fp:
        return json.load(fp)


def play(agent: Agent, balls: Optional[int] = None, episodes: Optional[int] = None):
    config = get_config()

    if balls is None:
        if config["balls"] and 2 >= config["balls"] >= 16:
            raise ValueError("Balls must be between 2 and 16")
        balls = config["balls"]

    if episodes is None:
        episodes = config["episodes"]

    games = [(create_table(balls), agent.decide_shot) for _ in range(episodes)]
    gh = GameHandler(window_pos=(0, 0), scaling=350)
    gh.play_games(games, auto_play=config["auto_play"],
                  shot_speed_factor=config["shot_speed_factor"])
