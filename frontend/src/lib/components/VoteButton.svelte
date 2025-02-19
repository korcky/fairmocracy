<script>
	let props = $props();
	let bgColor = props.buttonText === 'YES' ? 'green' : props.buttonText === 'NO' ? 'red' : 'grey';
</script>

<button type="button" class="btn btn-xl text-5xl font-extrabold" style="background: {bgColor}">
	{props.buttonText}
</button>

<style>
	.btn {
		color: white;
		width: 80%;
		height: 8rem;
	}
</style>
