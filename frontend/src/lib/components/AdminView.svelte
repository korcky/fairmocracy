<script>
	import { currentUser } from '$lib/stores/userData.svelte.js';
	import { gameState } from '$lib/stores/gameData.svelte.js';
</script>

<p class="text-center text-xl font-bold">
	Game join code: {$currentUser.gameCode}
</p>

<!-- Admin Controls Template-->
<p class="my-4 text-center">Admin Controls Template</p>
<div class="mx-auto my-4 grid max-w-md grid-cols-2 gap-4">
	<button class="variant-filled btn rounded bg-blue-500 px-4 py-2 text-white">Button1</button>
	<button class="variant-filled btn rounded bg-blue-500 px-4 py-2 text-white">Button2</button>
	<button class="variant-filled btn rounded bg-blue-500 px-4 py-2 text-white">Button3</button>
	<button class="variant-filled btn rounded bg-blue-500 px-4 py-2 text-white">Button4</button>
	<button class="variant-filled btn rounded bg-blue-500 px-4 py-2 text-white">Button5</button>
	<button class="variant-filled btn rounded bg-blue-500 px-4 py-2 text-white">Button6</button>
</div>

<style>
	.btn {
		color: white;
		transition-property: all;
		transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
		transition-duration: 0.15s;
	}
</style>
