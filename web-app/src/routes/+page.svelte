<script>
	import { rows } from '$lib/store';

	let { data } = $props();

	$effect(() => {
		rows.set(data.rows);
	});

	const columns = ['Organization', 'Date', 'Sector', 'Explanation'];
</script>

<h1>HEP Tracking Table</h1>

{#if data.rows.length === 0}
	<p>No data available.</p>
{:else}
	<div class="table-wrap">
		<table>
			<thead>
				<tr>
				{#each columns as col (col)}
					<th>{col}</th>
				{/each}
				</tr>
			</thead>
			<tbody>
				{#each data.rows as row, i (row.Organization + i)}
					<tr>
						<td>{row.Organization}</td>
						<td>{row.Date}</td>
						<td>{row.Sector}</td>
						<td>{@html row.Explanation}</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
{/if}

<style>
	:global(body) {
		margin: 0;
		font-family: system-ui, -apple-system, sans-serif;
		background: #f7f7f9;
		color: #1f2328;
	}

	h1 {
		margin: 0 0 1rem;
		font-size: 1.5rem;
	}

	.table-wrap {
		overflow-x: auto;
		border: 1px solid #d8dee4;
		border-radius: 8px;
		background: #fff;
	}

	table {
		width: 100%;
		border-collapse: collapse;
		font-size: 0.9rem;
	}

	th,
	td {
		padding: 0.65rem 1rem;
		text-align: left;
		vertical-align: top;
		border-bottom: 1px solid #eef1f4;
	}

	th {
		background: #f6f8fa;
		font-weight: 600;
		white-space: nowrap;
	}

	tbody tr:last-child td {
		border-bottom: none;
	}

	tbody tr:hover {
		background: #f6f8fa;
	}
</style>
