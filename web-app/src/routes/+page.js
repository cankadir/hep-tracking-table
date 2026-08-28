import { error } from '@sveltejs/kit';
import { DATA_URL } from '$lib/store';

export async function load({ fetch }) {
	const res = await fetch(DATA_URL);
	if (!res.ok) throw error(res.status, 'Failed to load tracking data');
	return { rows: await res.json() };
}
