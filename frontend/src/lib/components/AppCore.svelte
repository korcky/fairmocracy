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

	const currentScreen = writable('select');
	let loadedGameId = null;

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
				if (!$user.name) cs = 'register';
				else if (!$user.affiliations[$user.game.current_round]) cs = 'registerToVote';
				else if ($game.status === 'started') cs = 'vote';
				else cs = 'welcome';
			}
			return cs;
		}).subscribe((value) => {
			currentScreen.set(value);
		});
	});

	const handleSelect = () => currentScreen.set('register');
	const handleRegistration = () => currentScreen.set('registerToVote');
	const handleRegisterToVote = () => currentScreen.set('welcome');
	const handleNewVote = () => currentScreen.set('info');
	const handleVoteStart = () => currentScreen.set('vote');
	const handleVoteGiven = () => currentScreen.set('wait');
</script>

<h1>Debug: Game State</h1>
<pre>Debug gameState: {JSON.stringify($gameState, null, 2)}</pre>

{#if $currentScreen === 'select'}
	<GameSelectionScreen {gameState} onSelect={handleSelect} />
{:else if $currentScreen === 'register'}
	<RegisterScreen {gameState} onRegistration={handleRegistration} />
{:else if $currentScreen === 'registerToVote'}
	<RegisterToVoteScreen {gameState} onRegistration={handleRegisterToVote} />
{:else if $currentScreen === 'welcome'}
	<WelcomeScreen {gameState} onNewVote={handleNewVote} />
{:else if $currentScreen === 'info'}
	<VoteInfoScreen {gameState} onVoteStart={handleVoteStart} />
{:else if $currentScreen === 'vote'}
	<VoteScreen {gameState} onVoteGiven={handleVoteGiven} />
{:else if $currentScreen === 'wait'}
	<VoteWaitScreen {gameState} onNewVote={handleNewVote} />
{/if}
