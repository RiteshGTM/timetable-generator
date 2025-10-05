from flask import Flask, render_template, request, jsonify
from utils import initialize_data_files, create_sample_data, load_json, save_json, generate_id
from models import Course, Teacher, Room, TimeSlot, StudentGroup
from csp_solver import TimetableSolver

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Initialize data files and create sample data on startup
initialize_data_files()
sample_data = create_sample_data()
print(f"Application initialized with {sample_data}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/courses')
def courses():
    return render_template('manage_courses.html')

@app.route('/teachers')
def teachers():
    return render_template('manage_teachers.html')

@app.route('/rooms')
def rooms():
    return render_template('manage_rooms.html')

@app.route('/timeslots')
def timeslots():
    return render_template('manage_timeslots.html')

@app.route('/groups')
def groups():
    return render_template('manage_groups.html')

@app.route('/generate')
def generate():
    return render_template('generate.html')

@app.route('/view-timetable')
def view_timetable():
    return render_template('view_timetable.html')

# API Routes for Courses
@app.route('/api/courses', methods=['GET'])
def get_courses():
    try:
        courses = load_json('courses.json')
        return jsonify(courses)
    except Exception as e:
        print(f"Error loading courses: {str(e)}")
        return jsonify({'error': 'Failed to load courses'}), 500

@app.route('/api/courses', methods=['POST'])
def add_course():
    try:
        data = request.json
        if not data:
            return jsonify({'success': False, 'message': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['code', 'name', 'sessions_per_week', 'course_type']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'message': f'{field.replace("_", " ").title()} is required'}), 400
        
        # Check for duplicate course code
        courses = load_json('courses.json')
        if any(course['code'] == data['code'] for course in courses):
            return jsonify({'success': False, 'message': 'Course code already exists'}), 400
        
        course = Course(
            id=generate_id(),
            code=data.get('code'),
            name=data.get('name'),
            sessions_per_week=data.get('sessions_per_week'),
            course_type=data.get('course_type')
        )
        
        courses.append(course.to_dict())
        if save_json('courses.json', courses):
            return jsonify({'success': True, 'course': course.to_dict()})
        else:
            return jsonify({'success': False, 'message': 'Failed to save course'}), 500
            
    except Exception as e:
        print(f"Error adding course: {str(e)}")
        return jsonify({'success': False, 'message': 'Failed to add course'}), 500

@app.route('/api/courses/<course_id>', methods=['PUT'])
def update_course(course_id):
    data = request.json
    courses = load_json('courses.json')
    for i, course in enumerate(courses):
        if course['id'] == course_id:
            courses[i].update(data)
            save_json('courses.json', courses)
            return jsonify({'success': True, 'course': courses[i]})
    return jsonify({'success': False, 'message': 'Course not found'}), 404

@app.route('/api/courses/<course_id>', methods=['DELETE'])
def delete_course(course_id):
    courses = load_json('courses.json')
    courses = [course for course in courses if course['id'] != course_id]
    save_json('courses.json', courses)
    return jsonify({'success': True})

# API Routes for Teachers
@app.route('/api/teachers', methods=['GET'])
def get_teachers():
    teachers = load_json('teachers.json')
    return jsonify(teachers)

@app.route('/api/teachers', methods=['POST'])
def add_teacher():
    data = request.json
    teacher = Teacher(
        id=generate_id(),
        name=data.get('name'),
        department=data.get('department')
    )
    teachers = load_json('teachers.json')
    teachers.append(teacher.to_dict())
    save_json('teachers.json', teachers)
    return jsonify({'success': True, 'teacher': teacher.to_dict()})

@app.route('/api/teachers/<teacher_id>', methods=['PUT'])
def update_teacher(teacher_id):
    data = request.json
    teachers = load_json('teachers.json')
    for i, teacher in enumerate(teachers):
        if teacher['id'] == teacher_id:
            teachers[i].update(data)
            save_json('teachers.json', teachers)
            return jsonify({'success': True, 'teacher': teachers[i]})
    return jsonify({'success': False, 'message': 'Teacher not found'}), 404

@app.route('/api/teachers/<teacher_id>', methods=['DELETE'])
def delete_teacher(teacher_id):
    teachers = load_json('teachers.json')
    teachers = [teacher for teacher in teachers if teacher['id'] != teacher_id]
    save_json('teachers.json', teachers)
    return jsonify({'success': True})

# API Routes for Rooms
@app.route('/api/rooms', methods=['GET'])
def get_rooms():
    rooms = load_json('rooms.json')
    return jsonify(rooms)

@app.route('/api/rooms', methods=['POST'])
def add_room():
    data = request.json
    room = Room(
        id=generate_id(),
        room_number=data.get('room_number'),
        capacity=data.get('capacity'),
        room_type=data.get('room_type')
    )
    rooms = load_json('rooms.json')
    rooms.append(room.to_dict())
    save_json('rooms.json', rooms)
    return jsonify({'success': True, 'room': room.to_dict()})

@app.route('/api/rooms/<room_id>', methods=['PUT'])
def update_room(room_id):
    data = request.json
    rooms = load_json('rooms.json')
    for i, room in enumerate(rooms):
        if room['id'] == room_id:
            rooms[i].update(data)
            save_json('rooms.json', rooms)
            return jsonify({'success': True, 'room': rooms[i]})
    return jsonify({'success': False, 'message': 'Room not found'}), 404

@app.route('/api/rooms/<room_id>', methods=['DELETE'])
def delete_room(room_id):
    rooms = load_json('rooms.json')
    rooms = [room for room in rooms if room['id'] != room_id]
    save_json('rooms.json', rooms)
    return jsonify({'success': True})

# API Routes for TimeSlots
@app.route('/api/timeslots', methods=['GET'])
def get_timeslots():
    timeslots = load_json('timeslots.json')
    return jsonify(timeslots)

@app.route('/api/timeslots', methods=['POST'])
def add_timeslot():
    data = request.json
    timeslot = TimeSlot(
        id=generate_id(),
        day=data.get('day'),
        period=data.get('period'),
        start_time=data.get('start_time'),
        end_time=data.get('end_time')
    )
    timeslots = load_json('timeslots.json')
    timeslots.append(timeslot.to_dict())
    save_json('timeslots.json', timeslots)
    return jsonify({'success': True, 'timeslot': timeslot.to_dict()})

@app.route('/api/timeslots/<timeslot_id>', methods=['PUT'])
def update_timeslot(timeslot_id):
    data = request.json
    timeslots = load_json('timeslots.json')
    for i, timeslot in enumerate(timeslots):
        if timeslot['id'] == timeslot_id:
            timeslots[i].update(data)
            save_json('timeslots.json', timeslots)
            return jsonify({'success': True, 'timeslot': timeslots[i]})
    return jsonify({'success': False, 'message': 'TimeSlot not found'}), 404

@app.route('/api/timeslots/<timeslot_id>', methods=['DELETE'])
def delete_timeslot(timeslot_id):
    timeslots = load_json('timeslots.json')
    timeslots = [timeslot for timeslot in timeslots if timeslot['id'] != timeslot_id]
    save_json('timeslots.json', timeslots)
    return jsonify({'success': True})

# API Routes for Groups
@app.route('/api/groups', methods=['GET'])
def get_groups():
    groups = load_json('groups.json')
    return jsonify(groups)

@app.route('/api/groups', methods=['POST'])
def add_group():
    data = request.json
    group = StudentGroup(
        id=generate_id(),
        name=data.get('name'),
        semester=data.get('semester'),
        department=data.get('department')
    )
    groups = load_json('groups.json')
    groups.append(group.to_dict())
    save_json('groups.json', groups)
    return jsonify({'success': True, 'group': group.to_dict()})

@app.route('/api/groups/<group_id>', methods=['PUT'])
def update_group(group_id):
    data = request.json
    groups = load_json('groups.json')
    for i, group in enumerate(groups):
        if group['id'] == group_id:
            groups[i].update(data)
            save_json('groups.json', groups)
            return jsonify({'success': True, 'group': groups[i]})
    return jsonify({'success': False, 'message': 'Group not found'}), 404

@app.route('/api/groups/<group_id>', methods=['DELETE'])
def delete_group(group_id):
    groups = load_json('groups.json')
    groups = [group for group in groups if group['id'] != group_id]
    save_json('groups.json', groups)
    return jsonify({'success': True})

# Timetable Generation API
@app.route('/api/generate', methods=['POST'])
def generate_timetable():
    """
    Generate timetable using CSP solver
    """
    try:
        print("Starting timetable generation...")
        
        # Load all required data
        courses = load_json('courses.json')
        teachers = load_json('teachers.json')
        rooms = load_json('rooms.json')
        timeslots = load_json('timeslots.json')
        groups = load_json('groups.json')
        
        # Validate that all required data exists
        if not courses:
            return jsonify({'success': False, 'message': 'No courses found. Please add at least one course first.'}), 400
        
        if not teachers:
            return jsonify({'success': False, 'message': 'No teachers found. Please add at least one teacher first.'}), 400
        
        if not rooms:
            return jsonify({'success': False, 'message': 'No rooms found. Please add at least one room first.'}), 400
        
        if not timeslots:
            return jsonify({'success': False, 'message': 'No time slots found. Please add time slots first.'}), 400
        
        if not groups:
            return jsonify({'success': False, 'message': 'No student groups found. Please add at least one group first.'}), 400
        
        # Check for sufficient resources
        theory_rooms = [room for room in rooms if room['room_type'] == 'Theory']
        lab_rooms = [room for room in rooms if room['room_type'] == 'Lab']
        theory_courses = [course for course in courses if course['course_type'] == 'Theory']
        lab_courses = [course for course in courses if course['course_type'] == 'Lab']
        
        if theory_courses and not theory_rooms:
            return jsonify({'success': False, 'message': 'No theory rooms available for theory courses. Please add theory rooms.'}), 400
        
        if lab_courses and not lab_rooms:
            return jsonify({'success': False, 'message': 'No lab rooms available for lab courses. Please add lab rooms.'}), 400
        
        print(f"Loaded data: {len(courses)} courses, {len(teachers)} teachers, {len(rooms)} rooms, {len(timeslots)} timeslots, {len(groups)} groups")
        
        # Create CSP solver instance
        solver = TimetableSolver(courses, teachers, rooms, timeslots, groups)
        
        # Solve the timetable
        solution = solver.solve()
        
        if solution is None:
            return jsonify({
                'success': False, 
                'message': 'Could not generate timetable. No valid solution found. Try adjusting constraints or adding more resources.'
            }), 400
        
        # Save solution to timetable.json
        save_json('timetable.json', solution)
        
        # Get solution summary
        summary = solver.get_solution_summary()
        
        # Format solution for display
        formatted_solution = solver.format_solution(solution)
        
        print(f"Timetable generated successfully! {summary['total_assignments']} assignments created.")
        
        return jsonify({
            'success': True,
            'message': 'Timetable generated successfully!',
            'solution': solution,
            'formatted_solution': formatted_solution,
            'summary': summary
        })
        
    except Exception as e:
        print(f"Error generating timetable: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error generating timetable: {str(e)}'
        }), 500

# Get Generated Timetable
@app.route('/api/timetable', methods=['GET'])
def get_timetable():
    """
    Get the generated timetable data
    """
    try:
        timetable = load_json('timetable.json')
        return jsonify(timetable)
    except Exception as e:
        print(f"Error loading timetable: {str(e)}")
        return jsonify([])

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)

