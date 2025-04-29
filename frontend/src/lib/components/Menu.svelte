<script>
	import { fly } from 'svelte/transition';
	import { Portal } from '@jsrob/svelte-portal';

	let showMenu = false;

	const toggleMenu = () => (showMenu = !showMenu);
	const closeMenu = () => (showMenu = false);

	function stopPropagation(event) {
		event.stopPropagation();
	}
</script>

<button type="button" class="rounded bg-blue-500 p-2 text-white" onclick={toggleMenu}>
	Menu
</button>

{#if showMenu}
	<!-- Render menu and backdrop outside navbar -->
	<Portal target="body">
		<!-- Backdrop when menu open -->
		<!-- svelte-ignore a11y_click_events_have_key_events -->
		<!-- svelte-ignore a11y_interactive_supports_focus -->
		<div
			class="fixed inset-0 z-40 h-screen w-screen bg-black bg-opacity-25"
			onclick={closeMenu}
			role="button"
		></div>

		<!-- Menu container -->
		<!-- svelte-ignore a11y_click_events_have_key_events -->
		<!-- svelte-ignore a11y_no_static_element_interactions -->
		<div
			class="fixed right-0 top-0 z-50 h-full w-64 bg-white shadow-lg"
			transition:fly={{ x: 300, duration: 300 }}
			onclick={stopPropagation}
		>
			<!-- Close menu button -->
			<button
				type="button"
				class="absolute right-2 top-2 p-2 text-gray-500 hover:text-gray-700"
				onclick={closeMenu}
			>
				<!-- Unicode X sign-->
				&#x2715;
			</button>

			<!-- Menu content -->
			<nav class="p-4">
				<ul>
					<li class="mb-2">
						<a href="/" class="text-gray-700 hover:text-blue-500">Home</a>
					</li>
					<li class="mb-2">
						<a href="/about" class="text-gray-700 hover:text-blue-500">About</a>
					</li>
					<li class="mb-2">
						<a href="/admin" class="text-gray-700 hover:text-blue-500">Admin</a>
					</li>
				</ul>
			</nav>
		</div>
	</Portal>
{/if}
