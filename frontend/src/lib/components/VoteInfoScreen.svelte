<script>
	import { get } from 'svelte/store';
	import { hasSeenInfo } from '$lib/stores/screenStore.svelte.js';
	import { gameState, parties } from '$lib/stores/gameData.svelte.js';
	import { currentUser } from '$lib/stores/userData.svelte.js';
	import { PUBLIC_BACKEND_URL } from '$env/static/public';
	import { onMount } from 'svelte';

	console.log($parties);
	let selectedParty = '';
	let user = $currentUser;
	let RoundId = $gameState.current_round_id;
	let affiliationId = user.affiliations[RoundId];
	if (affiliationId.party_id && $parties.length > 0) {
		const party = $parties.find((p) => p.id === affiliationId.party_id);
		selectedParty = party.name ?? 'Unknown';
	}
	console.log('RoundId', RoundId);
	console.log('user affiliation', affiliationId);
	console.log('User party', affiliationId.party_id);
	console.log('User party', selectedParty);

	let questionsLeft = 0;
	let roundsLeft = 0;

	onMount(() => {
		if ($gameState.id) {
			const gameId = $gameState.id;
			fetch(`${PUBLIC_BACKEND_URL}/game/${gameId}/rounds`)
				.then((res) => res.json())
				.then((data) => {
					const totalRounds = data.length;
					const currentIndex = data.findIndex((r) => r.id === $gameState.current_round_id);
					roundsLeft = totalRounds - currentIndex - 1;
					console.log('Round completed, remaining rounds: ', roundsLeft);
				})
				.catch((e) => console.error('Failed to load rounds', e));
		}

		if ($gameState.current_round_id) {
			const roundId = $gameState.current_round_id;
			fetch(`${PUBLIC_BACKEND_URL}/round/${roundId}/voting_events`)
				.then((res) => res.json())
				.then((data) => {
					const totalQ = data.length;
					const currentevent = data.findIndex((r) => r.id === $gameState.current_voting_event_id);
					questionsLeft = totalQ - currentevent;
					console.log('Voting events left: ', questionsLeft);
				})
				.catch((e) => console.error('Failed to load voting events', e));
		}
	});

	function proceed() {
		hasSeenInfo.set(true);
	}

	let { current_voting_question: currentQuestion } = get(gameState);
</script>

<div class="info-container mt-8 flex w-full flex-col items-center justify-center space-y-4">
	<p class="text-lg font-semibold">Name: {user.name}</p>
	<p>Your selected party: {selectedParty}</p>
	<p>Voting rounds ahead: {roundsLeft} Voting round questions ahead: {questionsLeft}</p>
	<p class="w-full max-w-xl whitespace-pre-wrap px-4 text-left text-lg">
		{currentQuestion}
	</p>
	{#if $currentUser.eventRewards}
		<div class="w-full max-w-xl space-y-2 p-4 px-4">
			<p class="font-semibold">If proposal is accepted:</p>
			<ul class="ml-6 list-disc">
				<li>You: {$currentUser.eventRewards.accepted} points</li>
				<li>Your party: {$currentUser.partyEventRewards.accepted} points</li>
			</ul>

			<p class="mt-2 font-semibold">If proposal is rejected:</p>
			<ul class="ml-6 list-disc">
				<li>You: {$currentUser.eventRewards.rejected} points</li>
				<li>Your party: {$currentUser.partyEventRewards.rejected} points</li>
			</ul>
		</div>
	{/if}
	<button type="button" class="variant-filled btn bg-blue-500" onclick={proceed}>
		Proceed to Vote
	</button>
</div>
