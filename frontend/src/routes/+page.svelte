<main class="container mx-auto px-6 py-16">
	<h1
		class="font-display anim-gradient bg-secondary bg-clip-text pb-3 text-center text-5xl font-extrabold text-transparent md:text-6xl"
	>
		LLami
	</h1>

	<p class="mx-auto mt-6 max-w-3xl text-center text-lg font-medium text-gray-600">
		A simple robot arm powered from your phone, computer, or Jetson Nano.
	</p>
	<p class="mx-auto mt-6 max-w-3xl text-center text-lg font-medium text-gray-800">
		Multi Device compatibility!
	</p>

	<div class="mx-auto mt-12 grid max-w-screen-md grid-cols-1 gap-8 md:grid-cols-3">
		<div class="rounded-lg border border-gray-200 bg-white p-6 shadow-md hover:shadow-lg">
			<h3 class="mb-4 text-xl font-semibold text-gray-800">Phone</h3>
			<p class="text-gray-600">Control LLami using a user-friendly interface on your smartphone.</p>
		</div>

		<div class="rounded-lg border border-gray-200 bg-white p-6 shadow-md hover:shadow-lg">
			<h3 class="mb-4 text-xl font-semibold text-gray-800">Computer</h3>
			<p class="text-gray-600">
				Easily connect and manage your robot arm from your laptop or desktop.
			</p>
		</div>

		<div class="rounded-lg border border-gray-200 bg-white p-6 shadow-md hover:shadow-lg">
			<h3 class="mb-4 text-xl font-semibold text-gray-800">Jetson Nano</h3>
			<p class="text-gray-600">
				Harness the power of AI and robotics using the Jetson Nano platform. Less than $200!
			</p>
		</div>
	</div>

	<footer class="mt-20 border-t border-gray-200 pt-8 text-center">
		<p class="text-sm text-gray-500">
			Created with ❤️ by LLami enthusiasts (check out the team tab). Powering the future of
			robotics. Thanks to hugging face for lending the arm 🤗
		</p>
	</footer>
</main>

<style>
	.anim-gradient {
		background-image: linear-gradient(90deg, #4e54c8, #8f94fb, #4e54c8);
		animation: gradient-move 6s infinite linear;
		background-size: 200% 200%;
	}

	@keyframes gradient-move {
		0% {
			background-position: 0% 50%;
		}
		50% {
			background-position: 100% 50%;
		}
		100% {
			background-position: 0% 50%;
		}
	}
</style>
