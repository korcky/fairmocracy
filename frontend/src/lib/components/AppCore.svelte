<script>
	// Svelte imports
	import { onMount } from 'svelte';
	import { writable } from 'svelte/store';

	// Screen imports
	import GameSelectionScreen from '$lib/components/GameSelectionScreen.svelte';
	import WelcomeScreen from './WelcomeScreen.svelte';
	import RegisterScreen from './RegisterScreen.svelte';
	import RegisterToVoteScreen from './RegisterToVoteScreen.svelte';
	import VoteInfoScreen from '$lib/components/VoteInfoScreen.svelte';
	import VoteScreen from '$lib/components/VoteScreen.svelte';
	import VoteWaitScreen from '$lib/components/VoteWaitScreen.svelte';
	import GameEndedScreen from './GameEndedScreen.svelte';

	// Store imports
	import { currentUser } from '$lib/stores/userData.svelte.js';
	import { gameState, initGameStateSSE, loadParties } from '$lib/stores/gameData.svelte.js';
	import { currentScreen } from '$lib/stores/screenStore.svelte.js';

	let debug = writable(false);

	let _lastLoadedGameId = null;

	onMount(() => {
		initGameStateSSE();

		gameState.subscribe(($game) => {
			if ($game.id && $game.id !== _lastLoadedGameId) {
				_lastLoadedGameId = $game.id;
				loadParties($game.id);
			}
		});
	});
</script>

<button
	class="btn-primary btn"
	on:click={() => {
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
	<h1>Debug: Game State</h1>
	<pre>Debug gameState: {JSON.stringify($gameState, null, 2)}</pre>
	<h1>Debug: User Data</h1>
	<pre>Debug currentUser: {JSON.stringify($currentUser, null, 2)}</pre>
	<h1>Debug: Screen</h1>
	<pre>Debug currentScreen: {JSON.stringify($currentScreen, null, 2)}</pre>
{/if}

{#if $currentScreen === 'select'}
	<GameSelectionScreen />
{:else if $currentScreen === 'register'}
	<RegisterScreen />
{:else if $currentScreen === 'registerToVote'}
	<RegisterToVoteScreen />
{:else if $currentScreen === 'welcome'}
	<WelcomeScreen />
{:else if $currentScreen === 'info'}
	<VoteInfoScreen />
{:else if $currentScreen === 'vote'}
	<VoteScreen />
{:else if $currentScreen === 'wait'}
	<VoteWaitScreen />
{:else if $currentScreen === 'end'}
	<GameEndedScreen />
{/if}
