<script lang="ts">
	import { PUBLIC_BACKEND_URL } from "$env/static/public";
	import { FileDropzone } from '@skeletonlabs/skeleton';
	import { goto } from '$app/navigation';

	let uploadedFiles: File[] = [];

	function handleFileChange(event: CustomEvent<File[]>) {
        const files = event.detail;
		if (files && files.length > 0) {
			const file = files[0];
			if (file.type === 'text/csv') {
				uploadedFiles = Array.from(files);
			} else {
				alert('Please upload a valid CSV file.');
			}
		}
	}

	async function startGame() {
		if (uploadedFiles.length > 0) {
			const formData = new FormData();
			formData.append('file', uploadedFiles[0]);

			try {
				const response = await fetch(`${PUBLIC_BACKEND_URL}/upload_config`, {
					method: 'POST',
					body: formData
				});

				if (response.ok) {
					const result = await response.json();
					console.log(result);
					goto('/register');
				} else {
					const errorText = await response.text();
					alert('Upload failed: ' + errorText);
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

	<FileDropzone
        name = "config"
		accept=".csv"
		maxFiles={1}
		on:change={handleFileChange}
		class="w-full mt-4"
	>
		<svelte:fragment slot="message">Select config file or drag here</svelte:fragment>
		<svelte:fragment slot="meta">Only .csv files allowed, Max: 1 files</svelte:fragment>
	</FileDropzone>

	<div class="mt-4 flex justify-center">
		<button
			on:click={startGame}
			class="bg-blue-500 text-white px-4 py-2 rounded"
		>
			Start Game
		</button>
	</div>
</div>
