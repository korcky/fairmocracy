import { writable } from 'svelte/store';
import { PUBLIC_BACKEND_URL } from '$env/static/public';

export const parties = writable([]);

export async function loadParties(gameId) {
	try {
		const res = await fetch(`${PUBLIC_BACKEND_URL}/game/${gameId}/parties`);
		if (!res.ok) throw new Error(`Status ${res.status}`);
		const data = await res.json();
		parties.set(data);
	} catch (e) {
		console.error('Failed to load parties', e);
	}
}
