import { writable, get } from 'svelte/store';
import { PUBLIC_BACKEND_URL } from '$env/static/public';
import { currentUser, clearUserData, getExtraInfo } from './userData.svelte.js';

export const parties = writable([]);
export const gameState = writable({
	id: null,
	hash: null,
	name: null,
	status: null,
	current_round_id: null,
	current_voting_event_id: null,
	current_voting_question: null,
	countdown_ends_at: null,
	frontend_round_n: null,
	frontend_event_n: null
});

let _lastLoadedGameId = null;
let _evtSource = null;

export async function loadParties(gameId) {
	if (gameId === _lastLoadedGameId) return;
	_lastLoadedGameId = gameId;

	try {
		const res = await fetch(`${PUBLIC_BACKEND_URL}/game/${gameId}/parties`);
		if (!res.ok) throw new Error(`Status ${res.status}`);
		const data = await res.json();
		parties.set(data);
	} catch (e) {
		console.error('Failed to load parties', e);
	}
}

export function initGameStateSSE() {
	if (_evtSource) return;

	_evtSource = new EventSource(`${PUBLIC_BACKEND_URL}/sse/game-state`);

	_evtSource.onmessage = (evt) => {
		try {
			const data = JSON.parse(evt.data);

			const user = get(currentUser);
			if (!user.gameId || data.id !== user.gameId) {
				console.log('SSE for wrong game :', 'payload.id=', data.id, 'your gameId=', user.gameId);
				return;
			}

			gameState.update((prev) => {
				// if no previous round, initialize to 0 so that first will be 1 in any case
				let newRoundN = prev.frontend_round_n ?? 0;
				// check for new round
				if (data.current_round_id != null && data.current_round_id !== prev.current_round_id) {
					// double check to start at 1, otherwise increase round by 1
					newRoundN = prev.current_round_id == null ? 1 : newRoundN + 1;
				}

				// check if event changed
				let newEventN = prev.frontend_event_n ?? 0;
				if (
					data.current_voting_event_id != null &&
					data.current_voting_event_id !== prev.current_voting_event_id
				) {
					// same as with round: either 1 or increase by 1
					newEventN = prev.current_voting_event_id == null ? 1 : newEventN + 1;
				}

				return {
					...prev, // keep fields not in SSE
					...data, // overwrite/add only the SSE payload
					frontend_round_n: newRoundN,
					frontend_event_n: newEventN
				};
			});
			getExtraInfo(); // Get latest extra info for user and their party when we receive new SSE
		} catch (e) {
			console.error('Invalid SSE payload:', evt.data, e);
		}
	};

	_evtSource.onerror = (err) => {
		console.error('SSE error, reconnecting…', err);
		_evtSource.close();
		_evtSource = null;
	};
}

export function resetGame() {
	clearUserData();

	gameState.set({
		id: null,
		hash: null,
		name: null,
		status: null,
		current_round_id: null,
		current_voting_event_id: null,
		current_voting_question: null,
		countdown_ends_at: null,
		frontend_round_n: null,
		frontend_event_n: null
	});

	parties.set([]);
	_lastLoadedGameId = null;
}
