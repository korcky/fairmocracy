<script>
	import Countdown from './Countdown.svelte';
</script>

<div class="countdown-container mt-8 flex w-full flex-col items-center justify-center space-y-10">
	<Countdown
		countdownMessage="Waiting for others to finish voting."
		finishedMessage="Waiting for next round of voting."
	/>
</div>
