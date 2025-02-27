<script>
	import { z } from 'zod';
	import { setUserData } from '$lib/stores/userData.svelte.js';

	let { onRegistration } = $props();

	let name = $state('');
	let party = $state('');
	let errors = $state({});
	let success = $state(false);

	const formValidator = z.object({
		name: z.string().nonempty('Name is required'),
		party: z.enum(['red', 'blue'])
	});

	// Register function that uses zod for validating the inputs. Does not
	// store persistent data yet, need to implement cookies or something
	function register() {
		errors = {};
		try {
			const validatedData = formValidator.parse({ name, party });
			const { name: validName, party: validParty } = validatedData;
			setUserData(validName, validParty);
			success = true;
		} catch (err) {
			if (err instanceof z.ZodError) {
				errors = err.flatten().fieldErrors;
			}
		}
		// If the submitted data was fine by our validation standards, signal AppCore
		// to move into waiting room view
		if (success) {
			onRegistration();
		}
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
				value={party}
				oninput={(e) => (party = e.target.value)}
				class="select variant-form-material"
			>
				<option value=""></option>
				<option value="red">Red</option>
				<option value="blue">Blue</option>
			</select>
			{#if errors.party}
				<p class="mt-1 text-sm text-red-500">Select your party</p>
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
