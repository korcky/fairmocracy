<script lang="ts">
	import { PUBLIC_BACKEND_URL } from '$env/static/public';
	import { FileDropzone } from '@skeletonlabs/skeleton';
	import { goto } from '$app/navigation';
	import { setUserData } from '$lib/stores/userData.svelte.js';

	let uploadedFile: File | null = null;

	function handleFileChange(e: Event): void {
		const input = e.target as HTMLInputElement;
		const files = input?.files;
		const file = files?.[0];

		console.log('file:', file);

		if (file && file.name.toLowerCase().endsWith('.json')) {
			uploadedFile = file;
		} else {
			uploadedFile = null;
			alert('Please upload a valid JSON file.');
		}
	}
	async function startGame() {
		if (uploadedFile) {
			const formData = new FormData();
			formData.append('file', uploadedFile);

			try {
				const response = await fetch(`${PUBLIC_BACKEND_URL}/upload_config`, {
					method: 'POST',
					body: formData
				});

				if (response.ok) {
					const result = await response.json();
					console.log(result);
					setUserData({
						gameId: result.game_id,
						gameCode: result.game_code,
						userId: null,
						affiliations: {},
						votes: {}
					});
					alert(
						`Game created successfully!\nGame Code: ${result.game_code}\nGame ID: ${result.game_id}\nGame Name: ${result.game_name}\nNum Rounds: ${result.num}`
					);
					goto('/');
				} else {
					let errMsg = 'Unknown error';
					try {
						const payload = await response.json();
						errMsg = payload.error || payload.detail || JSON.stringify(payload);
					} catch (_) {
						// fallback to raw text
						errMsg = await response.text();
						console.error(errMsg);
					}
					alert(`Upload failed:\n${errMsg}`);
				}
			} catch (err) {
				console.error(err);
				alert('Error uploading file');
			}
		} else {
			alert('Please upload a file first.');
		}
	}
</script>

<div class="p-4">
	<h1 class="p-4 text-center text-lg">Upload File to Start Game</h1>

	<!-- Dropzone container with max width and styled to blend in -->
	<div class="mx-auto max-w-md rounded border-2 border-dashed border-gray-300 bg-transparent p-4">
		<FileDropzone
			name="config"
			accept=".json"
			maxFiles={1}
			on:change={handleFileChange}
			class="w-full bg-transparent"
		>
			<svelte:fragment slot="message">
				{#if uploadedFile}
					{uploadedFile.name}
				{:else}
					Select config file or drag here
				{/if}
			</svelte:fragment>
			<svelte:fragment slot="meta">Only .json files allowed, Max: 1 files</svelte:fragment>
		</FileDropzone>
	</div>

	<!-- Start button -->
	<div class="mt-4 flex justify-center">
		<button onclick={startGame} class="variant-filled btn rounded bg-blue-500 px-4 py-2 text-white">
			Start Game
		</button>
	</div>
</div>

<style>
	.btn {
		color: white;
		transition-property: all;
		transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
		transition-duration: 0.15s;
	}
</style>
