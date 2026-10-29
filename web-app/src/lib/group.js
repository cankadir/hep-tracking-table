/**
 * Flat rows -> Goal > Objective > Action > activities.
 *
 * The group keys use code *and* text, so two groups that happen to share a
 * code but describe different things never merge. Map preserves the sheet
 * order, so no sorting pass is needed.
 */

const groupBy = (items, keyOf) => {
	const groups = new Map();
	for (const item of items) {
		const key = keyOf(item);
		const group = groups.get(key);
		if (group) group.push(item);
		else groups.set(key, [item]);
	}
	return [...groups.values()];
};

const objectiveKey = (row) =>
	JSON.stringify([row['Objective Code'], row['Objective Desc'], row.Subtitle]);

const actionKey = (row) => JSON.stringify([row['Action Code'], row['Action Desc']]);

export function groupRows(rows) {
	return groupBy(rows, (row) => row.Goal).map((goalRows) => ({
		goal: goalRows[0].Goal,
		objectives: groupBy(goalRows, objectiveKey).map((objectiveRows) => ({
			code: objectiveRows[0]['Objective Code'],
			desc: objectiveRows[0]['Objective Desc'],
			subtitle: objectiveRows[0].Subtitle,
			actions: groupBy(objectiveRows, actionKey).map((actionRows) => ({
				code: actionRows[0]['Action Code'],
				desc: actionRows[0]['Action Desc'],
				activities: actionRows.map((row) => ({
					text: row['Activities-Deliverables'],
					status: row.Status,
					lead: row['Lead Implementers']
				}))
			}))
		}))
	}));
}
