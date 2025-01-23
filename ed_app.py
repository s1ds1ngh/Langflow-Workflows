from flask import Flask, request, jsonify
from flask_cors import CORS

from src.utils.constants import save_quest_path
from src.utils.helpers import execute_query, extract_questions, merge_questions

app = Flask(__name__)
CORS(app)


@app.route('/query-questions/<level>', methods=['POST'])
def query_questions(level):
    """
    Endpoint to fetch and update question data based on the given level.
    """
    try:
        data = request.get_json() or {}
        questions_data = data.get('questions', {})
        open_ended = questions_data.get('open_ended', [])
        multiple_choice = questions_data.get('multiple_choice', [])

        predefined_query = "SELECT * FROM questions WHERE difficulty_level = %s"
        query_result = execute_query(predefined_query, (level,))

        if not query_result["success"]:
            return jsonify({"error": query_result["error"]}), 500

        if open_ended and "data" in query_result:
            open_ended.extend(extract_questions(query_result["data"]))

        return jsonify(data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/save-payload', methods=['POST'])
def save_payload():
    """
    Endpoint to save the received payload to a file.
    """
    try:
        data = request.get_json() or {}
        with open(save_quest_path, 'w') as f:
            import json
            json.dump(data, f, indent=4)

        return jsonify({"message": "Payload saved successfully.", "file_path": save_quest_path}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
