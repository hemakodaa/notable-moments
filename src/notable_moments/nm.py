from notable_moments.graph import plot
from notable_moments.msg import (
    get_title,
    get_percentile,
    message_processing,
    FilterKind,
    MsgFilter,
)
from collections import Counter
import numpy as np


def notable_keyword(URL, pattern: str) -> list[float, int]:
    """
    Patterns: a valid regex pattern
    returns: [timestamps]
    """
    title = get_title(URL)
    print(f"Now loading comments for {title.encode()}")
    msg = message_processing(URL, FilterKind(MsgFilter.REGEX, pattern))
    return [(k, v) for k, v in Counter(msg).items()]


def notable_activity(URL: str, percentile: int, save: bool) -> list[float, int]:
    """
    Percentile: return the nth percentile of timestamp based on frequency
    Save: if True, saves histogram figure as png. Else it will only show the figure.
    returns: [(timestamp, frequency)]
    """
    title = get_title(URL)
    print(f"Now loading comments for {title.encode()}")
    msg = message_processing(URL, FilterKind(MsgFilter.ACTIVITY))
    item = {m: None for m in msg}  # remove duplicates
    frequency = list(map(lambda x: x.item(), np.bincount(msg)))
    item_frequency = list(zip(item, frequency))
    nm = get_percentile(item_frequency, percentile)
    plot(msg, title, save)
    return nm
