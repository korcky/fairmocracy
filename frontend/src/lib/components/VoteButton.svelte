<script lang="ts">
	import { getToastStore } from '@skeletonlabs/skeleton';
	import type { ToastSettings } from '@skeletonlabs/skeleton';
	let { onVoteGiven, buttonText } = $props();
	let bgColor =
		buttonText === 'YES' ? 'bg-green-500' : buttonText === 'NO' ? 'bg-red-500' : 'bg-gray-500';
	let answer = buttonText;

	const toastStore = getToastStore();

	function vote() {
		const t: ToastSettings = {
			message: `Voted: ${answer} !`,
			timeout: 10000,
			background: bgColor
		};
		if (onVoteGiven) {
			onVoteGiven();
		}
		toastStore.trigger(t);
	}
</script>

<button onclick={vote} type="button" class="btn btn-xl text-5xl font-extrabold {bgColor}">
	{buttonText}
</button>

<style>
	.btn {
		color: whitesmoke;
		width: 80%;
		height: 8rem;
		transition-property: all;
		transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
		transition-duration: 0.15s;
	}
</style>
