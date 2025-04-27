<script>
	import { hasSeenInfo } from '$lib/stores/screenStore.svelte.js';

	function proceed() {
		hasSeenInfo.set(true);
	}
</script>

<div class="info-container mt-8 flex w-full flex-col items-center justify-center space-y-4">
	<p>Info on the law that is going to be voted on</p>
	<button type="button" class="variant-filled btn bg-blue-500" onclick={proceed}
		>Proceed to Vote</button
	>
</div>
