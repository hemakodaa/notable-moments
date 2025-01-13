from chat_downloader import ChatDownloader
from chat_downloader.sites.common import Chat

# import matplotlib.pyplot as plt
from datetime import datetime

# from matplotlib.pyplot import figure
# import matplotlib.ticker as ticker
import requests
from bs4 import BeautifulSoup
import time
import numpy as np

# CHANGE URL AND THEN RUN THIS NEXT
# CHANGE GRAPH SIZE HERE
# figure(figsize=(52, 6), dpi=80)
# def plot(time_list: list[float], title: str):
#     plt.hist(time_list, int(time_list[-1]))
#     ax = plt.gca()
#     ax.xaxis.set_major_locator(ticker.MaxNLocator(int(time_list[-1]) / 4))
#     plt.savefig(f"{title}.png")


def get_percentile(item_frequency: list[tuple[int, int]], percentile: int):
    sort_to_frequency = sorted(item_frequency, key=lambda x: x[1])
    frequency_only = list(map(lambda x: x[1], sort_to_frequency))
    threshold = int(np.percentile(frequency_only, percentile))
    filtered = list(filter(lambda x: x[1] > threshold, item_frequency))
    return filtered


def get_title(URL) -> str:
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, "lxml")
    title: str = soup.find_all(name="title")[0].text
    return title.encode()


def chat(URL) -> Chat:
    chat_download_start = time.time()
    c: Chat = ChatDownloader().get_chat(URL)
    print(f"Total chat download runtime: {time.time() - chat_download_start}")
    return c


def calculate_chat_live_timestamp(message: int, stream_start: datetime):
    duration = (message / 1_000_000) - stream_start
    duration_in_minutes = int(duration // 60)
    return duration_in_minutes


def message_processing(URL: str) -> list[float]:
    time_list = []
    all_live_chat = list(filter(lambda x: x.get("time_in_seconds") > 0, chat(URL)))
    stream_start = (
        all_live_chat[0].get("timestamp") / 1_000_000
    )  # timestamp is in Unix epoch (microsecond)
    for count, c in enumerate(all_live_chat):
        print(f"Processing {count} chat...", end="\r")
        time_list.append(
            calculate_chat_live_timestamp(c.get("timestamp"), stream_start)
        )
    return time_list
