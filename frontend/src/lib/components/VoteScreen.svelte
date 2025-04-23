<script>
    import VoteButton from './VoteButton.svelte';
    import { gameState } from '$lib/stores/gameData.svelte.js';
    let { onVoteGiven } = $props();
</script>

{#if $gameState.voting_event}
    <div class="voting-info p-4">
        <h2 class="text-xl font-bold">Voting Issue</h2>
        <p class="text-lg font-semibold">{$gameState.voting_event.title}</p>
        <p class="text-md">{$gameState.voting_event.content}</p>

        <h3 class="text-lg font-bold mt-4">Extra Information</h3>
        <p class="text-md">{$gameState.voting_event.extra_info}</p>

        <h3 class="text-lg font-bold mt-4">Already Given Votes</h3>
        <ul>
            {#each $gameState.voting_event.votes as vote}
                <li>Voter ID: {vote.voter_id}, Vote: {vote.value}</li>
            {/each}
        </ul>
    </div>

    <div class="button-container mx-0 my-auto flex flex-col items-center justify-center gap-2 p-4">
        <VoteButton buttonText="YES" {onVoteGiven} />
        <VoteButton buttonText="NO" {onVoteGiven} />
        <VoteButton buttonText="ABSTAIN" {onVoteGiven} />
    </div>
{:else}
    <p>Loading voting event...</p>
{/if}
