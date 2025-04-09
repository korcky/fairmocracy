<script>
	import { z } from 'zod';
	import { setUserData, currentUser } from '$lib/stores/userData.svelte.js';
    import { PUBLIC_BACKEND_URL } from "$env/static/public";
	
	let { onRegistration } = $props();
	let party = $state('');
	let errors = $state({});
	let {game, name, userId, affiliations, rounds } = $currentUser;
	let partyOptions = $state([]);
	let gameState = JSON.parse(game.state);

	$effect(() => {
		if (game) {
			fetch(`${PUBLIC_BACKEND_URL}/parties/game/${game.id}`).then((res) => {
				if (res.ok) {
					res.json().then(respJson => partyOptions = respJson);
				} else {
					errors = { api: ['Failed to fetch parties'] };
				}
			});
			if (!rounds || rounds.length == 0) {
				fetch(`${PUBLIC_BACKEND_URL}/rounds/${game.id}`).then((res) => {
					if (res.ok) {
						res.json().then(respJson => setUserData({ game, name, userId, affiliations, rounds: respJson }));
					} else {
						errors = { api: ['Failed to fetch rounds'] };
					}
				});
			}
		}
	})
	
	let formValidator = z.object({
		party: z.string().nonempty('Select your party')
	});

	const register = () => {
		errors = {};
		try {
			const validatedData = formValidator.parse({  party });
			const { party: validParty } = validatedData;
			fetch(`${PUBLIC_BACKEND_URL}/register_to_vote`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ 
					party_id: parseInt(party),
					round_id: rounds[gameState.current_round].id,
					voter_id: userId })
			}).then((res) => {
				if (res.ok) {
					setUserData({name,game,userId,affiliations: { ...affiliations, [gameState.current_round]: { party: validParty } }});
					onRegistration();
				} else {
					errors = { name: ['Registration failed'] };
				}
			})
		} catch (err) {
			console.error(err)
			if (err instanceof z.ZodError) {
				errors = err.flatten().fieldErrors;
			}
		}
	}
</script>

<p class="p-4 text-center text-lg">Round {gameState.current_round}: select the party you represent.</p>

<div class="form-container">
	<div class="fields">
		<div class="field">
			<label for="party">Party</label>
			<select
				id="party"
				name="party"
				onchange={(e) => (party = e.target.value)}
				class="select variant-form-material"
			>
			<option value="" disabled selected>Select your party</option>
			{#if game}
				{#each partyOptions as p}
					<option value={p.id}>{p.name}</option>
				{/each}
				{/if}
			</select>
			{#if errors.party}
				<p class="mt-1 text-sm text-red-500">Select your party</p>
			{/if}
			{#if errors.api}
				<p class="mt-1 text-sm text-red-500">{errors.api}</p>
			{/if}
		</div>
	</div>
	<button onclick={register} type="button" class="variant-filled btn bg-blue-500">Enter</button>
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
