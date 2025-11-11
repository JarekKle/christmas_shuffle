import json
import random


class Shuffler:
    def __init__(self,names_file):
        self.names_file = names_file
        self.attendants = self.open_file(names_file)
        self.participants = None
        self.shuffled = None

    @staticmethod
    def open_file(file_name):
        with open(file_name, "r", encoding="utf-8") as f:
            file = json.load(f)
        return file

    def get_all_participants_names(self):
        participants = []
        for name, info in self.attendants["attendants"].items():
            if info.get("enabled") is True:
                participants.append(name)
        self.participants = participants

    def shuffle_participants(self,avoid_mutual=False, max_attempts=1000):
        n = len(self.participants)
        if n < 2:
            return None
        for attempt in range(max_attempts):
            shuffled = self.participants.copy()
            random.shuffle(shuffled)
            if any(self.participants[i] == shuffled[i] for i in range(n)):
                continue
            if avoid_mutual:
                mutual_found = False
                for i in range(n):
                    gifter = self.participants[i]
                    receiver = shuffled[i]
                    j = shuffled.index(gifter)
                    if self.participants[j] == receiver:
                        mutual_found = True
                        break
                if mutual_found:
                    continue
            self.shuffled = shuffled
            return
        return None

    def get_nick_from_name(self, name):
        return self.attendants["attendants"].get(name)["nick"]

    def get_results(self):
        results = {"results": []}
        for i in range(len(self.participants)):
            results["results"].append({"sender": self.participants[i], "receiver": self.shuffled[i]})
        return results

    def start(self):
        self.get_all_participants_names()
        self.shuffle_participants()
        self.get_all_participants_names()