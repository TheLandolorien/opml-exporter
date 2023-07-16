from unittest.mock import patch

from opml_exporter.utilities.arg_parser import OPMLArgumentParser


@patch("sys.argv", ["opml-exporter"])
def test_parser_generates_help_output():
    parser = OPMLArgumentParser()

    assert (
        parser.format_help()
        == f"usage: {OPMLArgumentParser.NAME} [-h] [--name NAME]\n\n{OPMLArgumentParser.DESCRIPTION}\n\noptions:\n  -h, --help   show this help message and exit\n  --name NAME  Podcast name\n"
    ), "should generate help output"


@patch("sys.argv", ["opml-exporter"])
def test_parser_initializes_args_given_no_options():
    parser = OPMLArgumentParser()

    assert parser.args.name is None, "should parse empty options"


@patch("sys.argv", ["opml-exporter", "--name", "Dad Pod"])
def test_parser_initializes_args_given_name_option():
    parser = OPMLArgumentParser()

    assert parser.args.name == "Dad Pod", "should parse name option"
