<script>
	import UserAvatar from './UserAvatar.svelte';
	import { currentUser } from '$lib/stores/userData.svelte.js';

	let { onNewVote } = $props();
</script>

<div class="welcome-container mt-8 flex w-full flex-col items-center justify-center space-y-4">
	<p>
		Welcome to fairmocracy {$currentUser.name} !
	</p>

    <!-- IDK just trying something :D maybe we can give everyone a random avatar -->
	<UserAvatar userName={$currentUser.name} party={$currentUser.party}  />

	<p>Please wait a moment, voting will start soon.</p>

	<button type="button" class="variant-filled-warning btn" onclick={onNewVote}
		>Demo: Force New Vote</button
	>
</div>
