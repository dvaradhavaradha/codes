from flask import Flask, request, jsonify
from github import Github
import json

app = Flask(__name__)

@app.route('/push', methods=['POST'])
def push_to_repo():
    try:
        # get the JSON data from the request
        data = request.get_json()

        # Convert the data back to a JSON string
        file_content = json.dumps(data)

        # Create a Github instance:
        token = "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"
        g = Github(token)

        # Get the specific repo
        repo = g.get_user().get_repo("deploy")

        # commit message
        commit_message = "Create file via PyGithub"

        # path to the file
        file_path = "new_file.json"

        # Create a new file in the repository
        repo.create_file(file_path, commit_message, file_content)

        return "File created successfully", 200
    except Exception as e:
        return str(e), 400

if __name__ == "__main__":
    app.run(debug=True)

