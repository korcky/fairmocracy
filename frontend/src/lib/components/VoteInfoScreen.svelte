<script>
	import ProgressBar from './ProgressBar.svelte';

	let { onVoteStart } = $props();
</script>

<div class="info-container mt-8 flex w-full flex-col items-center justify-center space-y-4">
	<p>Info on the law that is going to be voted on</p>
	<ProgressBar time="10" {onVoteStart} />
	<button type="button" class="variant-filled-warning btn" onclick={onVoteStart}
		>Demo: Force Vote Screen</button
	>
</div>
