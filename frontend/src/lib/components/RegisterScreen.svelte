<script>
	import { z } from 'zod';
	import { setUserData, currentUser } from '$lib/stores/userData.svelte.js';
	import { PUBLIC_BACKEND_URL } from '$env/static/public';

	let { onRegistration } = $props();
	let name = $state('');
	let errors = $state({});
	let { game } = $currentUser;

	let formValidator = z.object({
		name: z.string().nonempty('Name is required')
	});

	const register = () => {
		errors = {};
		try {
			const validatedData = formValidator.parse({ name });
			const { name: validName } = validatedData;

			fetch(`${PUBLIC_BACKEND_URL}/register`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ name: validName, game_id: game.id })
			}).then((res) => {
				if (res.ok) {
					res.json().then((respJson) => {
						setUserData({ game, name: respJson.name, userId: respJson.id });
						onRegistration();
					});
				} else {
					errors = { name: ['Registration failed'] };
				}
			});
		} catch (err) {
			console.error(err);
			if (err instanceof z.ZodError) {
				errors = err.flatten().fieldErrors;
			}
		}
		// If the submitted data was fine by our validation standards, signal AppCore
		// to move into waiting room view
	};
</script>

<p class="p-4 text-center text-lg">Please enter your name to join the game.</p>

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
