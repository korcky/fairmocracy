<script lang="ts">
	import { getToastStore } from '@skeletonlabs/skeleton';
	import type { ToastSettings } from '@skeletonlabs/skeleton';
	import { PUBLIC_BACKEND_URL } from '$env/static/public';
	import { currentUser, setUserData } from '$lib/stores/userData.svelte.js';
	import { gameState } from '$lib/stores/gameData.svelte.js';

	let { buttonText } = $props();
	let bgColor = $derived(
		buttonText === 'YES' ? 'bg-green-500' : buttonText === 'NO' ? 'bg-red-500' : 'bg-gray-500'
	);
	let answer = $derived(buttonText);

	const toastStore = getToastStore();

	async function vote() {
		const user = $currentUser;
		const state = $gameState;
		console.log('About to cast vote on event:', state.current_voting_event_id);

		const aff = user.affiliations[state.current_round_id];
		if (!aff) {
			console.error('No affiliation for this round');
			return;
		}

		const payload = {
			voter_id: user.userId,
			voting_event_id: state.current_voting_event_id,
			affiliation_id: aff.id,
			value: answer // "YES" | "NO" | "ABSTAIN"
		};

		try {
			const res = await fetch(`${PUBLIC_BACKEND_URL}/v1/voting/cast_vote`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify(payload)
			});

			if (res.ok) {
				console.log('Vote cast succeeded:', res.json());
				setUserData({
					votes: {
						...user.votes,
						[state.current_voting_event_id]: payload
					}
				});
			} else {
				console.error('Vote cast failed:', await res.text());
			}
		} catch (err) {
			console.error('Network error casting vote:', err);
		}

		const t: ToastSettings = {
			message: `Voted: ${answer}!`,
			timeout: 10000,
			background: bgColor
		};
		toastStore.trigger(t);
	}
</script>

<button onclick={vote} type="button" class="btn btn-xl text-5xl font-extrabold {bgColor}">
	{buttonText}
</button>

<style>
	.btn {
		color: whitesmoke;
		width: 80%;
		height: 8rem;
		transition-property: all;
		transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
		transition-duration: 0.15s;
	}
</style>
