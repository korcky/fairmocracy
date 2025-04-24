<script>
	import { onMount } from 'svelte';
	import { writable, derived } from 'svelte/store';
	import RegisterToVoteScreen from './RegisterToVoteScreen.svelte';
	import WelcomeScreen from './WelcomeScreen.svelte';
	import VoteInfoScreen from '$lib/components/VoteInfoScreen.svelte';
	import VoteScreen from '$lib/components/VoteScreen.svelte';
	import VoteWaitScreen from '$lib/components/VoteWaitScreen.svelte';
	import GameSelectionScreen from '$lib/components/GameSelectionScreen.svelte';
	import RegisterScreen from './RegisterScreen.svelte';
	import { currentUser } from '$lib/stores/userData.svelte.js';
	import { gameState, initGameStateSSE, loadParties } from '$lib/stores/gameData.svelte.js';
	import GameEndedScreen from './GameEndedScreen.svelte';

	const currentScreen = writable('select');
	let loadedGameId = null;
	let debug = writable(false);
	onMount(() => {
		initGameStateSSE();

		gameState.subscribe(($game) => {
			if ($game.id && $game.id !== loadedGameId) {
				loadedGameId = $game.id;
				loadParties(loadedGameId);
			}
		});

		derived([currentUser, gameState], ([$user, $game]) => {
			let cs = 'select';
			if ($user.game) {
				if (!$user.userId) cs = 'register';
				else if (!$user.affiliations[$game.current_round_id]) cs = 'registerToVote';
				else if ($game.status === 'started') cs = 'vote';
				else if ($game.status === 'ended') cs = 'end'
				else cs = 'welcome';
			}
			return cs;
		}).subscribe((value) => {
			currentScreen.set(value);
		});
	});

	const handleSelect = () => currentScreen.set('register');
	const handleRegistration = () => currentScreen.set('registerToVote');
	const handleNewVote = () => currentScreen.set('info');
	const handleVoteStart = () => currentScreen.set('vote');
</script>


<button
class="btn btn-primary"
on:click={() => {
	debug.update((d) => !d);
}}>
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

{/if}

{#if $currentScreen === 'select'}
	<GameSelectionScreen {gameState} onSelect={handleSelect} />
{:else if $currentScreen === 'register'}
	<RegisterScreen {gameState} onRegistration={handleRegistration} />
{:else if $currentScreen === 'registerToVote'}
	<RegisterToVoteScreen {gameState}  />
{:else if $currentScreen === 'welcome'}
	<WelcomeScreen {gameState} onNewVote={handleNewVote} />
{:else if $currentScreen === 'info'}
	<VoteInfoScreen {gameState} onVoteStart={handleVoteStart} />
{:else if $currentScreen === 'vote'}
	<VoteScreen {gameState} />
{:else if $currentScreen === 'wait'}
	<VoteWaitScreen {gameState} onNewVote={handleNewVote} />
{:else if $currentScreen === 'end'}
	<GameEndedScreen {gameState} />
{/if}
