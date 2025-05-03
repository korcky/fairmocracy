import { writable, get } from 'svelte/store';
import { browser } from '$app/environment';
import { gameState } from './gameData.svelte.js';
import { PUBLIC_BACKEND_URL } from '$env/static/public';

let _lastLoadedEventId = null; // To check whether we fetch new extra info
let _inFlightUserExtra = false; // Flag to add extra safety to prevent getExtraInfo from fetching user multiple times
let _inFlightPartyExtra = false; // Same as above but for user's party

export const currentUser = writable(
	(browser && JSON.parse(localStorage.getItem('userData'))) || {
		name: '',
		gameId: null,
		userId: null,
		affiliations: {},
		rounds: [],
		votes: {},
		isAdmin: false,
		gameCode: 'No game code, go to menu -> admin and upload a valid configuration file.',
		extraInfo: null,
		partyExtraInfo: null
	}
);

currentUser.subscribe((value) => {
	if (browser) {
		localStorage.setItem('userData', JSON.stringify(value));
	}
});

export function setUserData(updates) {
	currentUser.update((u) => ({ ...u, ...updates }));
}

export function clearUserData() {
	currentUser.set({
		name: '',
		gameId: null,
		userId: null,
		affiliations: {},
		rounds: [],
		votes: {},
		isAdmin: false,
		gameCode: 'No game code, go to menu -> admin and upload a valid configuration file.',
		extraInfo: null,
		partyExtraInfo: null
	});
	_lastLoadedEventId = null;
	_inFlightUserExtra = false;
	_inFlightPartyExtra = false;
}

export async function getExtraInfo() {
	const { userId, gameId, affiliations } = get(currentUser);
	const { current_round_id: roundId, current_voting_event_id: eventId } = get(gameState);
	if (!userId || !gameId || !roundId || !eventId || eventId === _lastLoadedEventId) return;
	_lastLoadedEventId = eventId;

	// User's personal extra info
	if (!_inFlightUserExtra) {
		_inFlightUserExtra = true;
		try {
			const res = await fetch(`${PUBLIC_BACKEND_URL}/v1/user/${userId}`);
			if (res.ok) {
				const { extra_info } = await res.json();
				// TODO: Check how the actual response for extra info looks like when it's implemented in the backend
				// since it possibly isn't exactly called "extra_info"
				setUserData({ extraInfo: extra_info });
			}
		} catch (e) {
			console.error('Failed to load user extraInfo', e);
		} finally {
			_inFlightUserExtra = false;
		}
	}

	// Extra info for the user's party
	const userPartyId = affiliations[roundId];
	if (userPartyId && !_inFlightPartyExtra) {
		_inFlightPartyExtra = true;
		try {
			const res = await fetch(`${PUBLIC_BACKEND_URL}/game/${gameId}/parties`);
			if (res.ok) {
				const parties = await res.json();
				const userPartyData = parties.find((p) => p.id === userPartyId);
				// TODO: Check how the actual response for extra info looks like when it's implemented in the backend
				// since it possibly isn't exactly called "extra_info"
				if (userPartyData) setUserData({ partyExtraInfo: userPartyData.extra_info });
			}
		} catch (e) {
			console.error('Failed to load party extraInfo', e);
		} finally {
			_inFlightPartyExtra = false;
		}
	}
}
