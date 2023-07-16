import pytest
import typing
import uuid
from unittest.mock import ANY, patch


from opml_exporter import cli


@pytest.fixture
def mock_records() -> typing.List[typing.Dict[str, str]]:
    return [
        {
            "ZUUID": str.upper(str(uuid.uuid4())),
            "ZFEEDURL": "https://rss.example.com/dad-pod",
            "ZWEBPAGEURL": "https://dad-pod.example.com",
            "ZTITLE": "Dad Pod",
        },
        {
            "ZUUID": str.upper(str(uuid.uuid4())),
            "ZFEEDURL": "https://rss.example.com/pod-one-out",
            "ZWEBPAGEURL": "https://pod-one-out.example.com",
            "ZTITLE": "Pod One Out",
        },
    ]


@patch("opml_exporter.cli.glob")
def test_run_should_raise_if_missing_podcast_db(mock_glob) -> None:
    mock_glob.glob.return_value = "foo"

    with pytest.raises(FileNotFoundError) as err:
        cli.run()
        assert False, "should raise FileNotFoundError"

    assert str(err.value) == "ERROR: No podcast database found"


@patch("opml_exporter.cli.sqlite3")
@patch("opml_exporter.cli.ET")
@patch("opml_exporter.cli.OPMLArgumentParser")
def test_run_should_query_local_apple_podcast_database_without_options(
    mock_parser,
    mock_xml,
    mock_sqlite3,
    mock_records,
) -> None:
    mock_parser().args.name = None
    mock_manager = mock_sqlite3.connect.return_value
    mock_manager.execute.return_value.fetchall.return_value = mock_records

    cli.run()

    mock_sqlite3.connect.assert_called_once_with(database=ANY, uri=True)

    mock_manager.execute.assert_called_once_with(cli.PODCAST_QUERY)
    mock_manager.execute.return_value.fetchall.assert_called_once()

    mock_xml.Element.assert_called_once_with("opml", attrib={"version": "1.0"})
    mock_xml.SubElement.assert_any_call(mock_xml.Element.return_value, "head")
    mock_xml.SubElement.assert_any_call(mock_xml.SubElement.return_value, "title")

    mock_xml.SubElement.assert_any_call(mock_xml.Element.return_value, "body")
    mock_xml.SubElement.assert_any_call(
        mock_xml.SubElement.return_value, "outline", attrib={"text": "feeds"}
    )

    podcast_1, podcast_2 = mock_records
    mock_xml.SubElement.assert_any_call(
        mock_xml.SubElement.return_value,
        "outline",
        attrib={
            "type": "rss",
            "text": podcast_1["ZTITLE"],
            "title": podcast_1["ZTITLE"],
            "xmlUrl": podcast_1["ZFEEDURL"],
            "htmlUrl": podcast_1["ZWEBPAGEURL"],
        },
    )
    mock_xml.SubElement.assert_any_call(
        mock_xml.SubElement.return_value,
        "outline",
        attrib={
            "type": "rss",
            "text": podcast_2["ZTITLE"],
            "title": podcast_2["ZTITLE"],
            "xmlUrl": podcast_2["ZFEEDURL"],
            "htmlUrl": podcast_2["ZWEBPAGEURL"],
        },
    )

    mock_xml.ElementTree.assert_called_once_with(element=mock_xml.Element.return_value)
    mock_xml.ElementTree.return_value.write.assert_called_once_with(
        "podcasts.opml", encoding="UTF-8", xml_declaration=True
    )

    mock_manager.close.assert_called_once()


@patch("opml_exporter.cli.sqlite3")
@patch("opml_exporter.cli.ET")
@patch("opml_exporter.cli.OPMLArgumentParser")
def test_should_query_specific_podcast_given_title_option(
    mock_parser,
    mock_xml,
    mock_sqlite3,
    mock_records,
) -> None:
    mock_manager = mock_sqlite3.connect.return_value
    podcast = mock_records[0]
    mock_parser().args.name = podcast["ZTITLE"]
    mock_manager.execute.return_value.fetchall.return_value = [podcast]

    cli.run()

    mock_sqlite3.connect.assert_called_once_with(database=ANY, uri=True)
    mock_manager.execute.assert_called_once_with(
        f"{cli.PODCAST_QUERY} WHERE ZTITLE = :name", {"name": podcast["ZTITLE"]}
    )
    mock_manager.execute.return_value.fetchall.assert_called_once()

    mock_xml.Element.assert_called_once_with("opml", attrib={"version": "1.0"})
    mock_xml.SubElement.assert_any_call(mock_xml.Element.return_value, "head")
    mock_xml.SubElement.assert_any_call(mock_xml.SubElement.return_value, "title")

    mock_xml.SubElement.assert_any_call(mock_xml.Element.return_value, "body")
    mock_xml.SubElement.assert_any_call(
        mock_xml.SubElement.return_value, "outline", attrib={"text": "feeds"}
    )

    mock_xml.SubElement.assert_any_call(
        mock_xml.SubElement.return_value,
        "outline",
        attrib={
            "type": "rss",
            "text": podcast["ZTITLE"],
            "title": podcast["ZTITLE"],
            "xmlUrl": podcast["ZFEEDURL"],
            "htmlUrl": podcast["ZWEBPAGEURL"],
        },
    )

    mock_xml.ElementTree.assert_called_once_with(element=mock_xml.Element.return_value)
    mock_xml.ElementTree.return_value.write.assert_called_once_with(
        "podcasts.opml", encoding="UTF-8", xml_declaration=True
    )

    mock_manager.close.assert_called_once()
