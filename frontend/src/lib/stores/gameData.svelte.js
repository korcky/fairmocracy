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
	console.log(`[gameData] loadParties called with gameId=${gameId}`);
	if (gameId === _lastLoadedGameId) {
		console.log('[gameData] same gameId — skipping');
		return;
	}
	_lastLoadedGameId = gameId;

	try {
		const res = await fetch(`${PUBLIC_BACKEND_URL}/game/${gameId}/parties`);
		if (!res.ok) throw new Error(`Status ${res.status}`);
		const data = await res.json();
		console.log('[gameData] loaded parties:', data);
		parties.set(data);
	} catch (e) {
		console.error('[gameData] Failed to load parties:', e);
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
				const next = { ...prev, ...data };

				// first roundId, init to 1
				if (prev.current_round_id == null && data.current_round_id != null) {
					next.frontend_round_n = 1;
					next.frontend_event_n = data.current_voting_event_id != null ? 1 : 0;
					return next;
				}

				// check for new round
				if (prev.current_round_id !== data.current_round_id) {
					// increase round counter
					next.frontend_round_n = (prev.frontend_round_n || 0) + 1;
					// reset event to 1
					next.frontend_event_n = data.current_voting_event_id != null ? 1 : 0;
				}
				// if no new round check for new event
				else if (
					prev.current_voting_event_id !== data.current_voting_event_id &&
					data.current_voting_event_id != null
				) {
					// increase event counter
					next.frontend_event_n = (prev.frontend_event_n || 0) + 1;
				}
				return next;
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
