from chat_downloader import ChatDownloader
from chat_downloader.sites.common import Chat
import matplotlib.pyplot as plt
import datetime
from matplotlib.pyplot import figure
import matplotlib.ticker as ticker
import requests
from bs4 import BeautifulSoup
import time

# CHANGE URL AND THEN RUN THIS NEXT
URL = "https://www.youtube.com/watch?v=QYN47aGY9j0"
# CHANGE GRAPH SIZE HERE
figure(figsize=(52, 6), dpi=80)


def get_title() -> str:
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, "lxml")
    title: str = soup.find_all(name="title")[0].text
    return title.encode()


def chat() -> Chat:
    chat_download_start = time.time()
    chat: Chat = ChatDownloader().get_chat(URL)
    print(f"Total chat download runtime: {time.time() - chat_download_start}")
    return chat


def message_processing():
    stream_start = 0
    started = False
    time_list = []
    message_processing_start = time.time()
    for message in chat():
        message_seconds = message.get("time_in_seconds")
        # skips all messages that are sent before stream starts
        if message_seconds < 0:
            continue
        # started => the first time the time_in_seconds is bigger than zero
        # means it's the stream start time
        # this must run ONLY ONCE
        if not started:
            stream_start = datetime.datetime.fromtimestamp(
                message.get("timestamp") / 1_000_000
            )  # timestamp is in unix epoch time (microseconds)
            started = True

        message_datetime = message.get("timestamp") / 1_000_000
        duration = stream_start - datetime.datetime.fromtimestamp(message_datetime)
        duration_in_minutes = abs(divmod(duration.total_seconds(), 60)[0])
        time_list.append(duration_in_minutes)
    print(f"Total message processing runtime: {time.time() - message_processing_start}")
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
    plot(message_processing())


if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"Total runtime: {time.time() - start_time}")
