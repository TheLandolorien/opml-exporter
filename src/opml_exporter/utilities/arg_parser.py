import argparse


class OPMLArgumentParser(argparse.ArgumentParser):
    NAME = "opml_exporter"
    DESCRIPTION = "Export OPML files for podcasts"

    def __init__(self):
        super().__init__(prog=self.NAME, description=self.DESCRIPTION)

        self.add_argument("--name", type=str, help="Podcast name")
        self.args = self.parse_args()
