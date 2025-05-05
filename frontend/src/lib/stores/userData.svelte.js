import { writable, get } from 'svelte/store';
import { browser } from '$app/environment';
import { gameState } from './gameData.svelte.js';
import { PUBLIC_BACKEND_URL } from '$env/static/public';

let _lastLoadedUserId = null;
let _lastLoadedEventId = null; // To check whether we fetch new extra info
let _inFlightUserExtra = false; // Flag to add extra safety to prevent getExtraInfo from fetching user multiple times
let _inFlightPartyExtra = false; // Same as above but for user's party
let _lastLoadedAffiliationId = null;

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
		partyExtraInfo: null,
		eventRewards: null,
		partyEventRewards: null
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
		partyExtraInfo: null,
		eventRewards: null,
		partyEventRewards: null
	});
	_lastLoadedEventId = null;
	_inFlightUserExtra = false;
	_inFlightPartyExtra = false;
}

export async function getExtraInfo() {
	const { userId, gameId, affiliations } = get(currentUser);
	const {
		current_round_id: roundId,
		current_voting_event_id: eventId,
		voting_system: sys,
		extra_info: extra
	} = get(gameState);

	if (!userId || !gameId || !roundId || !eventId || !sys || !extra) {
		return;
	}

	const { affiliation_id: currentAffId, party_id: userPartyId } = affiliations[roundId] || {};

	if (userId !== _lastLoadedUserId) {
		_lastLoadedEventId = null;
		_lastLoadedAffiliationId = null;
	}

	if (currentAffId !== _lastLoadedAffiliationId) {
		_lastLoadedEventId = null;
	}

	if (eventId === _lastLoadedEventId) {
		return;
	}

	_lastLoadedUserId = userId;
	_lastLoadedEventId = eventId;
	_lastLoadedAffiliationId = currentAffId;

	// User's personal extra info
	if (!_inFlightUserExtra) {
		_inFlightUserExtra = true;
		try {
			const res = await fetch(`${PUBLIC_BACKEND_URL}/v1/user/${userId}`);
			if (res.ok) {
				const { extra_info } = await res.json();
				setUserData({ extraInfo: extra_info });
			}
		} catch (e) {
			console.error('[getExtraInfo] Failed to load user extraInfo', e);
		} finally {
			_inFlightUserExtra = false;
		}
	}

	// Extra info for the user's party
	if (userPartyId && !_inFlightPartyExtra) {
		_inFlightPartyExtra = true;
		try {
			const res = await fetch(`${PUBLIC_BACKEND_URL}/game/${gameId}/parties`);
			if (res.ok) {
				const parties = await res.json();
				const p = parties.find((x) => x.id === userPartyId);
				setUserData({ partyExtraInfo: p?.extra_info || {} });
			}
		} catch (e) {
			console.error('[getExtraInfo] Failed to load party extraInfo', e);
		} finally {
			_inFlightPartyExtra = false;
		}
	}

	const tables = extra[sys] || { ACCEPTED: {}, REJECTED: {} };

	const uid = String(userId);
	const pid = String(userPartyId);

	const userRewards = {
		accepted: tables.ACCEPTED.voters?.[uid] ?? 0,
		rejected: tables.REJECTED.voters?.[uid] ?? 0
	};

	const partyRewards = {
		accepted: tables.ACCEPTED.parties?.[pid] ?? 0,
		rejected: tables.REJECTED.parties?.[pid] ?? 0
	};

	setUserData({
		eventRewards: userRewards,
		partyEventRewards: partyRewards
	});
}
