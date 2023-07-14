from unittest.mock import patch
import pytest

from opml_exporter import cli


@patch("opml_exporter.cli.glob")
def test_run_should_raise_if_missing_podcast_db(mock_glob):
    mock_glob.glob.return_value = "foo"

    with pytest.raises(FileNotFoundError) as err:
        cli.run()
        assert False, "should raise FileNotFoundError"

    assert str(err.value) == "ERROR: No podcast database found"


@patch("opml_exporter.cli.sqlite3")
def test_run_should_query_local_apple_podcast_database(mock_sqlite3):
    cli.run()

    mock_sqlite3.connect.assert_called()
    mock_sqlite3.connect.return_value.close.assert_called()
