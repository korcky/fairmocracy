<script>
	import { ProgressBar } from '@skeletonlabs/skeleton';
	import { onMount } from 'svelte';

	let { time = 60, onVoteStart } = $props();

	let timePassed = $state(0);
	let finished = $state(false);
	const delayHideMs = 1000;

    // Counts from 0 seconds to {time} seconds, which makes the bar update
    // When full, hides and signals for the AppCore to move to voting screen
	onMount(() => {
		const increment = 1;
		const interval = setInterval(() => {
			timePassed = timePassed + increment;
			if (timePassed >= time) {
				timePassed = time;
				clearInterval(interval);
				setTimeout(() => {
					finished = true;
                    if (onVoteStart) {
                        onVoteStart()
                    }
				}, delayHideMs);
			}
		}, 1000);
		return () => clearInterval(interval);
	});
</script>

{#if !finished}
<ProgressBar min={0} max={time} value={timePassed}  height="h-4" meter="bg-blue-600" track="bg-gray-400"/>
{/if}
