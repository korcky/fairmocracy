<div class="form-container">
	<div class="fields">
		<div class="field">
			<label for="name">Name</label>
			<input id="name" class="input variant-form-material" placeholder="Enter your name" />
		</div>
		<div class="field">
			<label for="party">Party</label>
			<select id="party" class="select variant-form-material">
				<option value="red">Red</option>
				<option value="blue">Blue</option>
			</select>
		</div>
	</div>
	<button class="enter-btn">Enter</button>
</div>

<style>
	.form-container {
		max-width: 50%;
		margin: 0 auto;
		display: flex;
		flex-direction: column;
		gap: 1rem;
		align-items: center;
	}

	.fields {
		display: flex;
		justify-content: center;
		align-items: flex-start;
		gap: 1rem;
		width: 100%;
	}

	.field {
		display: flex;
		flex-direction: column;
		flex: 1;
	}

	.field label {
		margin-bottom: 0.5rem;
		font-weight: bold;
	}

	.enter-btn {
		padding: 0.5rem 1rem;
		font-size: 1rem;
		border: none;
		border-radius: 4px;
		cursor: pointer;
		background-color: #317efb;
		color: white;
		transition: background-color 0.2s ease;
	}

	.enter-btn:hover {
		background-color: #2565c0;
	}
</style>
