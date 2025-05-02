<script>
    import VoteButton from './VoteButton.svelte';
    import { gameState } from '$lib/stores/gameData.svelte.js'; // Import the store
</script>

<div class="voting-info p-4">
    <h2 class="text-xl font-bold">Current Voting Issue</h2>
    <p class="text-lg font-semibold">{$gameState.current_voting_event.title}</p>
    <p class="text-md">{$gameState.current_voting_event.content}</p>
	<p class="p-4 text-center text-lg">Do you support this law?</p>

    <h3 class="text-lg font-bold mt-4">Votes Given</h3>
    <ul>
        {#each $gameState.current_voting_event.votes as vote}
            <li>Voter ID: {vote.voter_id}, Vote: {vote.value}</li>
        {/each}
    </ul>

    <h2 class="text-xl font-bold mt-8">Next Voting Issue</h2>
    <p class="text-lg font-semibold">{$gameState.next_voting_event.title}</p>
    <p class="text-md">{$gameState.next_voting_event.content}</p>
</div>
<p class="p-4 text-center text-lg">Do you support this law?</p>

<div class="button-container mx-0 my-auto flex flex-col items-center justify-center gap-2 p-4">
	<VoteButton buttonText="YES" />
	<VoteButton buttonText="NO" />
	<VoteButton buttonText="ABSTAIN" />
</div>
