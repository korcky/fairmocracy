# Fairmocracy backend
The backend is a FastAPI application.

## Quick start

* Once in your virtual environment, install dependencies:
    ```bash
    make setup-dev
    ```
    or
    ```bash
    pip install -r requirements.txt
    ```

* Run the application with
    ```bash
    make run
    ```
    or
    ```bash
    fastapi dev app.py
    ```


# Backend docs

The good place to start understasnding FastAPI: https://fastapi.tiangolo.com/learn/.

## Code structure

- `app.py` contains all the API endpoint declaration and most of their logic
- `db_config.py` defines the DB that the API will use
- `database` folder contains abstract DB engine and all implementations of it
- `configurations` folder contains logic to use configuration files to setup a game in DB
    - `configurations/examples` contains examples of configuration files
- `api` folder contains
    - `api/voting_systems` -- implementaions of voting system
    - `models.py` -- API models (classes that are used in the API reqeusts/responses)
    - `sse_connection_manager.py` -- implementation of Server-sent events (SSE) manager

### API 

#### `/join`

Returns infromation about specified game (uses game hash to identify the game) 

#### `/register`

Creates a user to be a part of a cpecified game

#### `/register_to_vote`

Creates a connection between user and a party for a specific round of a game

#### `/v1/user/{user_id}`

Returns information about user

#### `/v1/voting/cast_vote`

Casts a vote (`YES/NO/ABSTAIN`) of a specific users for a specific voting event

If it's a "last vote to be cast" -- conclude the voting event automatically: decides if it's `ACCEPTED` or `REJECTED` 
(based on the voting system) and calculate any other requiered metrics (based on the voting system)

#### `/game/{game_id}`

Returns infromation about specified game

#### `/game/{game_id}/parties`

Returns information about parties for the specified game

#### `/game/{game_id}/rounds`

Returns information about rounds for the specified game

#### `/round/{round_id}/voting_events`

Returns voting event for the specified round

#### `/voting_event/{voting_event_id}`

Returns information about specified voting event

#### `/voting_event/{voting_event_id}/conclude`

Concludes the voting event automatically: decides if it's `ACCEPTED` or `REJECTED` 
(based on the voting system) and calculate any other requiered metrics (based on the voting system)

#### `/upload_config`

Creates a game (all needed entities for it) in the DB based on the profided configuration file

#### `/sse/game-state`

Connects a clinet to listen for game state updates

### DB

- `database/abstract_engine.py` contains an abstract DB engine (all the requests that are needed for the API to work)
- `database/sql` countains an implementation of the abstarct DB engine to work with SQL databases

#### How to add support for the new DB

1. Inherit from `AbstractEngine` class and implement all the abstract methods so that this engine can work with your DB
(`database/sql` as an example)
2. Set your DB engine as `DB_ENGINE` in `db_config.py`

**TODO**: currently, `configuration` is hardcoded to work with SQL DB

#### DB schema

|Game||
|---|---|
|id||
|hash|code to quickly joint the game|
|name|additional identification for the game|
|current_round_id|what round of the game is currently active|
|current_voting_event_id|what voting event from the current round is currently active|
|n_voters|expected amount of voters in the game|
|status|current state of the game|

|Round||
|---|---|
|id|
|game_id|
|round_number|order of the round withing the game|

|Voter||
|---|---|
|id|
|game_id|
|name|just an additional identification for the user|
|extra_info|holds extra information for specific voting sustem|

|VotingEvent||
|---|---|
|id|
|round_id|
|title|title of the event|
|content|content/description of the event|
|voting_system|type of voting sustem to calculate result of the event + possible changes within extra_info|
|result|"ACCEPTED" or "REJECTED"|
|configuration|configuration for the voting event|
|extra_info|holds extra information for specific voting sustem|

|Vote||
|---|---|
|id|
|voter_id|
|voting_event_id|
|value|"YES"/"NO"/"ABSTAIN"|
|created_at|when vote have been casted|
|extra_info|holds extra information for specific voting sustem|

|Party||
|---|---|
|id|
|round_id|
|name|name which will be seen by the user|
|extra_info|holds extra information for specific voting sustem|

|Affiliation||
|---|---|
|id|
|voter_id|
|party_id|
|round_id|

## Game logic

### Configuration file

The main pupropse of a configuration file is to provide way of setuping a game (populate all the requirered entities in
the DB) without writing anything manually into the DB.

The full example of a configuration file can be seen here: `configurations/examples/configuration.json`

The current format of the configuration file:
```json
{
    "name": "game_name",    # a name for the game (for identification puproses)

    "n_voters": 101,        # number of voter in the game (used for automatic start of the game and voting 
                            # conclusion), during uploading of the config file admin specifies amount of real
                            # users, the rest (`n_voters - n_real_users`) will be "sumulated users" -- their
                            # votes (and possibly party affiliations) will be generated automatically

    "parties": [            # list of parties throught the game
        {
            "name": "Social Democratic Party",  # party name
            "round_id": 1                       # in which round of the game it appears
        },
        ...
    ],

    "affiliations": "randomize",    # how users connected to parties, currently supports only "randomize"
                                    # and it'll randomize affiliation for the "sumulated users"

    "voting_events": [                              # list of voting events
        {
            "title": "Carbon tax rate increase",        # a title for a vottin event
            "content": "In light of ...",               # its description
            "voting_system": "MAJORITY_WITH_REWARD",    # voting system type for the event
            "configuration": {                          # configuration for the voting system
                "pass_threshold": 0.5,
                "is_abstain_count_to_total": false, 
                "reward_per_voter": true,
                "reward_per_party": true
            },

            "extra_info": "randomize",                  # extra minformation for the event
                                                        # in case of `MAJORITY_WITH_REWARD`, rewards points
                                                        # can be randomized by using  "randomize"

            "round_id": 1                               # in which round of the game it appears
        },
        {
            "title": "Parental leave extention",
            "content": "With Finland's ...",
            "voting_system": "MAJORITY",                # voting events in the same game and round can
                                                        # have differetn voting system types
            "configuration": {
                "pass_threshold": 0.5,
                "is_abstain_count_to_total": false,
            },
            "extra_info": {},
            "round_id": 1
        },
        ...
    ]
}
```

### How to add an new voting system

Voting system is abstracted (`api/voting_systems/abstract.py`) into one method `voting_result(...)` which takes voting event,
all votes for that event, all the voters (for the current game) and all the parties (for the current game) as input and returns
vote result, all voters (that have changes) and all parties (that have changes). To minimize code changes to only the addition
of a new voting system, you should follow this interface.

The simplest implementation of a voting system is a majority voting system (`api/voting_systems/majority.py`) which simply look
at all casted votes and decided (based on the configured `pass_threshold` and `is_abstain_count_to_total`) if the voting event
is `ACCEPTED` or `REJECTED` (plus, return empty lists for voters and parties since there is nothing to be changed there).

A more complex implementation can be seen in a majority system with rewards (`api/voting_systems/reward.py`) which inherits from
majority system (and call it to define the result of the vote) and, on top of that, calculated a score (for both voters and
parties) based on the result of the voting event and `extra_info` provided in the voting event. This score is stored in
`extra_info` for voters and parties, so when the score is updated, `voting_result(...)` will return non empty list of voters and
parties (since their `extra_info` have been updated).

Any other new voting system should follow the same principals for `voting_result(...)` implementation:
- have a way to decide the result of the voting event
- store additional information for itself in the `extra_info` of the voting event (if this info is relevant to the
voting event)
- store additional information for itself in the `extra_info` of voters and parties (if this info is relevant to them)
- votes have also `extra_info`, so they can be also used

As an example, a voting system where voters have a "currency" that they can spent during the vote to wight their vote, for it:
- each voter will store (in `extra_info`) their current amount of currency
- each vote will store (in `extra_info`) how much currency the voter is spending on their vote
- during the vote conlusion, spent currency will weight the vote when calculating the result of the voting event
- based on the result of the voting event, current amount of currecny for voters will be change:
    - if voting event is `ACCEPTED`, all voters that voted `YES` will reduce amount of their current currency based on how much
    they have spent during the voting (i.e. `voting_result(...)` will return `ACCEPTED`, an empty list of parties and all the
    users that voted `YES` with updated balance in `extra_info`)
