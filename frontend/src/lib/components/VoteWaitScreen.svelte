<script>
	import Countdown from './Countdown.svelte';
	let { onNewVote } = $props();
</script>

<div class="countdown-container mt-8 flex w-full flex-col items-center justify-center space-y-10">
	<Countdown
		countdownTime="60"
		countdownMessage="Waiting for others to finish voting."
		finishedMessage="Waiting for next round of voting."
	/>
	<button type="button" class="variant-filled-warning btn" onclick={onNewVote}
		>Demo: Force New Vote</button
	>
</div>
