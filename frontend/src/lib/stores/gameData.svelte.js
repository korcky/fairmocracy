import { writable } from 'svelte/store';
import { PUBLIC_BACKEND_URL } from '$env/static/public';

export const parties = writable([]);

let _lastLoadedGameId = null;

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

export const gameState = writable({
	id: null,
	hash: null,
	name: null,
	status: null,
	current_round: null,
	current_voting_event_id: null,
	voting_event: {
		title: null,
		content: null,
		extra_info: null,
		votes: [],
	}
	// Whatever else we need
});

let _evtSource = null;

export function initGameStateSSE() {
	if (_evtSource) return;

	_evtSource = new EventSource(`${PUBLIC_BACKEND_URL}/sse/game-state`);
	_evtSource.onmessage = (evt) => {
		console.log('Received SSE:', evt.data);
		try {
			const data = JSON.parse(evt.data);
			gameState.set(data);
		} catch (e) {
			console.error('Invalid SSE payload:', evt.data, e);
		}
	};
	_evtSource.onerror = (err) => {
		console.error('SSE error, reconnecting', err);
		_evtSource.close();
		_evtSource = null;
	};
}
