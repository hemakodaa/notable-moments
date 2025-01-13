from chat_downloader import ChatDownloader
from chat_downloader.sites.common import Chat
import matplotlib.pyplot as plt
from datetime import datetime
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
    c: Chat = ChatDownloader().get_chat(URL)
    print(f"Total chat download runtime: {time.time() - chat_download_start}")
    return c


def calculate_chat_live_timestamp(message: int, stream_start: datetime):
    duration = stream_start - datetime.fromtimestamp(message / 1_000_000)
    duration_in_minutes = abs(divmod(duration.total_seconds(), 60)[0])
    return duration_in_minutes


def message_processing():
    time_list = []
    message_processing_start = time.time()
    all_live_chat = [c for c in chat() if c.get("time_in_seconds") > 0]
    stream_start = datetime.fromtimestamp(all_live_chat[0].get("timestamp") / 1_000_000)
    for c in all_live_chat:
        time_list.append(
            calculate_chat_live_timestamp(c.get("timestamp"), stream_start)
        )
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
