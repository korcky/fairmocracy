<script>
	import { ProgressRadial } from '@skeletonlabs/skeleton';
	import { onMount } from 'svelte';
	import { fade } from 'svelte/transition';
	import { get } from 'svelte/store';
	import { gameState } from '$lib/stores/gameData.svelte.js';

	const TOTAL_SECONDS = 60; // Fixed max value, change this if needed

	function secondsUntilEnd() {
		const { countdown_ends_at } = get(gameState);
		if (!countdown_ends_at) return 0;

		const endsAtMs =
			typeof countdown_ends_at === 'number' ? countdown_ends_at : Date.parse(countdown_ends_at);

		const diffMs = endsAtMs - Date.now();
		return Math.max(0, Math.ceil(diffMs / 1000));
	}

	let { countdownMessage, finishedMessage } = $props();
	const initialRemaining = secondsUntilEnd();
	const initialPassed = 100 + ((TOTAL_SECONDS - initialRemaining) / TOTAL_SECONDS) * 100;
	let timeRemaining = $state(initialRemaining);
	let timePassed = $state(initialPassed);
	let finished = $state(false);
	let showFinishedMessage = $state(false);
	const delayHideMs = 1000;
	const delayMessageMs = 2000;

	onMount(() => {
		const increment = 100 / TOTAL_SECONDS;
		const interval = setInterval(() => {
			timePassed = timePassed + increment;
			timeRemaining = Math.ceil(TOTAL_SECONDS - (timePassed - 100) / increment);
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
