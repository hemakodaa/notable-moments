from notable_moments import notable_keyword, notable_activity

url = "https://www.youtube.com/watch?v=bsfqMcMXg_8"


def test_run_activity():
    print(notable_activity(url, 90, False))


def test_run_keyword():
    print(
        notable_keyword(
            url,
            "tskr|TSKR",
        )
    )
