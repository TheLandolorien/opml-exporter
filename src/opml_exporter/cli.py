import glob
import os
import sqlite3
import typing
import xml.etree.ElementTree as ET

from opml_exporter.utilities.arg_parser import OPMLArgumentParser

MACOS_USER_PODCAST_PATH = (
    "~/Library/Group Containers/*.groups.com.apple.podcasts/Documents/MTLibrary.sqlite"
)
PODCAST_QUERY = "SELECT ZUUID, ZFEEDURL, ZWEBPAGEURL, ZTITLE FROM ZMTPODCAST"


def _get_database_path() -> str:
    try:
        (db_path,) = glob.glob(os.path.expanduser(MACOS_USER_PODCAST_PATH))
    except ValueError as err:
        raise FileNotFoundError("ERROR: No podcast database found") from err

    return db_path


def _get_connection() -> sqlite3.Connection:
    db_path = _get_database_path()
    sql_manager = sqlite3.connect(database=db_path, uri=True)
    sql_manager.row_factory = sqlite3.Row

    return sql_manager


def _generate_opml_file(records: typing.List[typing.Dict[str, str]]) -> None:
    opml = ET.Element("opml", attrib={"version": "1.0"})
    head = ET.SubElement(opml, "head")
    title = ET.SubElement(head, "title")
    title.text = "Podcast Subscriptions"
    body = ET.SubElement(opml, "body")
    feeds = ET.SubElement(body, "outline", attrib={"text": "feeds"})

    for podcast in records:
        ET.SubElement(
            feeds,
            "outline",
            attrib={
                "type": "rss",
                "text": podcast["ZTITLE"],
                "title": podcast["ZTITLE"],
                "xmlUrl": podcast["ZFEEDURL"],
                "htmlUrl": podcast["ZWEBPAGEURL"],
            },
        )

    ET.ElementTree(element=opml).write("podcasts.opml", encoding="UTF-8", xml_declaration=True)


def _get_podcast_data(name: str = None):
    sql_manager = _get_connection()

    with sql_manager:
        if name:
            result = sql_manager.execute(
                f"{PODCAST_QUERY} WHERE ZTITLE = :name",
                {"name": name},
            )
        else:
            result = sql_manager.execute(PODCAST_QUERY)

    records = result.fetchall()
    sql_manager.close()

    return records


def run() -> None:
    parser = OPMLArgumentParser()

    records = _get_podcast_data(name=parser.args.name)
    _generate_opml_file(records=records)
