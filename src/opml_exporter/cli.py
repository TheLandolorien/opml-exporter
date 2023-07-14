import glob
import os
import sqlite3

MACOS_USER_PODCAST_PATH = (
    "~/Library/Group Containers/*.groups.com.apple.podcasts/Documents/MTLibrary.sqlite"
)


def run() -> None:
    try:
        (db_path,) = glob.glob(os.path.expanduser(MACOS_USER_PODCAST_PATH))
    except ValueError as err:
        raise FileNotFoundError("ERROR: No podcast database found") from err

    sql_manager = sqlite3.connect(db_path, uri=True)

    sql_manager.close()
