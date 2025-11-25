import json, os

class StateStore:
    def __init__(self, path="state.json"):
        self.path = path
        self.state = {}
        self.load()

    def load(self):
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                self.state = json.load(f)

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.state, f)

    def get(self, project, default=0):
        return self.state.get(project, default)

    def update(self, project, startAt):
        self.state[project] = startAt
        self.save()
