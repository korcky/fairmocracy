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
	import { PUBLIC_BACKEND_URL } from '$env/static/public';

	const gameState = writable({});
	const currentScreen = writable('select');

	onMount(() => {
		const evtSource = new EventSource(`${PUBLIC_BACKEND_URL}/sse/game-state`);
		evtSource.onmessage = (event) => {
			console.log('Received SSE event:', event.data);
			try {
				const data = JSON.parse(event.data);
				gameState.set(data);
			} catch (e) {
				console.error('Failed to parse SSE event as JSON:', event.data, e);
			}
		};
		evtSource.onerror = (error) => {
			console.error('EventSource error:', error);
		};
		return () => {
			evtSource.close();
		};
	});

	derived([currentUser, gameState], ([$currentUser, $gameState]) => {
		let cs = 'select';
		if ($currentUser.game) {
			if ($currentUser.name) {
				if ($currentUser.affiliations[$currentUser.game.current_round]) {
					cs = 'welcome';
				} else {
					cs = 'registerToVote';
				}
			} else {
				cs = 'register';
			}
		}
		if ($currentUser.game && $gameState && $gameState.status === 'started') {
			cs = 'vote';
		}
		return cs;
	}).subscribe((value) => {
		currentScreen.set(value);
	});

	const handleSelect = () => currentScreen.set('register');
	const handleRegistration = () => currentScreen.set('registerToVote');
	const handleRegisterToVote = () => currentScreen.set('welcome');
	const handleNewVote = () => currentScreen.set('info');
	const handleVoteStart = () => currentScreen.set('vote');
	const handleVoteGiven = () => currentScreen.set('wait');
</script>

<h1>Debug: Game State</h1>
<pre>{JSON.stringify($gameState, null, 2)}</pre>

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
