import pandas as pd


class PointsReader:
    def __init__(self, file_path: str):
        """Initialize the reader with the path to the semicolon-separated CSV file."""
        self.df = pd.read_csv(file_path, sep=';')
        required_columns = {'Round', 'Question', 'User', 'User Points', 'Party Points'}
        if not required_columns.issubset(self.df.columns):
            missing = required_columns - set(self.df.columns)
            raise ValueError(f"Missing required columns in points table: {missing}")

    def get_points(self, round_number: int, question: str, user: int):
        """Return user and party points for a given user, round and question."""
        entry = self.df[(self.df['Round'] == round_number) &
                        (self.df['Question'] == question) &
                        (self.df['User'] == user)]
        if entry.empty:
            raise ValueError(f"No entry found for round {round_number}, question {question}, user {user}")
        return {
            'User Points': int(entry['User Points'].values[0]),
            'Party Points': int(entry['Party Points'].values[0])
        }
    