import random

from sqlmodel import Session

from api import models as api_models
from api.voting_systems import VotingResult
from database.sql import models as sql_models
from db_config import get_db_engine, DB_ENGINE


def rand_sign() -> int:
    return 1 if random.random() > 0.5 else -1


def initialize(number_of_voters: int = 5):
    try:
        game = get_db_engine().get_game(game_id=1)
        return
    except Exception:
        pass
    test_game = sql_models.Game(
        name="Test Game", hash="1234", rounds=[
            sql_models.Round(round_number=0, parties=[sql_models.Party(name="red"), sql_models.Party(name="blue")], rules="FI"),
            sql_models.Round(round_number=1, parties=[sql_models.Party(name="red"), sql_models.Party(name="blue")], rules="FI")],
            status=api_models.GameStatus.WAITING,
            n_voters=number_of_voters
    )
    with Session(DB_ENGINE.engine) as session:
        session.add(test_game)
        session.commit()
        session.refresh(test_game)
        session.add(test_game)
        session.commit()

        voting_event = sql_models.VotingEvent(
            title="dummy voting",
            content="to test stuff",
            voting_system=api_models.VotingSystem.MAJORITY_WITH_REWARD,
            configuration={
                "pass_threshold": 0.5,
                "is_abstain_count_to_total": False,
                "reward_per_voter": True,
                "reward_per_party": True,
            },
            extra_info={
                api_models.VotingSystem.MAJORITY_WITH_REWARD: {
                    VotingResult.ACCEPTED: {
                        "voters": {i + 1: rand_sign() * random.randint(1, 5) for i in range(number_of_voters)},
                        "parties": {1: 10, 2: -5},
                    },
                    VotingResult.REJECTED: {
                        "voters": {i + 1: rand_sign() * random.randint(1, 5)  for i in range(number_of_voters)},
                        "parties": {1: -1, 2: -10},
                    },
                },
            },
            round_id=test_game.rounds[0].id,
        )
        voting_event2 = sql_models.VotingEvent(
            title="dummy voting2",
            content="to test stuff2",
            voting_system=api_models.VotingSystem.MAJORITY,
            configuration={"pass_threshold": 0.5, "is_abstain_count_to_total": False},
            #extra_info=...
            round_id=test_game.rounds[0].id
        )
        voting_event3 = sql_models.VotingEvent(
            title="dummy voting3",
            content="to test stuff",
            voting_system=api_models.VotingSystem.MAJORITY,
            configuration={"pass_threshold": 0.5, "is_abstain_count_to_total": False},
            #extra_info=...
            round_id=test_game.rounds[1].id,
        )
        voting_event4 = sql_models.VotingEvent(
            title="dummy voting2",
            content="to test stuff2",
            voting_system=api_models.VotingSystem.MAJORITY,
            configuration={"pass_threshold": 0.5, "is_abstain_count_to_total": False},
            #extra_info=...
            round_id=test_game.rounds[1].id
        )
        session.add(voting_event)
        session.add(voting_event2)
        session.add(voting_event3)
        session.add(voting_event4)
        for ind in range(number_of_voters):
            session.add(sql_models.Voter(name=f"voter_{ind}", game_id=test_game.id))
        session.commit()

        test_game.current_round_id = test_game.rounds[0].id

        session.add(test_game)
        session.commit()

        session.refresh(voting_event)
        for ind in range(1, number_of_voters + 1):
           session.add(sql_models.Vote(
               value=api_models.VoteValue.YES if ind % 2 else api_models.VoteValue.NO,
               voter_id=ind,
               voting_event_id=voting_event.id,
           ))
        for ind in range(1, number_of_voters + 1):
            session.add(sql_models.Affiliation(
                voter_id=ind,
                party_id=ind % 2 + 1,
                round_id=1,
            ))
            session.add(sql_models.Affiliation(
                voter_id=ind,
                party_id=ind % 2 + 1,
                round_id=2,
            ))

        session.commit()
