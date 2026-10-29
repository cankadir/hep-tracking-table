/**
 * Status vocabulary. The sheet leaves some cells blank; those are "NA".
 * Order drives the stacked bar and the badge styles.
 */
export const STATUSES = [
	{ name: 'Completed', className: 'completed', color: '#1a7f37' },
	{ name: 'In progress', className: 'in-progress', color: '#0969da' },
	{ name: 'Not started', className: 'not-started', color: '#8c959f' },
	{ name: 'Blocked', className: 'blocked', color: '#cf222e' },
	{ name: 'NA', className: 'na', color: '#d8dee4' }
];

export const statusName = (status) => status ?? 'NA';

export const statusClass = (status) =>
	STATUSES.find((s) => s.name === statusName(status))?.className ?? 'na';
