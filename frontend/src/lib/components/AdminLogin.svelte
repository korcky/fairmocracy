<script>
	import { writable } from 'svelte/store';
	import { currentUser, setUserData } from '$lib/stores/userData.svelte.js';

	let username = '';
	let password = '';
	let error = '';

	let debug = writable(false);

	/**
	 * Very simple login function to give user admin rights
	 * by setting their isAdmin flag to true
	 */
	function handleSubmit() {
		if (username === 'admin' && password === 'admin') {
			error = '';
			setUserData({
				name: 'admin',
				isAdmin: true
			});
		} else {
			error = 'Invalid username or password';
		}
	}
</script>

<button
	class="btn-primary debug"
	onclick={() => {
		debug.update((d) => !d);
	}}
>
	{#if $debug}
		Hide debug
	{:else}
		Show debug
	{/if}
</button>

{#if $debug}
	<h1>Debug: User</h1>
	<pre>Debug currentUser: {JSON.stringify($currentUser, null, 2)}</pre>
{/if}

<form class="mx-auto my-8 w-full max-w-md space-y-4" onsubmit={handleSubmit}>
	<label class="label">
		<span class="label-text">Username</span>
		<input type="text" class="input" placeholder="Enter name" bind:value={username} />
	</label>

	<label class="label">
		<span class="label-text">Password</span>
		<input type="password" class="input" placeholder="Enter Password" bind:value={password} />
	</label>

	{#if error}
		<p class="text-sm text-red-500">{error}</p>
	{/if}

	<button type="submit" class="variant-filled btn mx-auto block bg-blue-500 px-4 py-2 text-white">
		Submit
	</button>
</form>

<style>
	.debug {
		color: black;
	}
	.btn {
		color: white;
		transition-property: all;
		transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
		transition-duration: 0.15s;
	}
</style>
