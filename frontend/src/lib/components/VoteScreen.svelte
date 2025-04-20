<script>
	import VoteButton from './VoteButton.svelte';
	let { onVoteGiven } = $props();
</script>

<p class="p-4 text-center text-lg">Do you support this law?</p>

<div class="button-container mx-0 my-auto flex flex-col items-center justify-center gap-2 p-4">
	<VoteButton buttonText="YES" {onVoteGiven} />
	<VoteButton buttonText="NO" {onVoteGiven} />
	<VoteButton buttonText="ABSTAIN" {onVoteGiven} />
</div>
