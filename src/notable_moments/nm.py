from notable_moments.graph import plot
from notable_moments.msg import get_title, get_percentile, message_processing
import numpy as np


def notable_moments(URL: str, percentile: int, save: bool):
    """
    Percentile: return the nth percentile of timestamp based on frequency
    Save: if True, saves histogram figure as png. Else it will only show the figure.
    """
    title = get_title(URL)
    print(f"Now loading comments for {title.encode()}")
    msg = message_processing(URL)
    item = {m: None for m in msg}
    frequency = list(map(lambda x: x.item(), np.bincount(msg)))
    item_frequency = list(zip(item, frequency))
    nm = get_percentile(item_frequency, percentile)
    plot(msg, title, save)
    return nm
