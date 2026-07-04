async function loadLocalBoard() {
    const res = await fetch("/api/local_tasks");
    const data = await res.json();

    document.getElementById('Onhold-lane').innerHTML = '<h3 style="color: #dc3545; border-bottom: 2px solid #dc3545; padding-bottom: 5px;">🛑 On-Hold</h3>';
    document.getElementById('Ongoing-lane').innerHTML = '<h3 style="color: #007bff; border-bottom: 2px solid #007bff; padding-bottom: 5px;">🏃 Ongoing</h3>';
    document.getElementById('Completed-lane').innerHTML = '<h3 style="color: #28a745; border-bottom: 2px solid #28a745; padding-bottom: 5px;">✅ Completed</h3>';

    data.local_tasks.forEach((task) => {
        const card = document.createElement('div');
        card.className = "kanban-card local-task-card";
        card.innerHTML = `<strong>📝 ${task.title}</strong><br><span class="badge-local">Local Offline Task</span>`;

        if (task.status === 'Completed') {
            document.getElementById('Completed-lane').appendChild(card);
        } else if (task.status === 'Onhold') {
            document.getElementById('Onhold-lane').appendChild(card);
        } else {
            document.getElementById('Ongoing-lane').appendChild(card);
        }
    });
}

async function AddTaskToBackend() {
    const taskValue = document.getElementById('taskField').value.trim();
    if (!taskValue) return alert("Please type a task title first!");

    const res = await fetch('/api/add_task', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: taskValue })
    });

    if (res.ok) {
        document.getElementById('taskField').value = '';
        loadLocalBoard();
    } else {
        alert("Failed to save local database task row.");
    }
}

loadLocalBoard();
