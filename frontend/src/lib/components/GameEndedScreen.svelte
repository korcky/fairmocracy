<script>
	import UserAvatar from './UserAvatar.svelte';
	import { currentUser } from '$lib/stores/userData.svelte.js';
</script>

<div class="welcome-container mt-8 flex w-full flex-col items-center justify-center space-y-4">


	<UserAvatar userName={$currentUser.name} party={$currentUser.party} />

	<p>
		Game ended, thank you for taking part!
	</p>
</div>
