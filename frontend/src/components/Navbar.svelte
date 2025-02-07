<script>
	let props = $props();
</script>

<nav class="navbar">
	<div class="container">
		<a href="/" class="logo">{props.title}</a>

		<ul class="nav-links">
			<li><a href="/about">About</a></li>
		</ul>
	</div>
</nav>

<style>
	.navbar {
		background-color: #317efb;
		color: #fff;
		padding: 1rem;
	}

	.container {
		display: flex;
		justify-content: space-between;
		align-items: center;
		max-width: 100%;
		margin: 0 auto;
	}

	.logo {
		font-size: 2rem;
	}
</style>
