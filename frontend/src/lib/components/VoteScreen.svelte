<script>
	import VoteButton from './VoteButton.svelte';
	let { onVoteGiven } = $props();
</script>

<p class="p-4 text-center text-lg">Do you support this law?</p>

<div class="button-container p-4 mx-0 my-auto flex flex-col gap-2 items-center justify-center">
	<VoteButton buttonText="YES" onVoteGiven={onVoteGiven} />
	<VoteButton buttonText="NO" onVoteGiven={onVoteGiven} />
	<VoteButton buttonText="EMPTY" onVoteGiven={onVoteGiven} />
</div>
