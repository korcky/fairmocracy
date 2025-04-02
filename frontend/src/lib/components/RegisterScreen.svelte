<script>
	import { z } from 'zod';
	import { setUserData, currentUser } from '$lib/stores/userData.svelte.js';
    import { PUBLIC_BACKEND_URL } from "$env/static/public";
	
	let { onRegistration } = $props();
	let name = $state('');
	let party = $state('');
	let errors = $state({});
	let {game} = $currentUser;
	let partyOptions = $state([]);
	
	$inspect(game)
	$inspect(partyOptions)
	$inspect(party)
	$effect(() => {
		if (game) {
			fetch(`${PUBLIC_BACKEND_URL}/parties/game/${game.id}`).then((res) => {
				if (res.ok) {
					res.json().then(respJson => partyOptions = respJson);
				} else {
					errors = { api: ['Failed to fetch parties'] };
				}
			});
		}
	})
	
	let formValidator = z.object({
		name: z.string().nonempty('Name is required'),
		party: z.string()
	});

	const register = () => {
		errors = {};
		try {
			const validatedData = formValidator.parse({ name, party });
			const { name: validName, party: validParty } = validatedData;
			fetch(`${PUBLIC_BACKEND_URL}/register`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ name: validName, party_id: parseInt(party), game_id: game.id })
			}).then((res) => {
				if (res.ok) {
					setUserData({ name: validName, party: validParty, game });
					onRegistration();
				} else {
					errors = { name: ['Registration failed'] };
				}
			})
		} catch (err) {
			console.log(err)
			if (err instanceof z.ZodError) {
				errors = err.flatten().fieldErrors;
			}
		}
		// If the submitted data was fine by our validation standards, signal AppCore
		// to move into waiting room view
	}
</script>

<p class="p-4 text-center text-lg">Please enter your name and select the party you represent.</p>

<div class="form-container">
	<div class="fields">
		<div class="field">
			<label for="name">Name</label>
			<input
				id="name"
				value={name}
				oninput={(e) => (name = e.target.value)}
				class="input variant-form-material"
				placeholder="Enter your name"
			/>
			{#if errors.name}
				<p class="mt-1 text-sm text-red-500">{errors.name[0]}</p>
			{/if}
		</div>
		<div class="field">
			<label for="party">Party</label>
			<select
				id="party"
				name="party"
				onchange={(e) => (party = e.target.value)}
				class="select variant-form-material"
			>	
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
				<p class="mt-1 text-sm text-red-500">Error while fetching party information</p>
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
