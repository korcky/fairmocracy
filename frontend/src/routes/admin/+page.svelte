<script lang="ts">
	import AdminLogin from '$lib/components/AdminLogin.svelte';
	import FileUpload from '$lib/components/FileUpload.svelte';
	import { currentUser } from '$lib/stores/userData.svelte.js';
</script>

{#if $currentUser.isAdmin}
	<FileUpload />
{:else}
	<AdminLogin />
{/if}
