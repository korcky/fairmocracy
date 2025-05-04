<script>
	import { get } from 'svelte/store';
	import { hasSeenInfo } from '$lib/stores/screenStore.svelte.js';
	import { currentUser } from '$lib/stores/userData.svelte.js';
	import { gameState } from '$lib/stores/gameData.svelte.js';

	function proceed() {
		hasSeenInfo.set(true);
	}

	let { current_voting_question: currentQuestion } = get(gameState);
</script>

<div class="info-container mt-8 flex w-full flex-col items-center justify-center space-y-4">
	<p class="w-full max-w-xl whitespace-pre-wrap px-4 text-left text-lg">
		{currentQuestion}
	</p>
	{#if $currentUser.eventRewards}
		<div class="w-full max-w-xl space-y-2 p-4 px-4">
			<p class="font-semibold">If accepted:</p>
			<ul class="ml-6 list-disc">
				<li>You: {$currentUser.eventRewards.accepted} points</li>
				<li>Your party: {$currentUser.partyEventRewards.accepted} points</li>
			</ul>

			<p class="mt-2 font-semibold">If rejected:</p>
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
