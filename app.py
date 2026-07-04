import sqlite3
import requests 
from flask import Flask, render_template, request, jsonify 

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/api/board', methods=['GET'])
#local Sqlite3 database task
def get_board_data():
    con = sqlite3.connect('tasks.db')
    cr = con.cursor()
    cr.execute('''SELECT id, title, status FROM tasks''')
    all_board_data = cr.fetchall()
    con.close()

    local_task_list = [{"id": task[0], "title": task[1], "status": task[2]} for task in all_board_data]

#Fetching Github info here
    repo_url = "https://github.com"
    headers = {"User-Agent": "Kanban-App"}

    github_projects_list = []

    try:
        response = requests.get(repo_url, headers=headers)
        all_repos = response.json()

        for repo in all_repos:
            repo_name = repo.get("name")

            topics_url = f"https://github.com{repo_name}/topics"
            topics_res = requests.get(topics_url, headers=headers)
            topics_list = topics_res.json().get('names', [])

            if "completed" in topics_list:
                tracker_status = "Completed"
            elif "onhold" in topics_list: 
                tracker_status = "Onhold"
            else:
                tracker_status = "Ongoing"
    
            github_projects_list.append({
                "name": repo_name.replace("_", " ").title(),
                "status": tracker_status
            })
    except Exception as e:
        print("\n❌ CRITICAL API FAILURE CLUE:", e, "\n")
        github_projects_list = []

    master_payload = {
        "local_tasks": local_task_list,
        "github_projects": github_projects_list
    }
    return jsonify(master_payload)

if __name__=="__main__":
    app.run(debug=True)
