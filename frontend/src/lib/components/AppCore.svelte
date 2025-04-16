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
	import { writable } from 'svelte/store';
	import { browser } from '$app/environment'

	// Listen to backend server sent events
	const gameState = writable({});
	//if (browser) {
	//	const evtSource = new EventSource(`${PUBLIC_BACKEND_URL}/sse/game-state`);
	//	evtSource.onmessage = function(event) {
	//		console.log(event)
	//		var dataobj = JSON.parse(event.data);
	//		gameState.update(dataobj);
	//	}
	//	evtSource.onerror = function(event) {
	//		console.log("Error: ", event);
	//	};
	//}

	//const gameState = selectJsonEvent(connection, 'message');


	const { game, name, affiliations, } = $currentUser;
    let poller
	const setupPoller = (id) => {
        if (poller) {
            clearInterval(poller)
        }
        poller = setInterval(doPoll(id), 2000)
	}

	const doPoll = (id) => async () => {
        const response = await fetch(`${PUBLIC_BACKEND_URL}/v1/voting/${id}/state`, {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json'
			}
		})
		if (response.ok) {
			const data = await response.json()
			gameState.set(data)}
        
    }
	if (game && game.id) {
		console.log("polling")
		setupPoller(game.id)	
	}

	let currentScreen = 'select';
	
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

	if (game && gameState.status == "started") {
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
	<GameSelectionScreen gameState={gameState} onSelect={handleSelect} />
{:else if currentScreen == 'register'}
	<RegisterScreen gameState={gameState} onRegistration={handleRegistration} />
{:else if currentScreen == 'registerToVote'}
	<RegisterToVoteScreen gameState={gameState} onRegistration={handleRegisterToVote} />
{:else if currentScreen == 'welcome'}
	<WelcomeScreen gameState={gameState} onNewVote={handleNewVote} />
{:else if currentScreen == 'info'}
	<VoteInfoScreen gameState={gameState} onVoteStart={handleVoteStart} />
{:else if currentScreen == 'vote'}
	<VoteScreen gameState={gameState} onVoteGiven={handleVoteGiven} />
{:else if currentScreen == 'wait'}
	<VoteWaitScreen gameState={gameState} onNewVote={handleNewVote} />
{/if}
