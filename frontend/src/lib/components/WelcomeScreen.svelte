<script>
	import UserAvatar from './UserAvatar.svelte';
	import { currentUser } from '$lib/stores/userData.svelte.js';
</script>

<div class="welcome-container mt-8 flex w-full flex-col items-center justify-center space-y-4">
	<p>
		Welcome to fairmocracy {$currentUser.name} !
	</p>

	<UserAvatar userName={$currentUser.name} party={$currentUser.party} />

	<p>Please wait a moment, voting will start soon.</p>
</div>
