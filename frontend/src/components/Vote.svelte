<script>
	import VoteButton from './VoteButton.svelte';
</script>

<div class="vote-container">
	<p>Vote buttons</p>
	<div class="button-container">
		<VoteButton buttonText="YES" />
		<VoteButton buttonText="NO" />
		<VoteButton buttonText="EMPTY" />
	</div>
</div>

<style>
	p {
		font-size: 1.5rem;
	}

	.vote-container {
		text-align: center;
	}

	.button-container {
		max-width: 50%;
		margin: 0 auto;
		display: flex;
		flex-direction: row;
		gap: 1rem;
		align-items: center;
		justify-content: center;
	}
</style>
