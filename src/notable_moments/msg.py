from chat_downloader import ChatDownloader
from chat_downloader.sites.common import Chat
from chat_downloader.errors import (
    URLNotProvided,
    InvalidURL,
    SiteNotSupported,
    ChatGeneratorError,
)
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import time
import numpy as np


def get_percentile(item_frequency: list[tuple[int, int]], percentile: int):
    sort_to_frequency = sorted(item_frequency, key=lambda x: x[1])
    frequency_only = list(map(lambda x: x[1], sort_to_frequency))
    threshold = int(np.percentile(frequency_only, percentile))
    filtered = list(filter(lambda x: x[1] > threshold, item_frequency))
    return filtered


def get_title(URL) -> str:
    r = requests.get(URL)
    if r.status_code != 200:
        return "Requesting title returned non 200 code."
    soup = BeautifulSoup(r.text, "lxml")
    title: str = soup.find_all(name="title")[0].text
    return title


def chat(URL) -> Chat:
    chat_download_start = time.time()
    try:
        c: Chat = ChatDownloader().get_chat(URL)
        print(f"Total chat download runtime: {time.time() - chat_download_start}")
    except (URLNotProvided, InvalidURL, SiteNotSupported, ChatGeneratorError) as e:
        exit(e)
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
    for c in all_live_chat:
        time_list.append(
            calculate_chat_live_timestamp(c.get("timestamp"), stream_start)
        )
    return time_list
