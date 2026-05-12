from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

students = [
    {"id": 1, "name": "Alice", "grade": "A"},
    {"id": 2, "name": "Bob",   "grade": "B"},
]
next_id = 3

@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "message": "Flask is running"}), 200

@app.route("/api/students", methods=["GET"])
def get_students():
    return jsonify(students), 200

@app.route("/api/students/<int:sid>", methods=["GET"])
def get_student(sid):
    s = next((s for s in students if s["id"] == sid), None)
    return (jsonify(s), 200) if s else (jsonify({"error": "Not found"}), 404)

@app.route("/api/students", methods=["POST"])
def add_student():
    global next_id
    data = request.get_json()
    if not data or "name" not in data or "grade" not in data:
        return jsonify({"error": "name and grade required"}), 400
    new = {"id": next_id, "name": data["name"], "grade": data["grade"]}
    students.append(new)
    next_id += 1
    return jsonify(new), 201

@app.route("/api/students/<int:sid>", methods=["DELETE"])
def delete_student(sid):
    global students
    before = len(students)
    students = [s for s in students if s["id"] != sid]
    if len(students) == before:
        return jsonify({"error": "Not found"}), 404
    return jsonify({"message": "Deleted"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
