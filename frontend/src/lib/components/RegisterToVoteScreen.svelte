<script>
	import { z } from 'zod';
	import { setUserData, currentUser } from '$lib/stores/userData.svelte.js';
	import { gameState, parties } from '$lib/stores/gameData.svelte.js';
	import { PUBLIC_BACKEND_URL } from '$env/static/public';

	let selectedParty = $state('');
	let errors = $state({});

	let formValidator = z.object({
		party: z.string().nonempty('Select your party')
	});

	async function registerToVote() {
		errors = {};

		const user = $currentUser;
		const gstate = $gameState;

		// validate selection
		try {
			formValidator.parse({ party: selectedParty });
		} catch (err) {
			errors = err.flatten().fieldErrors;
			return;
		}

		try {
			const res = await fetch(`${PUBLIC_BACKEND_URL}/register_to_vote`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({
					voter_id: user.userId,
					round_id: gstate.current_round_id,
					party_id: parseInt(selectedParty, 10)
				})
			});

			if (!res.ok) {
				console.error('[RegisterToVote] failed:', res.status, await res.text());
				errors = { api: ['Registration failed'] };
				return;
			}

			const affiliation = await res.json();
			console.log('[RegisterToVote] affiliation:', affiliation);

			setUserData({
				affiliations: {
					...user.affiliations,
					[affiliation.round_id]: affiliation.id
				}
			});
		} catch (e) {
			console.error('[RegisterToVote] error', e);
			errors = { api: ['Something went wrong'] };
		}
	}
</script>

<p class="p-4 text-center text-lg">
	Round {$gameState.frontend_round_n}: select the party you represent.
</p>

<div class="form-container">
	<div class="fields">
		<div class="field">
			<label for="party">Party</label>
			<select
				id="party"
				name="party"
				onchange={(e) => (selectedParty = e.target.value)}
				class="select variant-form-material"
			>
				<option value="" disabled selected>Select your party</option>
				{#each $parties as p}
					<option value={p.id}>{p.name}</option>
				{/each}
			</select>
			{#if errors.party}
				<p class="mt-1 text-sm text-red-500">Select your party</p>
			{/if}
			{#if errors.api}
				<p class="mt-1 text-sm text-red-500">{errors.api}</p>
			{/if}
		</div>
	</div>
	<button onclick={registerToVote} type="button" class="variant-filled btn bg-blue-500"
		>Enter</button
	>
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

	.field label {
		margin-bottom: 0.5rem;
		font-weight: bold;
	}

	.btn {
		color: white;
		transition-property: all;
		transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
		transition-duration: 0.15s;
	}
</style>
