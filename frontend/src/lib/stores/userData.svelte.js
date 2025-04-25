import { writable } from 'svelte/store';
import { browser } from '$app/environment';

export const currentUser = writable(
	(browser && JSON.parse(localStorage.getItem('userData'))) || {
		name: '',
		gameId: null,
		userId: null,
		affiliations: {},
		rounds: [],
		votes: {}
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
