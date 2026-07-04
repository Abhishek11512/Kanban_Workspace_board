async function loadBoardData() {
    const res = await fetch("/api/board");
    const data = await res.json()

    const onhold = document.getElementById('Onhold-lane').innerHTML = '<h3 style="color: #dc3545; border-bottom: 2px solid #dc3545; padding-bottom: 5px;">🛑 On-Hold</h3>';
    const ongoing = document.getElementById('Ongoing-lane').innerHTML = '<h3 style="color: #007bff; border-bottom: 2px solid #007bff; padding-bottom: 5px;">🏃 Ongoing</h3>';
    const completed = document.getElementById('Completed-lane').innerHTML = '<h3 style="color: #28a745; border-bottom: 2px solid #28a745; padding-bottom: 5px;">✅ Completed</h3>';

    data.github_projects.forEach((project) => {
        const card = document.createElement('div')
        card.className = "kanban-card";
        card.innerHTML = `<strong>📦 ${project.name}</strong><br><small style="color:gray;">GitHub Repository</small>`

        if (project.status === 'Completed') {
            document.getElementById('Completed-lane').appendChild(card);
        } else if (project.status === 'Onhold') {
            document.getElementById('Onhold-lane').appendChild(card);
        } else {
            document.getElementById('Ongoing-lane').appendChild(card);
        }
    });
}

loadBoardData();