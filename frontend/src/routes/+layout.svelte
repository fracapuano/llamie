<script>
	import '../app.css';
	import MenuBar from '$lib/components/app-menubar.svelte';

	let { children } = $props();
</script>

<div class="flex w-full justify-center py-5">
	<MenuBar />
</div>

<main>
	{@render children?.()}
</main>
