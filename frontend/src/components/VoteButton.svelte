<script>
	let props = $props();

	let bgColor = props.buttonText === 'YES' ? 'green' : props.buttonText === 'NO' ? 'red' : 'grey';
</script>

<button class="btn" style="background: {bgColor}">
	{props.buttonText}
</button>

<style>
	.btn {
		color: white;
	}
</style>
