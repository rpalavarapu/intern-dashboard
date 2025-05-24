def categorize_tasks(all_tasks):
    categorized = {}

    for name, tasks in all_tasks.items():
        categorized[name] = {
            'yesterday': [],
            'today': [],
            'blockers': []
        }

        for task in tasks:
            if 'blocked' in task['labels'] or 'Blocker' in task['labels']:
                categorized[name]['blockers'].append(task)
            elif task['status'] == 'closed':
                categorized[name]['yesterday'].append(task)
            else:
                categorized[name]['today'].append(task)
    return categorized  