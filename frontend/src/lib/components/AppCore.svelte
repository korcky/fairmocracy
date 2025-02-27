<script>
	import RegisterScreen from './RegisterScreen.svelte';
	import WelcomeScreen from './WelcomeScreen.svelte';
	import VoteInfoScreen from '$lib/components/VoteInfoScreen.svelte';
	import VoteScreen from '$lib/components/VoteScreen.svelte';
	import VoteWaitScreen from '$lib/components/VoteWaitScreen.svelte';

	// First landing on the page renders the regisster view
	let currentScreen = $state('register');

	// After succesfully registered, go to wait room
	function handleRegistration() {
		currentScreen = 'welcome';
	}

	// New law is introduced, currently manually called in app
	// TODO: External API call triggers new vote
	function handleNewVote() {
		currentScreen = 'info';
	}

	// After set time or manually, enter the voting screen
	function handleVoteStart() {
		currentScreen = 'vote';
	}

	// After user gives their vote, show remaining time for others,
    // and start wating for new law to be introduced
	function handleVoteGiven() {
		currentScreen = 'wait';
	}
</script>

{#if currentScreen == 'register'}
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
