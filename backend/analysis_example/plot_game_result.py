import numpy as np
from matplotlib import pyplot as plt

# from api import models as api_models
# from database.sql import models as sql_models
from db_config import DB_ENGINE


plt.rcParams.update({
    "savefig.dpi": 200,
    "savefig.bbox": "tight",
})

def image_size(width: float = 17, height: float = 13) -> tuple[float, float]:
    """convert figsize from cm to inches"""
    return width / 2.54, height / 2.54


def plot_path(filename: str) -> str:
    return f"analysis_example/plots/{filename}"


def plot_data(game_id: int, round_id: int, voting_event_ids: list[int]):
    game = DB_ENGINE.get_game(game_id=game_id)
    parties = [_p for _p in DB_ENGINE.get_parties(game_id=game_id) if _p.round_id == round_id]
    voters = DB_ENGINE.get_voters(game_id=game_id)
    affiliations = {
        affiliation.voter_id: affiliation.party_id
        for affiliation in DB_ENGINE.get_affiliations_for_round(round_id=round_id)
    }
    voting_events = [
        DB_ENGINE.get_voting_event(voting_event_id=voting_event_id)
        for voting_event_id in voting_event_ids
    ]
    votes = {
        voting_event_id: DB_ENGINE.get_votes(voting_event_id=voting_event_id)
        for voting_event_id in voting_event_ids
    }

    vote_values = {
        vote_value.capitalize(): [
            sum(vote.value == vote_value for vote in _votes)
            for _, _votes in votes.items()
        ]
        for vote_value in ["YES", "NO", "ABSTAIN"]
    }
    x = np.arange(len(votes))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=image_size())
    for vote_value, amount in vote_values.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, amount, width, label=vote_value)
        ax.bar_label(rects, padding=3)
        multiplier += 1
    ax.set_ylabel('Amount of votes')
    ax.set_xlabel('Voting event ID')
    ax.set_title('Votes per voting event')
    ax.set_xticks(x + width, list(votes))
    ax.legend(loc='upper right', ncols=3)
    ax.set_ylim(0, 65)
    plt.savefig(plot_path("votes_per_voting.png"))
    plt.close()

    x = np.arange(len(parties))  # the label locations
    width = 0.25  # the width of the bars
    fig, axs = plt.subplots(nrows=len(voting_events), ncols=1, figsize=image_size())
    fig.subplots_adjust(hspace=0)
    for ax, voting_event in zip(axs, voting_events):
        vote_values = {
            vote_value.capitalize(): [
                sum(vote.value == vote_value and affiliations[vote.voter_id] == party.id for vote in votes[voting_event.id])
                for party in parties
            ]
            for vote_value in ["YES", "NO", "ABSTAIN"]
        }
        multiplier = 0
        for vote_value, amount in vote_values.items():
            offset = width * multiplier
            rects = ax.bar(x + offset, amount, width, label=vote_value)
            ax.bar_label(rects, padding=3)
            multiplier += 1
        ax.tick_params(axis="x", which="both", bottom=False, labelbottom=False)
        ax.legend(loc='upper right', ncols=3)
        ax.set_ylim(0, 18)
    axs[0].set_title('Votes per party')
    axs[1].set_ylabel('Amount of votes')
    axs[-1].tick_params(axis="x", which="both", bottom=True, labelbottom=True)
    axs[-1].set_xticks(x + width, ["".join(w[0] for w in party.name.split(" ")) for party in parties])
    axs[-1].set_xlabel('Party')
    plt.savefig(plot_path("votes_per_party.png"))
    plt.close()

    party_score_change = {
        "".join(w[0] for w in party.name.split(" ")): [
            voting_event.extra_info["MAJORITY_WITH_REWARD"][voting_event.result]["parties"][str(party.id)]
            for voting_event in voting_events
        ]
        for party in parties
    }
    voter_score_change = {
        voter.id: [
            voting_event.extra_info["MAJORITY_WITH_REWARD"][voting_event.result]["voters"][str(voter.id)]
            for voting_event in voting_events
        ]
        for voter in voters
    }
    fig, axs = plt.subplots(nrows=2, ncols=1, figsize=image_size())
    fig.subplots_adjust(hspace=0)
    for party, score_change in party_score_change.items():
        axs[0].plot(np.cumsum([0] + score_change), label=party)
    for voter_id, score_change in list(voter_score_change.items())[:10]:
        axs[1].plot(np.cumsum([0] + score_change), label=voter_id)
    axs[0].legend(ncols=3)
    axs[0].set_title('Score change per event')
    axs[0].set_ylabel('Patry score')
    axs[0].tick_params(axis="x", which="both", bottom=False, labelbottom=False)
    axs[1].set_ylabel('Voter score (first 10)')
    axs[1].set_xticks(np.arange(len(voting_events) + 1), ['before'] + [v.id for v in voting_events])
    plt.savefig(plot_path("reward_change.png"))
    plt.close()
    





if __name__ == "__main__":
    plot_data(game_id=1, round_id=1, voting_event_ids=[1, 2, 3])

