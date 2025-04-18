<script>
	import { ProgressRadial } from '@skeletonlabs/skeleton';
	import { onMount } from 'svelte';
	import { fade } from 'svelte/transition';

	// Have fun reading this, will comment later :D

	let { countdownTime, countdownMessage, finishedMessage } = $props();
	countdownTime = Number(countdownTime) || 60;
	let timePassed = $state(100);
	let timeRemaining = $state(countdownTime);
	let finished = $state(false);
	let showFinishedMessage = $state(false);
	const delayHideMs = 1000;
	const delayMessageMs = 2000;

	onMount(() => {
		const increment = 100 / countdownTime;
		const interval = setInterval(() => {
			timePassed = timePassed + increment;
			timeRemaining = Math.floor(countdownTime - (timePassed - 100) / increment);
			if (timePassed >= 200) {
				timePassed = 200;
				timeRemaining = 0;
				clearInterval(interval);
				setTimeout(() => {
					finished = true;
				}, delayHideMs);
				setTimeout(() => {
					showFinishedMessage = true;
				}, delayMessageMs);
			}
		}, 1000);

		return () => clearInterval(interval);
	});
</script>

{#if !finished}
	<div transition:fade>
		<p class="mb-4 text-lg">{countdownMessage}</p>
		<ProgressRadial value={timePassed} width="w-64" stroke="60" font="100"
			>{timeRemaining}</ProgressRadial
		>
	</div>
{:else if showFinishedMessage}
	<div transition:fade>
		<p class="text-lg">{finishedMessage}</p>
	</div>
{/if}
