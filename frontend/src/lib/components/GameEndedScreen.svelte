<script>
	import UserAvatar from './UserAvatar.svelte';
	import { PUBLIC_BACKEND_URL } from '$env/static/public';
	import { currentUser } from '$lib/stores/userData.svelte.js';
	import { gameState } from '$lib/stores/gameData.svelte.js';

	let acceptedProposals = $state([]);
	let rejectedProposals = $state([]);
	let isMajorityWithReward = $state(false);

	const sys = $gameState.voting_system;
	const voterScore = $currentUser.extraInfo?.[sys]?.current_score ?? 0;
	const partyScore = $currentUser.partyExtraInfo?.[sys]?.current_score ?? 0;

	$effect(async () => {
		const roundId = $gameState.current_round_id;
		if (!roundId) return;

		try {
			const res = await fetch(`${PUBLIC_BACKEND_URL}/round/${roundId}/voting_events`);
			const events = await res.json();

			for (const ev of events) {
				if (ev.result === 'ACCEPTED') {
					acceptedProposals.push(ev.title);
				} else if (ev.result === 'REJECTED') {
					rejectedProposals.push(ev.title);
				}
				if (ev.extra_info?.MAJORITY_WITH_REWARD) {
					isMajorityWithReward = true;
				}
			}
		} catch (e) {
			console.error('Failed to load voting events', e);
		}
	});
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
	<ul class="list-disc">
		{#if acceptedProposals.length > 0}
			{#each acceptedProposals as proposal}
				<li>{proposal}</li>
			{/each}
		{:else}
			<li>No proposals were accepted.</li>
		{/if}
	</ul>
	<p>Proposals that were rejected:</p>
	<ul class="list-disc">
		{#if rejectedProposals.length > 0}
			{#each rejectedProposals as proposal}
				<li>{proposal}</li>
			{/each}
		{:else}
			<li>No proposals were rejected.</li>
		{/if}
	</ul>
</div>
