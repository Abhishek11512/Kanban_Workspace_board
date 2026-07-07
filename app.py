import sqlite3
import requests 
from flask import Flask, render_template, request, jsonify 

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/explorer')
def explorer_page():
    return render_template('explorer.html')

@app.route('/api/local_tasks', methods=['GET'])
def get_local_tasks():
    con = sqlite3.connect('tasks.db')
    cr = con.cursor()
    cr.execute('''SELECT id, title, status FROM tasks''')
    all_board_data = cr.fetchall()
    con.close()
    local_task_list = [{"id": task[0], "title": task[1], "status": task[2]} for task in all_board_data]
    return jsonify({"local_tasks": local_task_list})

@app.route('/api/github_scan', methods=['POST'])
def get_dynamic_github_data():
    request_data = request.get_json() or {}
    raw_link = request_data.get('github_link', '').strip()
    
    username = ""

    if "github.com/" in raw_link:
        username = raw_link.split("github.com/")[-1].split("/")[0].strip()

    repo_url = f"https://api.github.com/users/{username}/repos"

    headers = {
        "User-Agent": "Kanban-App",
        "Accept": "application/vnd.github.mercy-preview+json"
    }
    github_projects_list = []

    try:
        response = requests.get(repo_url, headers=headers)
        all_repos = response.json()

        if isinstance(all_repos, list):
            for repo in all_repos:
                repo_name = repo.get("name")

                topics_list =repo.get("topics", [])

                topics_list = [t.lower() for t in topics_list]

                if "completed" in topics_list:
                    tracker_status = "Completed"
                elif "on-hold" in topics_list or "onhold" in topics_list:
                    tracker_status = "Onhold"
                elif "ongoing" in topics_list:
                    tracker_status = "Ongoing"
                else:
                    is_fork = repo.get("fork", False)
                    if is_fork:
                        tracker_status = "Onhold"
                    else:
                        tracker_status = "Ongoing"
    
                github_projects_list.append({
                    "name": repo_name.replace("_", " ").replace("-", " ").title(),
                    "status": tracker_status
                })
        else:
            print(f"GitHub Server API Notice: {all_repos}")

    except Exception as e:
        print(f"❌ API Speed Sync Failure: {e}")
        github_projects_list = []

    return jsonify({"github_projects": github_projects_list})

@app.route('/api/add_task', methods=['POST'])
def add_task():
    request_data = request.get_json() or {}
    title = request_data.get('title', '').strip()
    
    if not title:
        return jsonify({"error": "No title provided"}), 400
        
    con = sqlite3.connect('tasks.db')
    cr = con.cursor()
    cr.execute("INSERT INTO tasks (title, status) VALUES (?, 'Ongoing')", (title,))
    con.commit()
    con.close()
    return jsonify({"success": True})

if __name__=="__main__":
    app.run(debug=True)
