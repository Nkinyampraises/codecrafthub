from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Path to the JSON file
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'courses.json')

# ─── Helper Functions ───────────────────────────────────────

def load_courses():
    """Load courses from JSON file"""
    if not os.path.exists(DATA_FILE):
        save_courses([])
        return []
    try:
        with open(DATA_FILE, 'r') as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

def save_courses(courses):
    """Save courses to JSON file"""
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(courses, f, indent=2)
    except Exception as e:
        print(f"Error saving file: {e}")

VALID_STATUSES = ["Not Started", "In Progress", "Completed"]

# ─── Routes ─────────────────────────────────────────────────

@app.route('/api/courses', methods=['POST'])
def create_course():
    """Create a new course"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Validate required fields
    required = ['name', 'description', 'target_date', 'status']
    for field in required:
        if field not in data or not data[field]:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    # Validate status
    if data['status'] not in VALID_STATUSES:
        return jsonify({
            "error": f"Invalid status. Must be one of: {VALID_STATUSES}"
        }), 400

    # Validate date format
    try:
        datetime.strptime(data['target_date'], '%Y-%m-%d')
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    courses = load_courses()

    # Auto-generate ID
    new_id = max([c['id'] for c in courses], default=0) + 1

    new_course = {
        "id": new_id,
        "name": data['name'],
        "description": data['description'],
        "target_date": data['target_date'],
        "status": data['status'],
        "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    courses.append(new_course)
    save_courses(courses)

    return jsonify({
        "message": "Course created successfully",
        "course": new_course
    }), 201


@app.route('/api/courses', methods=['GET'])
def get_all_courses():
    """Get all courses"""
    courses = load_courses()
    return jsonify({
        "message": "Courses retrieved successfully",
        "count": len(courses),
        "courses": courses
    }), 200


@app.route('/api/courses/<int:course_id>', methods=['GET'])
def get_course(course_id):
    """Get a single course by ID"""
    courses = load_courses()
    course = next((c for c in courses if c['id'] == course_id), None)
    if not course:
        return jsonify({"error": f"Course with ID {course_id} not found"}), 404
    return jsonify({
        "message": "Course retrieved successfully",
        "course": course
    }), 200


@app.route('/api/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    """Update a course by ID"""
    courses = load_courses()
    course = next((c for c in courses if c['id'] == course_id), None)
    if not course:
        return jsonify({"error": f"Course with ID {course_id} not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Validate status if provided
    if 'status' in data and data['status'] not in VALID_STATUSES:
        return jsonify({
            "error": f"Invalid status. Must be one of: {VALID_STATUSES}"
        }), 400

    # Validate date if provided
    if 'target_date' in data:
        try:
            datetime.strptime(data['target_date'], '%Y-%m-%d')
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    # Update fields
    for field in ['name', 'description', 'target_date', 'status']:
        if field in data:
            course[field] = data[field]

    save_courses(courses)
    return jsonify({
        "message": "Course updated successfully",
        "course": course
    }), 200


@app.route('/api/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    """Delete a course by ID"""
    courses = load_courses()
    course = next((c for c in courses if c['id'] == course_id), None)
    if not course:
        return jsonify({"error": f"Course with ID {course_id} not found"}), 404

    courses = [c for c in courses if c['id'] != course_id]
    save_courses(courses)
    return jsonify({
        "message": f"Course with ID {course_id} deleted successfully"
    }), 200


# ─── Startup ─────────────────────────────────────────────────

if __name__ == '__main__':
    print("CodeCraftHub API is starting...")
    print(f"Data file path: {DATA_FILE}")
    print("API will be available at: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)