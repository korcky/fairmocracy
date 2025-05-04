import random

from sqlmodel import Session, select

from api import models as api_models
from database.sql import models as sql_models
from db_config import DB_ENGINE


def get_random_value(possible_values) -> int:
    return random.choice([1, -1]) * random.choice(possible_values)


def upload_configuration(
    configuration: dict, number_of_real_voters: int
) -> sql_models.Game:
    """will work only with one active game"""
    if number_of_real_voters >= configuration["n_voters"]:
        raise Exception("only work with at least on simulated voter")

    with Session(DB_ENGINE.engine) as session:
        game = sql_models.Game(
            name=configuration["name"],
            status=api_models.GameStatus.WAITING,
            n_voters=configuration["n_voters"],
        )
        session.add(game)
        session.flush()

        rounds = list(set(party["round_id"] for party in configuration["parties"]))
        if rounds != list(set(party["round_id"] for party in configuration["voting_events"])):
            raise Exception("rounds in parties and voting_events aren't the same")
        
        rounds_map = {
            rounds[i]: sql_models.Round(round_number=i, game_id=game.id)
            for i in range(len(rounds))
        }
        for _round in rounds_map.values():
            session.add(_round)
        session.flush()

        parties = [
            sql_models.Party(name=party["name"], round_id=rounds_map[party["round_id"]].id)
            for party in configuration["parties"]
        ]
        for _party in parties:
            session.add(_party)
        session.flush()

        simulated_voters = [
            sql_models.Voter(name=f"simulated voter {i}", game_id=game.id)
            for i in range(configuration["n_voters"] - number_of_real_voters)
        ]
        for _voter in simulated_voters:
            session.add(_voter)
        session.flush()

        if configuration["affiliations"] == "randomize":
            for _round in rounds_map.values():
                round_parties = [_party for _party in parties if _party.round_id == _round.id]
                for voter_id in [_voter.id for _voter in simulated_voters]:
                    session.add(
                        sql_models.Affiliation(
                            voter_id=voter_id,
                            party_id=random.choice(round_parties).id,
                            round_id=_round.id,
                        )
                    )
        else:
            raise NotImplementedError("only randomize Affiliaztions are implemented")
        session.flush()

        first_voting_event_id = None
        for _voting_event in configuration["voting_events"]:
            extra_info = _voting_event["extra_info"]
            if (
                _voting_event["extra_info"] == "randomize"
                and _voting_event["voting_system"] == "MAJORITY_WITH_REWARD"
            ):
                first_voter_id = min(_voter.id for _voter in simulated_voters)
                round_parties = [
                    _party
                    for _party in parties
                    if _party.round_id == rounds_map[_voting_event["round_id"]].id
                ]
                extra_info = {
                    "MAJORITY_WITH_REWARD": {
                        "ACCEPTED": {
                            "voters": {
                                voter_id: get_random_value(range(5))
                                for voter_id in range(first_voter_id, configuration["n_voters"] + 1)
                            },
                            "parties": {
                                _party.id: get_random_value(range(0, 31, 10))
                                for _party in round_parties
                            },
                        },
                        "REJECTED": {
                            "voters": {
                                voter_id: get_random_value(range(5))
                                for voter_id in range(first_voter_id, configuration["n_voters"] + 1)
                            },
                            "parties": {
                                _party.id: get_random_value(range(0, 31, 10))
                                for _party in round_parties
                            },
                        },
                    }
                }

            voting_event = sql_models.VotingEvent(
                title=_voting_event["title"],
                content=_voting_event["content"],
                voting_system=_voting_event["voting_system"],
                configuration=_voting_event["configuration"],
                extra_info=extra_info,
                round_id=rounds_map[_voting_event["round_id"]].id,
            )
            session.add(voting_event)
            session.flush()

            if first_voting_event_id is None:
                first_voting_event_id = voting_event.id

            if (
                _voting_event["extra_info"] == "randomize"
                and _voting_event["voting_system"] == "MAJORITY_WITH_REWARD"
            ):
                # vote as best self outcome
                for _voter in simulated_voters:
                    yes_vote = extra_info["MAJORITY_WITH_REWARD"]["ACCEPTED"]["voters"][_voter.id]
                    no_vote = extra_info["MAJORITY_WITH_REWARD"]["REJECTED"]["voters"][_voter.id]
                    if yes_vote == no_vote and yes_vote <= 0:
                        vote_value = "ABSTAIN"
                    else:
                        vote_value = "YES" if yes_vote >= no_vote else "NO"
                    session.add(
                        sql_models.Vote(
                            value=vote_value,
                            voter_id=_voter.id,
                            voting_event_id=voting_event.id,
                        )
                    )

        session.commit()

        if number_of_real_voters <= 0:
            session.add(game)
            game.current_round_id = rounds_map[min(rounds)].id
            game.current_voting_event_id = first_voting_event_id
            session.commit()

        return game
