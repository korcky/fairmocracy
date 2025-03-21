import datetime

class Game:
    def __init__(self, name, description, issues):
        self.name = name
        self.description = description
        self.issues = issues
        self.current_index = 0
        self.state = "waiting"
        self.start_time = None
        self.end_time = None

    def start(self):
        self.state = "running"
        self.start_time = datetime.datetime.now()
        self.current_index = 0

    def end(self):
        self.state = "finished"
        self.end_time = datetime.datetime.now()

    def next_issue(self):
        if self.current_index < len(self.issues) - 1:
            self.current_index += 1
        else:
            self.end()

    def get_current_issue(self):
        if self.state != "running":
            return None
        return self.issues[self.current_index]

    def get_state(self):
        return {
            "name": self.name,
            "description": self.description,
            "state": self.state,
            "current_issue": self.get_current_issue().GetEventSubject() if self.get_current_issue() else None,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
        }
