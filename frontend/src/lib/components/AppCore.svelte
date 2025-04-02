<script>
	import RegisterScreen from './RegisterScreen.svelte';
	import WelcomeScreen from './WelcomeScreen.svelte';
	import VoteInfoScreen from '$lib/components/VoteInfoScreen.svelte';
	import VoteScreen from '$lib/components/VoteScreen.svelte';
	import VoteWaitScreen from '$lib/components/VoteWaitScreen.svelte';
	import GameSelectionScreen from '$lib/components/GameSelectionScreen.svelte';
	import { currentUser } from '$lib/stores/userData.svelte.js';
	// First landing on the page renders the regisster view
	const { game, name, party } = $currentUser;
	console.log(game, name, party)
	let currentScreen = $state('select');
	const handleSelect = () => {
		currentScreen = 'register';
	}
	if (game) {
		currentScreen = 'register';
		if (name && party) {
			currentScreen = 'welcome';
		}
	}

	// After succesfully registered, go to wait room
	const handleRegistration = () =>  {
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
{:else if currentScreen == 'welcome'}
	<WelcomeScreen onNewVote={handleNewVote} />
{:else if currentScreen == 'info'}
	<VoteInfoScreen onVoteStart={handleVoteStart} />
{:else if currentScreen == 'vote'}
	<VoteScreen onVoteGiven={handleVoteGiven} />
{:else if currentScreen == 'wait'}
	<VoteWaitScreen onNewVote={handleNewVote} />
{/if}
