<script>
	import { PUBLIC_BACKEND_URL } from '$env/static/public';
	import { setUserData } from '$lib/stores/userData.svelte.js';
	import { loadParties, gameState } from '$lib/stores/gameData.svelte.js';
	import { getExtraInfo } from '$lib/stores/userData.svelte.js';

	let gameCode = $state('');
	let error = $state('');

	const onsubmit = async (e) => {
		e.preventDefault();
		error = '';
		console.log('[GameSelection] submitting code', gameCode);

		try {
			const res = await fetch(
				`${PUBLIC_BACKEND_URL}/join?game_hash=${encodeURIComponent(gameCode)}`
			);
			if (!res.ok) {
				error = `Game code submission failed: ${res.status} ${res.statusText}`;
				return;
			}
			const gameObj = await res.json();
			console.log('[GameSelection] joined game, response:', gameObj);

			setUserData({ gameId: gameObj.id });
			gameState.update((prev) => ({
				...prev,
				...gameObj,
				frontend_round_n: gameObj.current_round_id ? 1 : 0,
				frontend_event_n: gameObj.current_voting_event_id ? 1 : 0
			}));
			loadParties(gameObj.id);
			getExtraInfo();
		} catch (err) {
			console.error('[GameSelection] network error:', err);
			error = 'Network error';
		}
	};
</script>

<p class="p-4 text-center text-lg">Enter game code:</p>

<div class="form-container">
	<div class="fields">
		<div class="field">
			<input
				id="game-code"
				value={gameCode}
				oninput={(e) => (gameCode = e.target.value)}
				class="input variant-form-material"
				placeholder="Game code"
			/>
		</div>
		{#if error}
			<p class="mt-1 text-sm text-red-500">{error}</p>
		{/if}
	</div>
	<button onclick={onsubmit} type="submit" class="variant-filled btn bg-blue-500">Enter</button>
</div>

<style>
	.form-container {
		max-width: 90%;
		margin: 0 auto;
		display: flex;
		flex-direction: column;
		gap: 1rem;
		align-items: center;
	}

	.fields {
		display: flex;
		justify-content: center;
		flex-direction: column;
		gap: 1rem;
	}

	.field {
		display: flex;
		flex-direction: column;
		flex: 1;
	}

	.btn {
		color: white;
		transition-property: all;
		transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
		transition-duration: 0.15s;
	}
</style>
