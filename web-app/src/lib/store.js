import { writable } from 'svelte/store';

export const DATA_URL =
	'https://raw.githubusercontent.com/cankadir/hep-tracking-table/refs/heads/main/data/hep-tracking.json';

export const rows = writable([]);
