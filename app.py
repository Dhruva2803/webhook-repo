from flask import Flask, request, render_template, jsonify
from models import insert_event, get_latest_events

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.json
    event_type = request.headers.get('X-GitHub-Event')

    try:
        if event_type == 'push':
            author = payload['pusher']['name']
            to_branch = payload['ref'].split('/')[-1]
            timestamp = payload['head_commit']['timestamp']
            insert_event({
                "author": author,
                "action": "push",
                "from_branch": None,
                "to_branch": to_branch,
                "timestamp": timestamp
            })
        elif event_type == 'pull_request':
            author = payload['pull_request']['user']['login']
            from_branch = payload['pull_request']['head']['ref']
            to_branch = payload['pull_request']['base']['ref']
            timestamp = payload['pull_request']['updated_at']
            action = "merge" if payload['pull_request'].get('merged') else "pull_request"
            insert_event({
                "author": author,
                "action": action,
                "from_branch": from_branch,
                "to_branch": to_branch,
                "timestamp": timestamp
            })
    except Exception as e:
        print("Error:", e)

    return '', 204

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/events')
def events():
    return jsonify(get_latest_events())

if __name__ == '__main__':
    app.run(port=5000, debug=True)
