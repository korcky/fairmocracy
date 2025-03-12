#This class represents a voter. It contains the following attributes:
# - voterID: A unique identifier for the voter.
# - name: The name of the voter.
# - sex: The sex of the voter.
# - Party Affiliation: The party affiliation of the voter.
# - votingEvent: The voting event that the voter is participating in.
import random
class Voter:


    def __init__(self, name, sex, party):
        self.name = name
        self.voterID = random.randint(100000, 999999)
        self.sex = sex
        self.party = party
        self.votingEvent = None


    def GetVoterID(self):
        return self.voterID
    def GetName(self):
        return self.name
    def GetSex(self):
        return self.sex
    def GetParty(self):
        return self.party