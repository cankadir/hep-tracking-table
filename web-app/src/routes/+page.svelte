<script>
	import Accordion from '$lib/components/Accordion.svelte';
	import StatusBar from '$lib/components/StatusBar.svelte';
	import { groupRows } from '$lib/group';
	import { statusClass, statusName } from '$lib/status';

	let { data } = $props();

	const goals = $derived(groupRows(data.rows));
</script>

<svelte:head><title>HEP Tracking Table</title></svelte:head>

<div class="page">
	<h1>HEP Tracking Table</h1>

	{#if goals.length === 0}
		<p>No data available.</p>
	{:else}
		{#each goals as goal (goal.goal)}
			<div class="goal">
				<Accordion title={goal.goal} level={2}>
					{#each goal.objectives as objective (`${objective.code}-${objective.desc}`)}
						<div class="objective">
							<Accordion
								code={objective.code}
								title={objective.desc}
								subtitle={objective.subtitle}
								level={3}
							>
								{#snippet extra()}
									<StatusBar activities={objective.actions.flatMap((action) => action.activities)} />
								{/snippet}
								{#each objective.actions as action (`${action.code}-${action.desc}`)}
									<article class="action">
										<h4><span class="code">{action.code}</span> {action.desc}</h4>

										<div class="table-wrap">
											<table>
												<thead>
													<tr>
														<th>Activity</th>
														<th>Status</th>
														<th>Lead Implementers</th>
													</tr>
												</thead>
												<tbody>
													{#each action.activities as activity, i (i)}
														<tr>
															<td>{activity.text}</td>
															<td>
																<span class="status {statusClass(activity.status)}">{statusName(activity.status)}</span>
															</td>
															<td>{activity.lead ?? '—'}</td>
														</tr>
													{/each}
												</tbody>
											</table>
										</div>
									</article>
								{/each}
							</Accordion>
						</div>
					{/each}
				</Accordion>
			</div>
		{/each}
	{/if}
</div>

<style>
	:global(html) {
		font-size: 100%;
	}

	:global(body) {
		margin: 0;
		font-family: system-ui, -apple-system, sans-serif;
		background: #f7f7f9;
		color: #1f2328;
	}

	.page {
		max-width: 72rem;
		margin: 0 auto;
		padding: 1.5rem;
	}

	h1 {
		margin: 0 0 1.5rem;
		font-size: 1.75rem;
	}

	.goal + .goal {
		margin-top: 0.75rem;
	}

	.objective + .objective {
		margin-top: 0.5rem;
	}

	.action h4 {
		margin: 1.25rem 0 0;
		font-size: 0.95rem;
	}

	.action:first-child h4 {
		margin-top: 0;
	}

	.code {
		font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
		font-size: 0.8rem;
		background: #eef1f4;
		border-radius: 0.25rem;
		padding: 0 0.35rem;
	}

	.table-wrap {
		overflow-x: auto;
	}

	table {
		width: 100%;
		margin-top: 0.5rem;
		border-collapse: collapse;
		font-size: 0.85rem;
	}

	th {
		background: #f6f8fa;
		padding: 0.5rem 0.75rem;
		text-align: left;
		vertical-align: top;
		font-weight: 600;
	}

	th:first-child {
		width: 60%;
	}

	td {
		padding: 0.5rem 0.75rem;
		vertical-align: top;
		border-top: 0.0625rem solid #eef1f4;
		overflow-wrap: anywhere;
	}

	.status {
		display: inline-block;
		padding: 0.125rem 0.5rem;
		border-radius: 0.75rem;
		font-size: 0.75rem;
		font-weight: 500;
	}

	.status.not-started {
		background: #eef1f4;
		color: #59636e;
	}

	.status.in-progress {
		background: #ddf4ff;
		color: #0969da;
	}

	.status.completed {
		background: #dafbe1;
		color: #1a7f37;
	}

	.status.blocked {
		background: #ffebe9;
		color: #cf222e;
	}

	.status.na {
		background: #f6f8fa;
		color: #8c959f;
	}

	@media (max-width: 40rem) {
		.page {
			padding: 1rem;
		}

		table {
			font-size: 0.8rem;
		}
	}
</style>
