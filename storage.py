import json
import os


class Storage:
    def __init__(self, filename="data.json"):
        self.filename = filename

    def save(self, data):
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def load(self):
        if not os.path.exists(self.filename):
            return []

        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            return []