import { defineConfig } from 'vitest/config';
import { sveltekit } from '@sveltejs/kit/vite';

export default defineConfig({
	plugins: [sveltekit()],

	test: {
		include: ['src/**/*.{test,spec}.{js,ts}']
	},

	ssr: {
		noExternal: ['@skeletonlabs/skeleton']
	},

	preview: {
		host: '0.0.0.0',
		port: Number(process.env.PORT) || 10000,
		allowedHosts: ['fairmocracy.onrender.com']
	}
});
