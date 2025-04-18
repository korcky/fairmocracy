<script>
    import { PUBLIC_BACKEND_URL } from "$env/static/public";
	import { setUserData } from "$lib/stores/userData.svelte.js";

let gameCode = $state('');
let error = $state('');
const { onSelect } = $props();

const onsubmit = (e) => {
    e.preventDefault();
    fetch(`${PUBLIC_BACKEND_URL}/join?game_hash=${gameCode}`).then((res) => {
        if (res.ok) {
            res.json().then(respJson => {setUserData({game: respJson})
            onSelect();
        })
        } else {
            error = "Game code submission failed: "+res.statusText;
        }
    }).catch((err) => {
        console.log(err)
        error = "Network error";
    });
}
</script>

<p class="p-4 text-center text-lg">Enter game code:</p>

<div class="form-container">
	<div class="fields">
		<div class="field">
			<input
				id="game-code"
				value={gameCode}
				oninput={(e) => (gameCode = e.target.value)}
				class="input variant-form-material"
				placeholder="Game code"
			/>
		</div>
        {#if error}
            <p class="mt-1 text-sm text-red-500">{error}</p>
        {/if}
	</div>
	<button onclick={ onsubmit } type="submit" class="variant-filled btn bg-blue-500">Enter</button>
</div>

<style>
	.form-container {
		max-width: 90%;
		margin: 0 auto;
		display: flex;
		flex-direction: column;
		gap: 1rem;
		align-items: center;
	}

	.fields {
		display: flex;
		justify-content: center;
		flex-direction: column;
		gap: 1rem;
	}

	.field {
		display: flex;
		flex-direction: column;
		flex: 1;
	}

	.btn {
		color: white;
		transition-property: all;
		transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
		transition-duration: 0.15s;
	}
</style>
