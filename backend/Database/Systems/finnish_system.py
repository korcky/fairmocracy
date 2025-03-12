class FinnishSystem(VotingSystem):
    def __init__(self):
        super().__init__("Finnish")
        self.seats = 0
        self.parties = []
        self.votes = []
        self.votes_per_party = []
        self.quota = 0