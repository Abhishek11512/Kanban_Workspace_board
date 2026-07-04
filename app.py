import sqlite3
import requests 
from flask import Flask, render_template, request, jsonify 

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/api/board', methods=['POST'])
#local Sqlite3 database task to fetch data
def get_dynamic_board_data():
    con = sqlite3.connect('tasks.db')
    cr = con.cursor()
    cr.execute('''SELECT id, title, status FROM tasks''')
    all_board_data = cr.fetchall()
    con.close()
    local_task_list = [{"id": task[0], "title": task[1], "status": task[2]} for task in all_board_data]

    #Extracting username from the link provided
    request_data = request.get_json() or {}
    raw_link = request_data.get('github_link', '').strip()
    username = "Abhishek11512"

    if "github.com/" in raw_link:
        username = raw_link.split("github.com/")[-1].split("/")[0].strip()

#Fetching Github info here
    repo_url = f"https://api.github.com/users/{username}/repos"
    headers = {"User-Agent": "Kanban-App"}
    github_projects_list = []

    try:
        response = requests.get(repo_url, headers=headers)
        all_repos = response.json()

        if isinstance(all_repos, list):
            for repo in all_repos:
                repo_name = repo.get("name")

                is_fork = repo.get("fork", False)
                has_stars = repo.get("stargazers_count", 0) > 0

                if has_stars and not is_fork:
                    tracker_status = "Completed"
                elif is_fork: 
                    tracker_status = "Onhold"
                else:
                    tracker_status = "Ongoing"
    
                github_projects_list.append({
                    "name": repo_name.replace("_", " ").replace("-", " ").title(),
                    "status": tracker_status
                })
        else:
            print(f"API API Feedback Notice: {all_repos}")

    except Exception as e:
        print(f"❌ API Speed Sync Failure: {e}")
        github_projects_list = []

    master_payload = {
        "local_tasks": local_task_list,
        "github_projects": github_projects_list
    }
    return jsonify(master_payload)

if __name__=="__main__":
    app.run(debug=True)
