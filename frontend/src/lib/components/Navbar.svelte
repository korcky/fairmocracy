<script>
	import { AppBar } from '@skeletonlabs/skeleton';
	import Menu from './Menu.svelte';

	let { title = 'fairmocracy' } = $props();
</script>

<AppBar gridColumns="grid-cols-3" slotDefault="place-self-center" slotTrail="place-content-end">
	<svelte:fragment slot="lead">
		<a href="/" class="text-3xl font-bold text-blue-600">{title}</a>
	</svelte:fragment>
	<svelte:fragment slot="trail">
		<Menu />
	</svelte:fragment>
</AppBar>
