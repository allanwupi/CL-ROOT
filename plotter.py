import ast

import matplotlib.pyplot as plt
import numpy as np


def main():
    with open("log.txt") as log_file:
        runs = [ast.literal_eval(line) for line in log_file if line.strip()]

    figure, axes = plt.subplots()
    colors = ["tab:blue", "tab:orange"]
    labels = ["Bot 1", "Bot 2"]

    for bot, (color, label) in enumerate(zip(colors, labels)):
        scores = [run[bot] for run in runs]
        for run in scores:
            axes.plot(range(1, len(run) + 1), run, color=color, alpha=0.15)

        turns_data = [
            [run[turn] for run in scores if turn < len(run)]
            for turn in range(max(map(len, scores)))
        ]
        mean = np.array([np.mean(turn) for turn in turns_data])
        standard_deviation = np.array([np.std(turn) for turn in turns_data])
        turns = np.arange(1, len(mean) + 1)
        axes.plot(turns, mean, color=color, label=f"{label} mean")
        axes.fill_between(
            turns,
            mean - standard_deviation,
            mean + standard_deviation,
            color=color,
            alpha=0.2,
            label=f"{label} +/- 1 SD",
        )

    axes.set_xlabel("Turn")
    axes.set_ylabel("Victory points")
    axes.set_title("Victory points over time")
    axes.legend()
    figure.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()