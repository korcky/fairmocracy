<script>
	import '../app.css';
	import { initializeStores, Toast } from '@skeletonlabs/skeleton';
	import Navbar from '$lib/components/Navbar.svelte';
	let { children } = $props();
	initializeStores();
</script>

<!-- Navigation bar, containing our project on the left and menu on the right -->
<Navbar title="fairmocracy" />

<!-- This just renders basically all content that is given on +page.svelte for each route -->
{@render children()}

<!-- This is the toast that triggers on vote given, has to be on top level per docs -->
<Toast
	position="b"
	width="max-w-[500px] mx-auto"
	padding="p-4"
	rounded="rounded-md"
	shadow="shadow-md"
/>
