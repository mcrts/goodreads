from pathlib import Path

import fire

from .server import app
from .index import init_index, add_source_file
from .ranker import Ranker



class ServerCommand:
    def __init__(self, appdir):
        self.appdir = Path(appdir)
        self.indexdir = self.appdir / "index"

    def run(self):
        app.config["APPDIR"] = self.appdir
        app.config["INDEXDIR"] = self.indexdir
        app.run(debug=True, port=5000)

class IndexCommand:
    def __init__(self, appdir):
        self.appdir = Path(appdir)
        self.indexdir = self.appdir / "index"

    def init(self):
        init_index(self.indexdir)
    
    def add(self, src):
        add_source_file(self.indexdir, src)

class RankerCommand:
    def __init__(self, appdir):
        self.appdir = Path(appdir)
        self.rankdir = self.appdir / "ranker"
        self.ranker = Ranker(self.rankdir)
   
    def add(self, src):
        self.ranker.add_reviews(src)

    def test(self):
        print(len(self.ranker.user_index.index))
        print(len(self.ranker.book_index.index))
        print(self.ranker.csr_matrix.size)

class Command:
    def __init__(self, appdir):
        self.index = IndexCommand(appdir)
        self.server = ServerCommand(appdir)
        self.ranker = RankerCommand(appdir)

def main():
    fire.Fire(Command)