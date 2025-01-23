from notable_moments import notable_keyword, notable_activity


def test_run_activity():
    print(notable_activity("https://www.youtube.com/watch?v=_Hw2Spr4YQc", 90, False))


def test_run_keyword():
    print(
        notable_keyword(
            "https://www.youtube.com/watch?v=_Hw2Spr4YQc",
            "tskr|TSKR",
        )
    )
