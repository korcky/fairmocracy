<script>
	import '../app.css';
	import Navbar from '$lib/components/Navbar.svelte';
	let { children } = $props();
</script>

<Navbar title="fairmocracy" />

{@render children()}
