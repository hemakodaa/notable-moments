from graph import plot
from msg import get_title, get_percentile, message_processing
import numpy as np


def notable_moments(URL: str, percentile: int):
    title = get_title(URL)
    print(f"Now loading comments for {title.encode()}")
    msg = message_processing(URL)
    item = {m: None for m in msg}
    frequency = list(map(lambda x: x.item(), np.bincount(msg)))
    item_frequency = list(zip(item, frequency))
    nm = get_percentile(item_frequency, percentile)
    plot(msg, title)
    return nm
