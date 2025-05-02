<script>
	import { hasSeenInfo } from '$lib/stores/screenStore.svelte.js';
	import { gameState, parties} from '$lib/stores/gameData.svelte.js';
	import { currentUser } from '$lib/stores/userData.svelte.js';
	import { PUBLIC_BACKEND_URL } from '$env/static/public';
	
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

	let totalRounds = 0;
	let roundsLeft = 0;

	$: if ($gameState.id) {
		const gameId = $gameState.id;
		fetch(`${PUBLIC_BACKEND_URL}/game/${gameId}/rounds`)
			.then(res => res.json())
			.then(data => {
				totalRounds = data.length;
				roundsLeft = totalRounds;
				console.log("Loaded total rounds:", totalRounds);
			})
			.catch(e => console.error("Failed to load rounds", e));
	}
	 // Watch for round updates and decrease totalRounds
	$: if ($gameState.current_round_id !== RoundId) {
		// Ensure we only update RoundId when the round is truly changing
		RoundId = $gameState.current_round_id;
		if (roundsLeft > 0) {
		roundsLeft -= 1; // Decrease rounds when the current round changes
		}
		console.log("Round completed, remaining rounds: ", roundsLeft);
  	}

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
