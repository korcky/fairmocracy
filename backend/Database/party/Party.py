#This class represents a party object
class Party:
    def __init__(self, name: str, game_id: int, id: int = None):
        self.id = id
        self.name = name
        self.game_id = game_id
        self.voters = []
        self.voting_events = []
        self.game = None