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
	<button type="button" class="variant-filled btn bg-blue-500" onclick={proceed}>
		Proceed to Vote
	</button>
</div>
