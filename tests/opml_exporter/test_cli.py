import pytest

from opml_exporter import cli


def test_run_should_raise_not_implemented_error():
    with pytest.raises(NotImplementedError):
        cli.run()
        assert False, "should raise NotImplementedError"
