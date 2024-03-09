import argparse
from enum import Enum
import logging
from play import play
from stable_baselines3 import PPO
from agent import PPOAgent
from fetch_models import list_models, fetch_model


class Mode(Enum):
    EVALUATE = "evaluate"
    PLAY = "play"
    FETCH = "fetch"


def get_args():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Pool Agent CLI")
    subparsers = parser.add_subparsers(dest="mode", required=True)

    eval_parser = subparsers.add_parser(
        Mode.EVALUATE.value, help="Train a model")
    eval_parser.add_argument(
        "-m", "--model", type=str, help="Path to pretrained model to train from"
    )
    eval_parser.add_argument(
        "-v",
        "--version",
        type=int,
        help="Train from pretrained model version. WARNING: This will overwrite existing models",
    )
    eval_parser.add_argument(
        "-b",
        "--balls",
        type=int,
        help="Amount of balls on table",
    )

    play_parser = subparsers.add_parser(
        Mode.PLAY.value, help="Play the game using a pretrained model"
    )
    play_parser.add_argument(
        "-m", "--model", required=True, type=str, help="Path to model"
    )
    play_parser.add_argument(
        "-e", "--episodes", type=int, default=1, help="Episodes to play"
    )
    play_parser.add_argument(
        "-r", "--render", action="store_true", help="Render the game"
    )
    play_parser.add_argument(
        "-b",
        "--balls",
        type=int,
        help="Amount of balls on table",
    )

    fetch_parser = subparsers.add_parser(
        Mode.FETCH.value, help="Fetch a model from the server"
    )

    fetch_parser.add_argument(
        "-m", "--model", type=str, help="Model name"
    )

    fetch_parser.add_argument(
        "-l", "--list", action="store_true", help="List available models"
    )

    return parser.parse_args()


def main():
    args = get_args()

    # Logger setup
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    match args.mode:
        case Mode.FETCH.value:
            if args.model and args.list:
                raise ValueError("Cannot list and fetch at the same time")

            if args.list:
                models = list_models()
                if not models:
                    print("No models available.")
                else:
                    print("Available models:")
                for model in models:
                    print(f" - {model}")

            if args.model:
                fetch_model(args.model)

        case Mode.PLAY.value:
            if args.balls and 2 >= args.balls >= 16:
                raise ValueError("Balls must be between 2 and 16")

            model = PPO.load(args.model)
            agent = PPOAgent(model)

            play(agent, args.balls, args.episodes)


if __name__ == "__main__":
    main()
