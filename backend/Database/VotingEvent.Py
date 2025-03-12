
#This class is used to store the information of a voting event. It contains the following attributes:
# - eventID: A unique identifier for the voting event.
# - eventDate: The date of the voting event.
# - eventSubject: The subject of the voting event.
# - votingSystem: The voting system used in the voting event.

import datetime
class VotingEvent:
    def __init__(self, eventID, eventDate, eventSubject, votingSystem):
        self.eventID = eventID
        self.eventDate = eventDate
        self.eventSubject = eventSubject
        self.votingSystem = votingSystem

    def GetEventID(self):
        return self.eventID

    def GetEventDate(self):
        return self.eventDate

    def GetEventSubject(self):
        return self.eventSubject

    def GetVotingSystem(self):
        return self.votingSystem