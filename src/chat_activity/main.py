from chat_downloader import ChatDownloader
import numpy as np
import matplotlib.pyplot as plt
import datetime
from matplotlib.pyplot import figure
import matplotlib.ticker as ticker
import requests
from bs4 import BeautifulSoup

# CHANGE URL AND THEN RUN THIS NEXT
URL = "https://www.youtube.com/watch?v=QYN47aGY9j0"
# CHANGE GRAPH SIZE HERE
figure(figsize=(52, 6), dpi=80)


def get_title() -> str:
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, "lxml")
    title: str = soup.find_all(name="title")[0].text
    return title.encode()


def chat() -> list[float]:
    chat = ChatDownloader().get_chat(URL)
    starttime = 0
    started = False
    time_list = []
    # this takes a long time
    for message in chat:
        message_seconds = message.get("time_in_seconds")
        if message_seconds < 0:
            continue
        if not started:
            starttime = datetime.datetime.fromtimestamp(
                message.get("timestamp") / 1000 / 1000
            )
            started = True

        message_datetime = message.get("timestamp") / 1000 / 1000
        duration = starttime - datetime.datetime.fromtimestamp(message_datetime)
        duration_in_minutes = abs(divmod(duration.total_seconds(), 60)[0])
        time_list.append(duration_in_minutes)
    return time_list


def plot(time_list: list[float]):
    plt.hist(time_list, int(time_list[-1]))
    ax = plt.gca()
    ax.xaxis.set_major_locator(ticker.MaxNLocator(int(time_list[-1]) / 4))
    plt.show()


def main():
    title = get_title()
    print(f"Now loading comments for {title}")
    plt.title(title)
    plot(chat())


if __name__ == "__main__":
    main()
