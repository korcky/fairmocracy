import io
import pandas as pd
from datetime import datetime
from api.models import Game, GameStatus, VotingEvent, Party, Round
from sqlmodel import Session
from database.sql import models as sql_models
from db_config import get_db_engine, DB_ENGINE


class VotingConfigReader:
    def __init__(self, file_like: io.StringIO):
        df = pd.read_csv(file_like, delimiter=";")
        if "Voters" not in df.columns:
            raise ValueError("Missing required column 'Voters' in your config CSV.")
        try:
            df["Voters"] = df["Voters"].astype(int)
        except Exception:
            raise ValueError("Column 'Voters' must contain integer values.")

        if "Fractions" not in df.columns:
            df["Fractions"] = ""

        df["RoundKey"] = (
            df[["Rules", "Parties", "Fractions"]].astype(str).agg("||".join, axis=1)
        )

        df["RoundID"] = pd.factorize(df["RoundKey"])[0]

        self.round_voter_targets = df.groupby("RoundID")["Voters"].first().to_dict()
        self.n_voters = max(self.round_voter_targets.values())

        df = df.drop(columns=["Voters", "RoundKey"])

        self._df = df
        self.rounds = self._load_rounds()
        self.name = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _load_rounds(self):
        rounds = []
        df = self._df

        for round_id, group in df.groupby("RoundID", sort=False):
            rule = group["Rules"].iloc[0]
            parties = [p.strip() for p in group["Parties"].iloc[0].split(",")]

            raw_fracs = group["Fractions"].iloc[0]
            if pd.isna(raw_fracs) or not raw_fracs.strip():
                fractions = []
            else:
                parts = [x.strip() for x in raw_fracs.split(",") if x.strip()]
                fractions = [float(x) for x in parts]
                last_frac = round(1.0 - sum(fractions), 10)
                fractions.append(last_frac)

            questions = group["Questions"].tolist()

            rounds.append(
                {
                    "Rules": rule,
                    "Parties": parties,
                    "Fractions": fractions,
                    "Questions": questions,
                }
            )

        return rounds

    def get_game(self):
        """Retrieves configured Game object"""
        game = sql_models.Game(
            name=self.name,
            status=GameStatus.WAITING,
            n_voters=self.n_voters
        )

        with Session(DB_ENGINE.engine) as session:
            session.add(game)
            session.flush()  # generate game.id

            sql_rounds = []
            for idx, rnd in enumerate(self.rounds):
                r = sql_models.Round(
                    round_number=idx,
                    game_id=game.id,
                    rules=rnd["Rules"]
                )
                r.voting_events = [
                    sql_models.VotingEvent(
                        title=q,
                        content=q,
                        voting_system="MAJORITY"
                    )
                    for q in rnd["Questions"]
                ]
                r.parties = [sql_models.Party(name=p) for p in rnd["Parties"]]
                sql_rounds.append(r)

            for r in sql_rounds:
                session.add(r)

            session.commit()
            session.refresh(game)

            first_round = game.rounds[0]
            game.current_round_id = first_round.id
            session.add(game)
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
        return self.rounds[round_number]["Rules"]

    def get_parties(self, round_number: int):
        self._validate_round_number(round_number)
        return self.rounds[round_number]["Parties"]

    def get_fractions(self, round_number: int):
        self._validate_round_number(round_number)
        return self.rounds[round_number]["Fractions"]

    def get_questions(self, round_number: int):
        self._validate_round_number(round_number)
        return self.rounds[round_number]["Questions"]

    def get_name(self):
        return self.name
