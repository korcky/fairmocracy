import { writable, get } from 'svelte/store';
import { browser } from '$app/environment';
import { gameState } from './gameData.svelte.js';
import { PUBLIC_BACKEND_URL } from '$env/static/public';

let _lastLoadedUserId = null;
let _lastLoadedEventId = null; // To check whether we fetch new extra info
let _inFlightUserExtra = false; // Flag to add extra safety to prevent getExtraInfo from fetching user multiple times
let _inFlightPartyExtra = false; // Same as above but for user's party
let _inFlightEventRewards = false; // For current event's rewards

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
	_inFlightEventRewards = false;
}

export async function getExtraInfo() {
	const { userId, gameId, affiliations } = get(currentUser);
	const { current_round_id: roundId, current_voting_event_id: eventId } = get(gameState);
	if (!userId || !gameId || !roundId || !eventId) return;

	if (userId !== _lastLoadedUserId) {
		_lastLoadedEventId = null;
	}

	if (eventId === _lastLoadedEventId) return;

	_lastLoadedEventId = eventId;
	_lastLoadedUserId = userId;

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
				if (userPartyData) setUserData({ partyExtraInfo: userPartyData?.extra_info || {} });
			}
		} catch (e) {
			console.error('Failed to load party extraInfo', e);
		} finally {
			_inFlightPartyExtra = false;
		}
	}

	// Get possible rewards for the event
	if (!_inFlightEventRewards) {
		_inFlightEventRewards = true;
		try {
			const res = await fetch(`${PUBLIC_BACKEND_URL}/v1/voting/current_state/${gameId}`);
			if (res.ok) {
				const evt = await res.json();
				const sys = evt.voting_system;
				const rewards = evt.extra_info?.[sys] || {};
				// rewards should be like { ACCEPTED: { voters: {…}, parties: {…} }, REJECTED: { … } }

				// user individual rewards (default 0):
				const userRewards = {
					accepted: rewards.ACCEPTED?.voters?.[userId] ?? 0,
					rejected: rewards.REJECTED?.voters?.[userId] ?? 0
				};

				// party rewards (default 0):
				const partyAccepted = rewards.ACCEPTED?.parties || {};
				const partyRejected = rewards.REJECTED?.parties || {};
				const userPartyId = affiliations[roundId];
				const userPartyRewards = {
					accepted: partyAccepted[userPartyId] ?? 0,
					rejected: partyRejected[userPartyId] ?? 0
				};

				setUserData({
					eventRewards: userRewards,
					partyEventRewards: userPartyRewards
				});
			}
		} catch (e) {
			console.error('Failed to load rewards for event', e);
		} finally {
			_inFlightEventRewards = false;
		}
	}
}
