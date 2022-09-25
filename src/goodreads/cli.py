from pathlib import Path

import fire

from .server import app
from .index import init_index, add_source_file, find_most_active_users, find_reviews
from .ranker import Ranker



class ServerCommand:
    def __init__(self, appdir):
        self.appdir = Path(appdir)
        self.indexdir = self.appdir / "index"
        self.rankdir = self.appdir / "ranker"

    def run(self):
        app.config["APPDIR"] = self.appdir
        app.config["INDEXDIR"] = self.indexdir
        app.config["RANKDIR"] = self.rankdir
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
    
    def train(self):
        self.ranker.train()

class InteractionCommand:
    def __init__(self, appdir):
        self.appdir = Path(appdir)
        self.indexdir = self.appdir / "index"
    
    def find_active_users(self, src):
        res = find_most_active_users(src)
        print(res.most_common(10))
    
    def find_reviews(self, src, user):
        from pprint import pprint
        res = find_reviews(self.indexdir, src, user)
        pprint(res[:100])

class Command:
    def __init__(self, appdir):
        self.index = IndexCommand(appdir)
        self.server = ServerCommand(appdir)
        self.ranker = RankerCommand(appdir)
        self.interactions = InteractionCommand(appdir)

def main():
    fire.Fire(Command)