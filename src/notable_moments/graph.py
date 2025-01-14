from matplotlib.pyplot import figure
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import re


def sanitize_title(title: str):
    compile = re.compile(r"\w")
    find = compile.finditer(title)
    collected_matches = [character.group(0) for character in find]
    return "".join(collected_matches)


def plot(time_list: list[float], title: str, save: bool):
    if not save:
        return
    filename = f"{sanitize_title(title)}.png"
    figure(figsize=(52, 6), dpi=80)
    plt.title(title)
    plt.hist(time_list, int(time_list[-1]))
    ax = plt.gca()
    ax.xaxis.set_major_locator(ticker.MaxNLocator(int(time_list[-1]) / 4))
    plt.savefig(filename)


if __name__ == "__main__":
    print(sanitize_title("MY CHILDHOOD #1 FEAR 💧 Escalator / エスカレーター"))
