<script>
	import { scaleLinear } from 'd3-scale';
	import { STATUSES, statusName } from '$lib/status';

	let { activities = [], label = 'Status mix' } = $props();

	const counts = $derived.by(() => {
		const c = Object.fromEntries(STATUSES.map((s) => [s.name, 0]));
		for (const activity of activities) {
			const name = statusName(activity.status);
			c[name] = (c[name] ?? 0) + 1;
		}
		return c;
	});

	const total = $derived(STATUSES.reduce((sum, s) => sum + counts[s.name], 0));

	const scale = $derived(scaleLinear([0, total || 1], [0, 100]));

	const segments = $derived.by(() => {
		let x = 0;
		const out = STATUSES.map((s) => {
			const count = counts[s.name];
			const width = scale(count);
			const segment = { name: s.name, className: s.className, color: s.color, count, x, width };
			x += width;
			return segment;
		});
		return out.filter((s) => s.count > 0);
	});

	const summary = $derived(segments.map((s) => `${s.count} ${s.name}`).join(', '));
</script>

<svg
	class="status-bar"
	viewBox="0 0 100 8"
	preserveAspectRatio="none"
	role="img"
	aria-label="{label}: {summary}"
>
	{#each segments as segment (segment.name)}
		<rect
			x={segment.x}
			y="0"
			width={segment.width}
			height="8"
			fill={segment.color}
		><title>{`${segment.count} ${segment.name}`}</title></rect>
	{/each}
</svg>

<style>
	.status-bar {
		display: block;
		width: 100%;
		height: 0.5rem;
	}
</style>
