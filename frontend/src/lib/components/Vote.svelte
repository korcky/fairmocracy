<script>
	import VoteButton from './VoteButton.svelte';
</script>

<p class="p-4 text-center text-lg">Do you support this law?</p>

<div class="button-container">
	<VoteButton buttonText="YES" />
	<VoteButton buttonText="NO" />
	<VoteButton buttonText="EMPTY" />
</div>

<style>
	.button-container {
		padding: 1rem;
		margin: 0 auto;
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
		align-items: center;
		justify-content: center;
	}
</style>
