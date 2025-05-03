<script>
	import { hasSeenInfo } from '$lib/stores/screenStore.svelte.js';
	import { gameState, parties} from '$lib/stores/gameData.svelte.js';
	import { currentUser } from '$lib/stores/userData.svelte.js';
	import { PUBLIC_BACKEND_URL } from '$env/static/public';
	import { onMount } from 'svelte';
	
	console.log($parties);
	let selectedParty = '';
	let user = $currentUser;
	let RoundId = $gameState.current_round_id;
	let affiliationId = user.affiliations[RoundId];
	if (affiliationId.party_id && $parties.length > 0) {
			const party = $parties.find(p => p.id === affiliationId.party_id);
			selectedParty = party.name ?? 'Unknown';
		}
	console.log("RoundId" , RoundId);
	console.log("user affiliation" , affiliationId);
	console.log("User party" , affiliationId.party_id);
	console.log("User party" , selectedParty);

	let previousId = null;
	let roundsLeft = 0;

	onMount(() => {
		if ($gameState.id) {
			const gameId = $gameState.id;
			fetch(`${PUBLIC_BACKEND_URL}/game/${gameId}/rounds`)
				.then(res => res.json())
				.then(data => {
					const totalRounds = data.length;
					const currentIndex = data.findIndex(r => r.id === $gameState.current_round_id);
					roundsLeft = totalRounds - currentIndex - 1;
					console.log("Round completed, remaining rounds: ", roundsLeft);
				})
				.catch(e => console.error("Failed to load rounds", e));
	}
	});

	function proceed() {
		hasSeenInfo.set(true);
	}

</script>

<div class="info-container mt-8 flex w-full flex-col items-center justify-center space-y-4">
	<!-- Display user-specific info -->
	<p class="text-lg font-semibold">Name: {user.name}</p>
	<p>Your selected party: {selectedParty}</p>
	<p>Voting rounds ahead: {roundsLeft}</p>

	<!-- Proceed button -->
	<button type="button" class="variant-filled btn bg-blue-500" on:click={proceed}>
		Proceed to Vote
	</button>
</div>
