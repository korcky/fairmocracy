<script>
	import { goto } from '$app/navigation';
	import UserAvatar from './UserAvatar.svelte';
	import { onMount } from 'svelte';
	import { currentUser } from '$lib/stores/userData.svelte.js';
	import { gameState, parties} from '$lib/stores/gameData.svelte.js';

	let selectedParty = '';
	let user = $currentUser;
	let voterScore = user.extra_info?.MAJORITY_WITH_REWARD?.current_score ?? 0;
	let partyScore = 0;
	let RoundId = $gameState.current_round_id;
	let affiliationId = user.affiliations[RoundId];
	if (affiliationId.party_id && $parties.length > 0) {
			const party = $parties.find(p => p.id === affiliationId.party_id);
			partyScore = party.extra_info?.MAJORITY_WITH_REWARD?.current_score ?? 0;
			selectedParty = party.name ?? 'Unknown';
		}
	let isMajorityWithReward = false;
	let acceptedProposals = [];
	let rejectedProposals = [];

	onMount(async () => {
		if ($gameState.current_round_id) {
			const roundId = $gameState.current_round_id;
			fetch(`${PUBLIC_BACKEND_URL}/round/${roundId}/voting_events`)
				.then(res => res.json())
				.then(votingEvents => {
					for (const event of votingEvents) {
						if (event.result === 'ACCEPTED') {
							acceptedProposals.push(event.title);
						} else if (event.result === 'REJECTED') {
							rejectedProposals.push(event.title);
						}
						const extra = event.extra_info?.MAJORITY_WITH_REWARD;
						if (extra) {
							isMajorityWithReward = true;
						}
					}
					const totalQ = votingEvents.length;
					console.log("Voting events retrieved: ", totalQ);
				})
				.catch(e => console.error("Failed to load voting events", e));
			}
		}
	);
</script>

<div class="welcome-container mt-8 flex w-full flex-col items-center justify-center space-y-4">
	<UserAvatar userName={$currentUser.name} party={$currentUser.party} />

	<p>Game ended, thank you for taking part!</p>
	<!-- Display user's points if available -->
	{#if isMajorityWithReward}
		<p>Your points: {voterScore}</p>
		<p>Your party's points: {partyScore}</p>
  	{/if}

	<p>Proposals that were accepted:</p>
	<ul>
		{#if acceptedProposals.length > 0}
		  {#each acceptedProposals as proposal}
			<li>{proposal}</li>
		  {/each}
		{:else}
		  <li>No proposals were accepted.</li>
		{/if}
	  </ul>
	<p>Proposals that were rejected:</p>
	<ul>
		{#if rejectedProposals.length > 0}
		  {#each rejectedProposals as proposal}
			<li>{proposal}</li>
		  {/each}
		{:else}
		  <li>No proposals were rejected.</li>
		{/if}
	  </ul>
</div>
