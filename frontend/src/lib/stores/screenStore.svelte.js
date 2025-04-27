import { writable, derived } from 'svelte/store';
import { currentUser } from './userData.svelte.js';
import { gameState } from './gameData.svelte.js';

// Flag checking if user has proceeded to vote after seeing info on the law
export const hasSeenInfo = writable(false);

let _lastEventId = null;

export const currentScreen = derived(
	[currentUser, gameState, hasSeenInfo],
	([$user, $game, seen], set) => {
		// Hasn't joined a game
		if (!$user.gameId) {
			hasSeenInfo.set(false);
			_lastEventId = null;
			return set('select');
		}

		// Hasn't given name
		if (!$user.userId) {
			hasSeenInfo.set(false);
			_lastEventId = null;
			return set('register');
		}

		// Hasn't selected party for round
		if (!$user.affiliations?.[$game.current_round_id]) {
			hasSeenInfo.set(false);
			_lastEventId = null;
			return set('registerToVote');
		}

		// Waiting for others
		if ($game.status === 'waiting') {
			hasSeenInfo.set(false);
			_lastEventId = null;
			return set('welcome');
		}

		// New voting event, game has started
		if ($game.status === 'started' && $game.current_voting_event_id !== _lastEventId) {
			hasSeenInfo.set(false);
			_lastEventId = $game.current_voting_event_id;
			return set('info');
		}

		// Still in same voting event
		if ($game.status === 'started') {
			const eventId = $game.current_voting_event_id;

			// Not proceeded to vote
			if (!seen) {
				return set('info');
			}

			// Proceeded but not voted
			if ($user.votes?.[eventId] === undefined) {
				return set('vote');
			}

			// Voted
			return set('wait');
		}

		// Game has ended
		if ($game.status === 'ended') {
			return set('end');
		}

		// Fallback (should never hit, but just in case)
		return set('select');
	},
	'select'
);
