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
from enum import Enum, auto
import re
import time
import numpy as np


class MsgFilter(Enum):
    ACTIVITY = auto()
    REGEX = auto()


class FilterKind:
    def __init__(self, kind: MsgFilter, pattern: None | str = None):
        self.p = pattern
        self.k = kind

    def pattern(self) -> str | None:
        return self.p

    def kind(self) -> MsgFilter:
        return self.k


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


def calculate_chat_live_timestamp(message_timestamp: int, stream_start: datetime):
    # this returns the timestamp in minutes format
    duration = (message_timestamp / 1_000_000) - stream_start
    duration_in_minutes = int(duration // 60)
    return duration_in_minutes


def message_processing(URL: str, filter_kind: FilterKind) -> list[float]:
    time_list = []
    match filter_kind.kind():
        case MsgFilter.ACTIVITY:
            all_live_chat = list(
                filter(lambda x: x.get("time_in_seconds") > 0, chat(URL))
            )
        case MsgFilter.REGEX:
            if not filter_kind.pattern():
                raise ValueError("No keyword inserted.")
            try:
                compile = re.compile(rf"{filter_kind.pattern()}")
            except re.error as e:
                raise ValueError(e)
            all_live_chat = list(
                filter(
                    lambda x: x.get("time_in_seconds") > 0
                    and [m for m in compile.finditer(x.get("message"))],
                    chat(URL),
                )
            )
        case _:
            raise ValueError("BUG: MsgFilter was not used")
    match filter_kind.kind():
        case MsgFilter.ACTIVITY:
            stream_start = (
                all_live_chat[0].get("timestamp") / 1_000_000
            )  # timestamp is in Unix epoch (microsecond)
            for c in all_live_chat:
                time_list.append(
                    calculate_chat_live_timestamp(c.get("timestamp"), stream_start)
                )
            return time_list
        case MsgFilter.REGEX:
            for c in all_live_chat:
                time_list.append(c.get("time_in_seconds") // 60)
            return time_list
        case _:
            raise ValueError("BUG: MsgFilter was not used")
