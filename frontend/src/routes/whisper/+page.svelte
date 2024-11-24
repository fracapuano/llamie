<script lang="ts">
	import WhisperTransformers from '$lib/components/app-whisper-transformers.svelte';
	import { fade } from 'svelte/transition';
	import { onMount } from 'svelte';

	// declare loaded boolean variable
	let loaded = false;

	onMount(() => {
		// set loaded to true
		loaded = true;
	});
</script>

{#if loaded}
	<main in:fade={{ duration: 400, delay: 100 }} class="md:px-30 mx-auto mt-10 px-6">
		<div class="mx-auto flex flex-col items-center justify-stretch px-4">
			<h1
				class="font-display anim-gradient bg-secondary bg-clip-text pb-3 text-center text-4xl font-bold group-hover:text-transparent md:text-5xl"
			>
				LLami
			</h1>
		</div>

		<div class="justify mx-auto mt-20 flex flex-col items-center">
			<WhisperTransformers />
		</div>
	</main>
{/if}
