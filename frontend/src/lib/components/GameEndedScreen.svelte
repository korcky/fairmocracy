<script>
	import { goto } from '$app/navigation';
	import UserAvatar from './UserAvatar.svelte';
	import { currentUser } from '$lib/stores/userData.svelte.js';
	import { resetGame } from '$lib/stores/gameData.svelte.js';

	function handleNewGame() {
		resetGame();
		goto('/');
	}
</script>

<div class="welcome-container mt-8 flex w-full flex-col items-center justify-center space-y-4">
	<UserAvatar userName={$currentUser.name} party={$currentUser.party} />

	<p>Game ended, thank you for taking part!</p>

	<!-- maybe show results here… -->

	<button type="button" class="variant-filled btn bg-blue-500" onclick={handleNewGame}>
		Start a New Game
	</button>
</div>
