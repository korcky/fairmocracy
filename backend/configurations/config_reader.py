import pandas as pd
from datetime import datetime
from api.models import Game, GameStatus, VotingEvent, Party, Round
from sqlmodel import Session
from database.sql import models as sql_models
from db_config import get_db_engine, DB_ENGINE


class VotingConfigReader:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.rounds = self._load_rounds()
        self.name = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _load_rounds(self):
        """Group rows into rounds based on identical Rules, Parties, and Fractions."""
        df = pd.read_csv(self.file_path, delimiter=';')

        if 'Fractions' not in df.columns:
            df['Fractions'] = ''

        # Create a unique round identifier to preserve order
        df['RoundKey'] = df[['Rules', 'Parties', 'Fractions']].agg('||'.join, axis=1)
        df['RoundID'] = pd.factorize(df['RoundKey'])[0]

        rounds = []
        for _, group in df.groupby('RoundID', sort=False):
            rule = group['Rules'].iloc[0]
            parties = [p.strip() for p in group['Parties'].iloc[0].split(',')]

            raw_fractions = group['Fractions'].iloc[0]
            if pd.isna(raw_fractions) or raw_fractions.strip() == '':
                fractions = []
            else:
                fractions = [float(f.strip()) for f in raw_fractions.split(',') if f.strip() != '']
                # Calculate last fraction to make sum to 1.0
                last_fraction = round(1.0 - sum(fractions), 10)  # round to avoid floating point issues
                fractions.append(last_fraction)

            questions = group['Questions'].tolist()

            round_data = {
                'Rules': rule,
                'Parties': parties,
                'Fractions': fractions,
                'Questions': questions
            }
            rounds.append(round_data)

        return rounds

    def _validate_round_number(self, round_number: int):
        if not (0 <= round_number < len(self.rounds)):
            raise IndexError(f"Round number {round_number} is out of range. Only {len(self.rounds)} rounds available.")

    def get_game(self):
        """Retrieves configured Game object"""
        game = sql_models.Game(name=self.name, status=GameStatus.WAITING)
    
        with Session(DB_ENGINE.engine) as session:
            # Add the game to the session and generate the game ID
            session.add(game)
            session.flush()  # Generates game.id

            rounds = []

            for rnd in range(0, len(self.rounds)):
                voting_events = []
                parties = []

                for question in self.get_questions(rnd):
                    voting_events.append(sql_models.VotingEvent(title=question, content = question,voting_system="MAJORITY", round_id = rnd))

                for party in self.get_parties(rnd):
                    parties.append(sql_models.Party(name=party, round_id = rnd))

                rounds.append(sql_models.Round(
                    round_number=rnd,
                    game_id=game.id,
                    rules=self.get_rule(rnd),
                    parties=parties,
                    voting_events=voting_events))
                
            for i in rounds:
                session.add(i)
            game.rounds = rounds
            game.status = GameStatus.STARTED
            session.commit()
            session.refresh(game)
            
        return game
    
    def get_round(self, round_number: int):
        self._validate_round_number(round_number)
        return self.rounds[round_number]

    def get_all_rounds(self):
        return self.rounds

    def get_rule(self, round_number: int):
        self._validate_round_number(round_number)
        return self.rounds[round_number]['Rules']

    def get_parties(self, round_number: int):
        self._validate_round_number(round_number)
        return self.rounds[round_number]['Parties']

    def get_fractions(self, round_number: int):
        self._validate_round_number(round_number)
        return self.rounds[round_number]['Fractions']

    def get_questions(self, round_number: int):
        self._validate_round_number(round_number)
        return self.rounds[round_number]['Questions']
    
    def get_name(self):
        return self.name
    