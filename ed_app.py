from flask import Flask, request, jsonify
from flask_cors import CORS

from src.utils.helpers import execute_query, extract_questions, merge_questions

app = Flask(__name__)
CORS(app)


@app.route('/query-questions/<level>', methods=['POST'])
def query_questions(level):
    data = request.get_json()

    if not data or 'query' not in data:
        return jsonify({"success": False, "error": "Missing 'query' in request body."}), 400

    query = data['query']
    result = execute_query(query, level)

    if result['success']:
        questions = extract_questions(result['data'])
        return jsonify({"db_questions": questions}), 200
    else:
        return jsonify({"success": False, "error": result['error']}), 400


@app.route('/merge-question', methods=['POST'])
def merge_questions():
    data = request.get_json()

    if not data or 'gen_quest' not in data or 'db_quest' not in data:
        return jsonify({"success": False, "error": "Missing 'gen_quest' or 'db_quest' in request body."}), 400

    gen_quest = data['gen_quest']
    db_quest = data['db_quest']

    if 'questions' in gen_quest and 'open_ended' in gen_quest['questions']:
        gen_quest['questions']['open_ended'].extend(db_quest)
    else:
        return jsonify({"success": False, "error": "'gen_quest' does not have the correct structure."}), 400

    return jsonify({"success": True, "merged_questions": gen_quest}), 200


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
