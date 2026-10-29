<script>
	import { slide } from 'svelte/transition';
	import accordionOpen from '$lib/assets/accordion-open.svg';

	let {
		title,
		code = null,
		subtitle = null,
		level = 2,
		open = $bindable(false),
		extra = null,
		children
	} = $props();
</script>

<svelte:element this={`h${level}`} class="heading">
	<button
		class="header"
		class:open
		class:large={level === 2}
		aria-expanded={open}
		onclick={() => (open = !open)}
	>
		<span class="label">
			<span class="line">
				{#if code}<span class="code">{code}</span>{/if}
				<span class="title">{title}</span>
			</span>
			{#if subtitle}<span class="subtitle">{subtitle}</span>{/if}
		</span>
		{#if extra}
			<span class="extra">{@render extra()}</span>
		{/if}
		<img class="icon" class:open src={accordionOpen} alt="" aria-hidden="true" />
	</button>
</svelte:element>

{#if open}
	<div class="body" transition:slide={{ duration: 200 }}>
		{@render children()}
	</div>
{/if}

<style>
	.heading {
		margin: 0;
	}

	.header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 1rem;
		width: 100%;
		padding: 0.625rem 0.875rem;
		background: #fff;
		border: 0.0625rem solid #000;
		font: inherit;
		font-size: 1.05rem;
		font-weight: 600;
		color: #080808;
		text-align: left;
		cursor: pointer;
		transition: background-color 150ms ease;
	}

	.header.large {
		font-size: 1.25rem;
	}

	.header:hover {
		background: #efefe9;
	}

	.header.open {
		background: #d6d6ce;
	}

	.label {
		display: flex;
		flex: 1;
		flex-direction: column;
		gap: 0.15rem;
		min-width: 0;
	}

	.extra {
		flex-shrink: 0;
		width: 10rem;
	}

	.line {
		display: flex;
		align-items: baseline;
		flex-wrap: wrap;
		gap: 0.5rem;
	}

	.code {
		font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
		font-size: 0.8rem;
		font-weight: 500;
		background: #eef1f4;
		border-radius: 0.25rem;
		padding: 0 0.35rem;
	}

	.subtitle {
		font-size: 0.85rem;
		font-weight: 400;
		color: #59636e;
	}

	.icon {
		width: 1.3125rem;
		height: 1.3125rem;
		flex-shrink: 0;
		transition: transform 150ms ease;
	}

	.icon.open {
		transform: rotate(45deg);
	}

	.body {
		padding: 0.75rem 0.875rem 1rem 1.25rem;
		border: 0.0625rem solid #000;
		border-top: none;
		background: #fff;
	}

	@media (prefers-reduced-motion: reduce) {
		.icon {
			transition: none;
		}
	}

	@media (max-width: 40rem) {
		.header {
			font-size: 1rem;
		}

		.body {
			padding-left: 0.875rem;
		}

		.extra {
			display: none;
		}
	}
</style>
