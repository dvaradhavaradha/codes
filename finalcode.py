from flask import Flask, request, jsonify
from github import Github
import json
import os

app = Flask(__name__)

@app.route('/push', methods=['POST'])
def push_to_repo():
    try:
        # Get the JSON data from the request
        data = request.get_json()

        # Check if the required variables are in the data
        required_vars = ['string1', 'string2', 'userlist']
        for var in required_vars:
            if var not in data:
                return jsonify({"error": f"{var} is required"}), 400

        # Get the variables from the data
        string1 = data['string1']
        string2 = data['string2']
        userlist = data['userlist']

        # Check if the local file exists
        if not os.path.isfile(string1):
            return jsonify({"error": f"{string1} does not exist"}), 400

        # Read the local file
        with open(string1, 'r') as file:
            file_content = file.read()

        # Create a Github instance:
        token = "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"
        g = Github(token)

        # Get the specific repo
        repo = g.get_user().get_repo("deploy")

        # commit message
        commit_message = "Create file via PyGithub"

        # Create the new .tf file in the repository
        new_tf_file = string2 + ".tf"
        repo.create_file(new_tf_file, commit_message, file_content)

        # Create the content for the .tfvars file
        tfvars_content = f'projectname = "{string2}"\nuserlist = {json.dumps(userlist)}'

        # Create the new .tfvars file in the repository
        new_tfvars_file = string2 + ".tfvars"
        repo.create_file(new_tfvars_file, commit_message, tfvars_content)

        return "Files created successfully", 200
    except Exception as e:
        return str(e), 400

if __name__ == "__main__":
    app.run(debug=True)



