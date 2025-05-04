<script>
	import VoteButton from './VoteButton.svelte';
	import { currentUser } from '$lib/stores/userData.svelte.js';
	import { gameState } from '$lib/stores/gameData.svelte.js';
	import { get } from 'svelte/store';

	// info toggle
	let showInfo = false;
	function toggleInfo() {
		showInfo = !showInfo;
	}

	// info to show from stores
	const currentQuestion = get(gameState).current_voting_question;
	const userRewards = get(currentUser).eventRewards || { accepted: 0, rejected: 0 };
	const partyRewards = get(currentUser).partyEventRewards || { accepted: 0, rejected: 0 };
</script>

<!-- Overlay: only when showInfo is true -->
{#if showInfo}
	<div
		class="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
		role="button"
		tabindex="0"
		aria-label="Close details overlay"
		on:click={toggleInfo}
		on:keydown={(e) => (e.key === 'Enter' || e.key === ' ') && toggleInfo()}
	>
		<!-- svelte-ignore a11y_click_events_have_key_events -->
		<!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
		<div
			class="preset-filled-surface-100-900 border-surface-200-800 divide-surface-200-800 card w-full max-w-md divide-y overflow-hidden border"
			role="dialog"
			aria-modal="true"
			tabindex="-1"
			on:click|stopPropagation
		>
			<header class="flex items-center justify-between border-b p-4">
				<h2 class="h6 m-0">Proposal Details</h2>
				<button
					type="button"
					class="p-2 text-2xl text-gray-500 hover:text-gray-700"
					aria-label="Close details"
					on:click={toggleInfo}
				>
					&#x2715;
				</button>
			</header>
			<article class="space-y-4 p-4 pt-4">
				<p class="whitespace-pre-wrap">{currentQuestion}</p>
				<div class="mt-4 space-y-2">
					<p class="font-semibold">If proposal is accepted:</p>
					<ul class="ml-6 list-disc">
						<li>You: {userRewards.accepted} points</li>
						<li>Your party: {partyRewards.accepted} points</li>
					</ul>
					<p class="mt-2 font-semibold">If proposal is rejected:</p>
					<ul class="ml-6 list-disc">
						<li>You: {userRewards.rejected} points</li>
						<li>Your party: {partyRewards.rejected} points</li>
					</ul>
				</div>
			</article>
		</div>
	</div>
{/if}

<!-- Main vote elements -->
<div class="p-4 text-center">
	<p class="mb-6 text-lg">Do you support the proposal?</p>

	<!-- show/hide info button -->
	<button type="button" class="variant-filled btn mb-4 bg-blue-500" on:click={toggleInfo}>
		View Info
	</button>

	<div class="button-container mx-0 my-auto flex flex-col items-center justify-center gap-2">
		<VoteButton buttonText="YES" />
		<VoteButton buttonText="NO" />
		<VoteButton buttonText="ABSTAIN" />
	</div>
</div>
