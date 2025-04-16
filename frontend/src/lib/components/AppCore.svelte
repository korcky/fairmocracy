<script>
	import RegisterToVoteScreen from './RegisterToVoteScreen.svelte';
	import WelcomeScreen from './WelcomeScreen.svelte';
	import VoteInfoScreen from '$lib/components/VoteInfoScreen.svelte';
	import VoteScreen from '$lib/components/VoteScreen.svelte';
	import VoteWaitScreen from '$lib/components/VoteWaitScreen.svelte';
	import GameSelectionScreen from '$lib/components/GameSelectionScreen.svelte';
	import RegisterScreen from './RegisterScreen.svelte';
	import { currentUser } from '$lib/stores/userData.svelte.js';
	import { PUBLIC_BACKEND_URL } from '$env/static/public';
	import { createSSEConnection, selectJsonEvent } from '$lib/services/sseService.js'

	// Listen to backend server sent events
	const connection = createSSEConnection(`${PUBLIC_BACKEND_URL}/sse/game-state`)
	const jsonData = selectJsonEvent(connection, 'message');

	const { game, name, affiliations, userId } = $currentUser;

	let currentScreen = $state('select');
	const handleSelect = () => {
		currentScreen = 'register';
	}
	if (game) {
		if (name) {
			if (affiliations[game.current_round]) {
			currentScreen = 'welcome';
		} else {
			currentScreen = 'registerToVote';
		
		} } else {
			currentScreen = 'register'
		}
	} else {
		currentScreen = 'select';
	}

	if (game && game.state.active) {
		currentScreen = 'vote'

	}

	// After succesfully registered, go to wait room
	const handleRegistration = () =>  {
		currentScreen = 'registerToVote';
	}

	const handleRegisterToVote = () => {
		currentScreen = 'welcome';
	}

	// New law is introduced, currently manually called in app
	// TODO: External API call triggers new vote
	const handleNewVote = () => {
		currentScreen = 'info';
	}

	// After set time or manually, enter the voting screen
	const handleVoteStart = () => {
		currentScreen = 'vote';
	}

	// After user gives their vote, show remaining time for others,
    // and start wating for new law to be introduced
	const handleVoteGiven = () => {
		currentScreen = 'wait';
	}
</script>


{#if currentScreen == 'select'}
	<GameSelectionScreen onSelect={handleSelect} />
{:else if currentScreen == 'register'}
	<RegisterScreen onRegistration={handleRegistration} />
{:else if currentScreen == 'registerToVote'}
	<RegisterToVoteScreen onRegistration={handleRegisterToVote} />
{:else if currentScreen == 'welcome'}
	<WelcomeScreen onNewVote={handleNewVote} />
{:else if currentScreen == 'info'}
	<VoteInfoScreen onVoteStart={handleVoteStart} />
{:else if currentScreen == 'vote'}
	<VoteScreen onVoteGiven={handleVoteGiven} />
{:else if currentScreen == 'wait'}
	<VoteWaitScreen onNewVote={handleNewVote} />
{/if}
