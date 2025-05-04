<script>
	import { goto } from '$app/navigation';
	import UserAvatar from './UserAvatar.svelte';
	import { onMount } from 'svelte';
	import { currentUser } from '$lib/stores/userData.svelte.js';

	let votingResults = null;
	let isMajorityWithReward = false;

	onMount(async () => {
		// Fetch the voting results from the API
		const response = await fetch(`/api/voting_event/${votingEventId}/conclude`);
		if (response.ok) {
		votingResults = await response.json();
		isMajorityWithReward = votingResults.voter_rewards !== undefined; // Check if it's MajorityWithRewardSystem
		}
	});
</script>

<div class="welcome-container mt-8 flex w-full flex-col items-center justify-center space-y-4">
	<UserAvatar userName={$currentUser.name} party={$currentUser.party} />

	<p>Game ended, thank you for taking part!</p>
	<!-- Display user's points if available -->
	{#if isMajorityWithReward}
		<p>Your reward points: {votingResults.voter_rewards[$currentUser.id] || 0}</p>
		<p>Your party's reward points: {votingResults.party_rewards[$currentUser.party] || 0}</p>
  	{/if}

	<p>Proposals that were accepted:</p>
	<ul>
		{#if votingResults && votingResults.accepted_proposals.length > 0}
		  {#each votingResults.accepted_proposals as proposal}
			<li>{proposal}</li>
		  {/each}
		{:else}
		  <li>No proposals were accepted.</li>
		{/if}
	  </ul>
	<p>Proposals that were rehjected:</p>
	<ul>
		{#if votingResults && votingResults.rejected_proposals.length > 0}
		  {#each votingResults.rejected_proposals as proposal}
			<li>{proposal}</li>
		  {/each}
		{:else}
		  <li>No proposals were rejected.</li>
		{/if}
	  </ul>

	<!-- maybe show results here… -->
</div>
