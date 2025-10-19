import sqlite3
from collections.abc import Iterator
from pathlib import PurePath, Path
import json


class ChatItemParser:
    def __init__(self, json_file: dict):
        self._json = json_file

    @property
    def _set_json(self, json_file: dict):
        return self._json

    @_set_json.setter
    def _set_json(self, value: dict):
        self._json = value

    def time_in_seconds(self) -> int:
        return self._json.get("time_in_seconds")

    def action_type(self) -> str:
        return self._json.get("action_type")

    def message(self) -> str:
        return self._json.get("message")

    def message_id(self) -> str:
        return self._json.get("message_id")

    def timestamp(self) -> int:
        return self._json.get("timestamp")

    def time_text(self) -> str:
        return self._json.get("time_text")

    def author(self) -> dict:
        return self._json.get("author")

    def message_type(self) -> str:
        return self._json.get("message_type")

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


def parse_json(chat: Iterator) -> Iterator:
    chat_parser = ChatItemParser({})
    import time
    start = time.time()
    for row in chat:
        chat_parser._set_json = row
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
    print(f"Finished in: {time.time() - start}")


def connect_db(db_path: str) -> sqlite3.Connection:
    if not Path(db_path).exists():
        exit("Path to db doesn't exist.")
    return sqlite3.connect(db_path)


def create_table(conn: sqlite3.Connection, table_name: str):
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


def insert_into_table(conn: sqlite3.Connection, table_name: str, values: list[dict]):
    cur = conn.cursor()
    stmt = (
        f"INSERT OR IGNORE INTO {table_name}"
        "(TIME_IN_SECONDS, ACTION_TYPE, MESSAGE, MESSAGE_ID, TIMESTAMP, TIME_TEXT, AUTHOR, MESSAGE_TYPE) VALUES("
        ":time_in_seconds, :action_type, :message, :message_id, :timestamp, :time_text, :author, :message_type)"
    )
    cur.executemany(stmt, values)
    conn.commit()


def db_get_messages(video_id: str, db_path) -> Iterator[dict[str, int | str]]:
    """
    currently used msg: 'time_in_seconds', 'timestamp', 'message'
    """
    conn = connect_db(db_path)
    cur = conn.cursor()

    stmt = (
        f"SELECT TIME_IN_SECONDS, TIMESTAMP, MESSAGE FROM {video_id} ORDER BY TIMESTAMP"
    )
    for row in cur.execute(stmt):
        time_in_seconds, timestamp, message = row
        yield {
            "time_in_seconds": time_in_seconds,
            "timestamp": timestamp,
            "message": message,
        }


def check_chat_existence_in_db(db_path: str, video_id: str) -> bool:
    conn = connect_db(db_path)
    cur = conn.cursor()
    stmt = "SELECT name FROM sqlite_master WHERE type='table' AND name=':video_id'"
    does_it_exist = cur.execute(stmt, {"video_id": video_id})
    return True if list(does_it_exist) else False


def db_insert_main(db_path: str, video_id: str, chat: Iterator):
    # TODO: how to get args for db path?
    # answer: use configparser?
    conn = connect_db(db_path)
    table_name = video_id
    create_table(conn, table_name)
    print("Parsing json file...")
    chat_items = [c for c in parse_json(chat)]
    print("parse complete")
    if chat_items:
        insert_into_table(conn, table_name, chat_items)
    else:
        print("No chat for this Video exists.")
    conn.close()


# if __name__ == "__main__":
#     simulate_get_messages()
