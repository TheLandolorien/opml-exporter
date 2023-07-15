import glob
import os
import sqlite3

import xml.etree.ElementTree as ET

MACOS_USER_PODCAST_PATH = (
    "~/Library/Group Containers/*.groups.com.apple.podcasts/Documents/MTLibrary.sqlite"
)
PODCAST_QUERY = "SELECT ZUUID, ZFEEDURL, ZWEBPAGEURL, ZTITLE FROM ZMTPODCAST"


def run() -> None:
    try:
        (db_path,) = glob.glob(os.path.expanduser(MACOS_USER_PODCAST_PATH))
    except ValueError as err:
        raise FileNotFoundError("ERROR: No podcast database found") from err

    sql_manager = sqlite3.connect(database=db_path, uri=True)
    sql_manager.row_factory = sqlite3.Row

    with sql_manager:
        result = sql_manager.execute(PODCAST_QUERY)

    records = result.fetchall()

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

    sql_manager.close()
