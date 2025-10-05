"""
Utility functions for SmartTable - College Timetable Generator
"""

import json
import os
import time
from datetime import datetime


def load_json(filename):
    """
    Load data from JSON file in data/ folder
    Returns empty list if file doesn't exist
    """
    data_dir = "data"
    filepath = os.path.join(data_dir, filename)
    
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as file:
                return json.load(file)
        else:
            return []
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading {filename}: {e}")
        return []


def save_json(filename, data):
    """
    Save data to JSON file in data/ folder with proper formatting
    """
    data_dir = "data"
    
    # Create data directory if it doesn't exist
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    filepath = os.path.join(data_dir, filename)
    
    try:
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
        return True
    except IOError as e:
        print(f"Error saving {filename}: {e}")
        return False


def generate_id():
    """
    Generate unique ID using timestamp and random component
    """
    import random
    timestamp = int(time.time() * 1000)
    random_component = random.randint(1000, 9999)
    return f"{timestamp}_{random_component}"


def initialize_data_files():
    """
    Create empty JSON files if they don't exist
    """
    files_to_create = [
        'courses.json',
        'teachers.json', 
        'rooms.json',
        'timeslots.json',
        'groups.json',
        'timetable.json'
    ]
    
    for filename in files_to_create:
        filepath = os.path.join("data", filename)
        if not os.path.exists(filepath):
            save_json(filename, [])
            print(f"Created empty {filename}")


def create_sample_data():
    """
    Generate sample data for the timetable application
    """
    from models import Course, Teacher, Room, TimeSlot, StudentGroup
    
    # Create sample courses
    courses = [
        Course(id=generate_id(), code="CS101", name="Data Structures", sessions_per_week=3, course_type="Theory"),
        Course(id=generate_id(), code="CS102", name="Database Lab", sessions_per_week=2, course_type="Lab"),
        Course(id=generate_id(), code="CS103", name="Algorithms", sessions_per_week=3, course_type="Theory"),
        Course(id=generate_id(), code="CS104", name="Web Technology", sessions_per_week=3, course_type="Theory"),
        Course(id=generate_id(), code="CS105", name="Programming Lab", sessions_per_week=2, course_type="Lab")
    ]
    
    # Create sample teachers
    teachers = [
        Teacher(id=generate_id(), name="Dr. John Smith", department="Computer Science"),
        Teacher(id=generate_id(), name="Prof. Sarah Johnson", department="Computer Science"),
        Teacher(id=generate_id(), name="Dr. Michael Brown", department="Computer Science"),
        Teacher(id=generate_id(), name="Prof. Emily Davis", department="Computer Science")
    ]
    
    # Create sample rooms
    rooms = [
        Room(id=generate_id(), room_number="A101", capacity=60, room_type="Theory"),
        Room(id=generate_id(), room_number="A102", capacity=60, room_type="Theory"),
        Room(id=generate_id(), room_number="Lab1", capacity=30, room_type="Lab"),
        Room(id=generate_id(), room_number="Lab2", capacity=30, room_type="Lab")
    ]
    
    # Create sample time slots (Monday to Friday, 8 periods each day)
    timeslots = []
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    time_periods = [
        ("09:00", "10:00"), ("10:00", "11:00"), ("11:00", "12:00"), ("12:00", "13:00"),
        ("13:00", "14:00"), ("14:00", "15:00"), ("15:00", "16:00"), ("16:00", "17:00")
    ]
    
    for day in days:
        for period, (start_time, end_time) in enumerate(time_periods, 1):
            timeslots.append(TimeSlot(
                id=generate_id(),
                day=day,
                period=period,
                start_time=start_time,
                end_time=end_time
            ))
    
    # Create sample student groups
    groups = [
        StudentGroup(id=generate_id(), name="CS-A", semester=3, department="Computer Science"),
        StudentGroup(id=generate_id(), name="CS-B", semester=3, department="Computer Science"),
        StudentGroup(id=generate_id(), name="IT-A", semester=3, department="Information Technology")
    ]
    
    # Save all data to JSON files
    save_json('courses.json', [course.to_dict() for course in courses])
    save_json('teachers.json', [teacher.to_dict() for teacher in teachers])
    save_json('rooms.json', [room.to_dict() for room in rooms])
    save_json('timeslots.json', [timeslot.to_dict() for timeslot in timeslots])
    save_json('groups.json', [group.to_dict() for group in groups])
    save_json('timetable.json', [])  # Empty timetable initially
    
    print("Sample data created successfully!")
    return {
        'courses': len(courses),
        'teachers': len(teachers),
        'rooms': len(rooms),
        'timeslots': len(timeslots),
        'groups': len(groups)
    }
