from .server import app
import fire


class ServerCommand:
    def run(self):
        app.run(debug=True, port=5000)


class Command:
    def __init__(self):
        self.server = ServerCommand()

def main():
    fire.Fire(Command)