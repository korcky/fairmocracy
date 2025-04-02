import pandas as pd


class VotingConfigReader:
    def __init__(self, file_path: str):
        """Initialize the reader with the path to the CSV file."""
        self.file_path = file_path
        self.configurations = self._load_configurations()

    def _load_configurations(self):
        """Load configurations from the CSV file into a list of dictionaries."""
        df = pd.read_csv(self.file_path, delimiter=';')
        return df.to_dict(orient='records')

    def get_number_of_rounds(self):
        """Retrieve the number of rounds"""
        return len(self.configurations)

    def get_round_config(self, round_number: int):
        """Retrieve configuration for a specific round (row index starting from 0)."""
        if 0 <= round_number < len(self.configurations):
            return self.configurations[round_number]
        else:
            raise IndexError(f"Round number {round_number} out of range {len(self.configurations)}.")

    def get_configurations(self):
        """Retrieve all rounds as a list of dictionaries."""
        return self.configurations

    def get_voting_system(self, round_number: int):
        """Retrieve the voting system for a specific round."""
        if 0 <= round_number < len(self.configurations):
            return self.get_round_config(round_number).get("Voting system")
        else:
            raise IndexError(f"Round number {round_number} out of range {len(self.configurations)}.")

    def get_questions(self, round_number: int):
        """Retrieve the questions for a specific round."""
        if 0 <= round_number < len(self.configurations):
            questions_str = self.get_round_config(round_number).get("Questions")
            questions = [question.strip() for question in questions_str.split(",")]
            return questions
        else:
            raise IndexError(f"Round number {round_number} out of range {len(self.configurations)}.")

    def get_parties(self, round_number: int):
        """Retrieve the parties for a specific round."""
        if 0 <= round_number < len(self.configurations):
            parties_str = self.get_round_config(round_number).get("Parties")
            parties = [party.strip() for party in parties_str.split(",")]
            return parties
        else:
            raise IndexError(f"Round number {round_number} out of range {len(self.configurations)}.")
