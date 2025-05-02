import { writable, get } from 'svelte/store';
import { PUBLIC_BACKEND_URL } from '$env/static/public';
import { currentUser, clearUserData } from './userData.svelte.js';

export const parties = writable([]);
export const rounds = writable([]);
export const gameState = writable({
	id: null,
	hash: null,
	name: null,
	status: null,
	current_round_id: null,
	current_voting_event_id: null
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
		console.log('Parties loaded:', data);
	} catch (e) {
		console.error('Failed to load parties', e);
	}
}

export async function loadRounds(gameId) {
	if (gameId === _lastLoadedGameId) return;
	_lastLoadedGameId = gameId;

	try {
		const res = await fetch(`${PUBLIC_BACKEND_URL}/game/${gameId}/rounds`);
		if (!res.ok) throw new Error(`Status ${res.status}`);
		const data = await res.json();
		rounds.set(data);
		console.log('Rounds loaded:', data);
	} catch (e) {
		console.error('Failed to load rounds', e);
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

			gameState.set(data);
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
		current_voting_event_id: null
	});

	parties.set([]);
	_lastLoadedGameId = null;
}