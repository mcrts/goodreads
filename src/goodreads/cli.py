from .server import app
from .index import init_index, add_source_file
import fire


class ServerCommand:
    def __init__(self, indexdir):
        self.indexdir = indexdir

    def run(self):
        app.config["INDEXDIR"] = self.indexdir
        app.run(debug=True, port=5000)

class IndexCommand:
    def __init__(self, indexdir):
        self.indexdir = indexdir

    def init(self):
        init_index(self.indexdir)
    
    def add(self, src):
        add_source_file(self.indexdir, src)

class Command:
    def __init__(self, indexdir):
        self.index = IndexCommand(indexdir)
        self.server = ServerCommand(indexdir)

def main():
    fire.Fire(Command)