import sqlite3
from datetime import time, timedelta
from collections.abc import Iterator
from pathlib import PurePath, Path
import json


class ChatItemParser:
    def __init__(self, json: dict):
        self.json = json

    def time_in_seconds(self) -> int:
        return self.json.get("time_in_seconds")

    def action_type(self) -> str:
        return self.json.get("action_type")

    def message(self) -> str:
        return self.json.get("message")

    def message_id(self) -> str:
        return self.json.get("message_id")

    def timestamp(self) -> int:
        return self.json.get("timestamp")

    def time_text(self) -> str:
        return self.json.get("time_text")

    def author(self) -> dict:
        return self.json.get("author")

    def message_type(self) -> str:
        return self.json.get("message_type")

    def _test(self):
        fns = [
            self.action_type(),
            self.author(),
            self.message(),
            self.message_id(),
            self.message_type(),
            self.time_in_seconds(),
            self.time_text(),
            self.time_text(),
        ]
        if any(fns) is None:
            exit("\n".join(fns))
        else:
            exit("All good.")


def parse_json(path: str) -> Iterator:
    r = list()
    with open(path, "r") as f:
        r = json.load(f)  # list of dicts
    for chat in r:
        chat_parser = ChatItemParser(chat)
        yield {
            "time_in_seconds": chat_parser.time_in_seconds(),
            "action_type": chat_parser.action_type(),
            "message": chat_parser.message(),
            "message_id": chat_parser.message_id(),
            "timestamp": chat_parser.timestamp(),
            "time_text": chat_parser.time_text(),
            "author": str(chat_parser.author()),  # stored as a text in db
            "message_type": chat_parser.message_type(),
        }


def connect_db() -> sqlite3.Connection:
    db_path = PurePath("db").joinpath("chat.db")
    if not Path(db_path).exists():
        exit("Path to db doesn't exist.")
    return sqlite3.connect(db_path)


def create_table(table_name: str):
    conn = connect_db()
    cur = conn.cursor()
    stmt = (
        f"CREATE TABLE IF NOT EXISTS {table_name} ("
        "ID INTEGER PRIMARY KEY AUTOINCREMENT,"
        "TIME_IN_SECONDS REAL,"
        "ACTION_TYPE TEXT,"
        "MESSAGE TEXT,"
        "MESSAGE_ID TEXT,"
        "TIMESTAMP INTEGER,"
        "TIME_TEXT TEXT,"
        "AUTHOR TEXT,"
        "MESSAGE_TYPE TEXT)STRICT"
    )
    cur.execute(stmt)


def insert_into_table(table_name: str, values: list[dict]):
    conn = connect_db()
    cur = conn.cursor()
    stmt = (
        f"INSERT OR IGNORE INTO {table_name}"
        "(TIME_IN_SECONDS, ACTION_TYPE, MESSAGE, MESSAGE_ID, TIMESTAMP, TIME_TEXT, AUTHOR, MESSAGE_TYPE) VALUES("
        ":time_in_seconds, :action_type, :message, :message_id, :timestamp, :time_text, :author, :message_type)"
    )
    cur.executemany(stmt, values)
    conn.commit()


def db_main():
    table_name = "pankoscared" # this will be video id
    create_table(table_name)
    chat_items = [
        c for c in parse_json(PurePath("chat_results").joinpath("pankoscared.json"))
    ]
    insert_into_table(table_name, chat_items)


if __name__ == "__main__":
    db_main()
