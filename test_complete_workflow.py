#!/usr/bin/env python3
"""
Complete Workflow Test for SmartTable - College Timetable Generator
Tests all major functionality including edge cases and error handling.
"""

import requests
import json
import time
import sys

# Test configuration
BASE_URL = "http://localhost:5000"
API_BASE = f"{BASE_URL}/api"

def print_test_header(test_name):
    """Print formatted test header"""
    print(f"\n{'='*60}")
    print(f"TEST: {test_name}")
    print(f"{'='*60}")

def print_result(success, message):
    """Print test result"""
    status = "PASS" if success else "FAIL"
    print(f"[{status}]: {message}")

def test_server_connection():
    """Test if server is running"""
    print_test_header("Server Connection")
    try:
        response = requests.get(BASE_URL, timeout=5)
        if response.status_code == 200:
            print_result(True, "Server is running and accessible")
            return True
        else:
            print_result(False, f"Server returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_result(False, "Cannot connect to server. Make sure Flask app is running.")
        return False
    except Exception as e:
        print_result(False, f"Unexpected error: {str(e)}")
        return False

def test_api_endpoints():
    """Test all API endpoints"""
    print_test_header("API Endpoints")
    
    endpoints = [
        ("/api/courses", "GET"),
        ("/api/teachers", "GET"),
        ("/api/rooms", "GET"),
        ("/api/timeslots", "GET"),
        ("/api/groups", "GET"),
        ("/api/timetable", "GET")
    ]
    
    all_passed = True
    
    for endpoint, method in endpoints:
        try:
            url = f"{API_BASE}{endpoint}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                print_result(True, f"{method} {endpoint} - {len(data)} items")
            else:
                print_result(False, f"{method} {endpoint} - Status {response.status_code}")
                all_passed = False
                
        except Exception as e:
            print_result(False, f"{method} {endpoint} - Error: {str(e)}")
            all_passed = False
    
    return all_passed

def test_data_validation():
    """Test data validation and error handling"""
    print_test_header("Data Validation")
    
    # Test invalid course data
    invalid_course = {
        "code": "",  # Empty code
        "name": "",  # Empty name
        "sessions_per_week": 0,  # Invalid sessions
        "course_type": ""  # Empty type
    }
    
    try:
        response = requests.post(f"{API_BASE}/courses", 
                               json=invalid_course, 
                               headers={'Content-Type': 'application/json'})
        
        if response.status_code == 400:
            print_result(True, "Invalid course data properly rejected")
        else:
            print_result(False, f"Expected 400, got {response.status_code}")
            return False
            
    except Exception as e:
        print_result(False, f"Error testing validation: {str(e)}")
        return False
    
    return True

def test_crud_operations():
    """Test CRUD operations for all entities"""
    print_test_header("CRUD Operations")
    
    # Test data
    test_course = {
        "code": "TEST101",
        "name": "Test Course",
        "sessions_per_week": 3,
        "course_type": "Theory"
    }
    
    try:
        # Create
        response = requests.post(f"{API_BASE}/courses", 
                               json=test_course,
                               headers={'Content-Type': 'application/json'})
        
        if response.status_code == 200:
            data = response.json()
            course_id = data['course']['id']
            print_result(True, f"Course created with ID: {course_id}")
            
            # Read
            response = requests.get(f"{API_BASE}/courses")
            if response.status_code == 200:
                courses = response.json()
                if any(c['id'] == course_id for c in courses):
                    print_result(True, "Course found in list")
                else:
                    print_result(False, "Course not found in list")
                    return False
            else:
                print_result(False, "Failed to read courses")
                return False
            
            # Update
            update_data = {"name": "Updated Test Course"}
            response = requests.put(f"{API_BASE}/courses/{course_id}",
                                  json=update_data,
                                  headers={'Content-Type': 'application/json'})
            
            if response.status_code == 200:
                print_result(True, "Course updated successfully")
            else:
                print_result(False, f"Failed to update course: {response.status_code}")
                return False
            
            # Delete
            response = requests.delete(f"{API_BASE}/courses/{course_id}")
            if response.status_code == 200:
                print_result(True, "Course deleted successfully")
            else:
                print_result(False, f"Failed to delete course: {response.status_code}")
                return False
                
        else:
            print_result(False, f"Failed to create course: {response.status_code}")
            return False
            
    except Exception as e:
        print_result(False, f"Error in CRUD operations: {str(e)}")
        return False
    
    return True

def test_timetable_generation():
    """Test timetable generation with sample data"""
    print_test_header("Timetable Generation")
    
    try:
        # Check if we have enough data for generation
        response = requests.get(f"{API_BASE}/courses")
        courses = response.json() if response.status_code == 200 else []
        
        response = requests.get(f"{API_BASE}/teachers")
        teachers = response.json() if response.status_code == 200 else []
        
        response = requests.get(f"{API_BASE}/rooms")
        rooms = response.json() if response.status_code == 200 else []
        
        response = requests.get(f"{API_BASE}/timeslots")
        timeslots = response.json() if response.status_code == 200 else []
        
        response = requests.get(f"{API_BASE}/groups")
        groups = response.json() if response.status_code == 200 else []
        
        print(f"Data available: {len(courses)} courses, {len(teachers)} teachers, {len(rooms)} rooms, {len(timeslots)} timeslots, {len(groups)} groups")
        
        if len(courses) == 0 or len(teachers) == 0 or len(rooms) == 0 or len(timeslots) == 0 or len(groups) == 0:
            print_result(False, "Insufficient data for timetable generation")
            return False
        
        # Attempt generation
        response = requests.post(f"{API_BASE}/generate")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print_result(True, f"Timetable generated successfully! {result.get('summary', {}).get('total_assignments', 0)} assignments created")
                return True
            else:
                print_result(False, f"Generation failed: {result.get('message', 'Unknown error')}")
                return False
        else:
            result = response.json()
            print_result(False, f"Generation failed: {result.get('message', 'Unknown error')}")
            return False
            
    except Exception as e:
        print_result(False, f"Error in timetable generation: {str(e)}")
        return False

def test_edge_cases():
    """Test edge cases and error handling"""
    print_test_header("Edge Cases")
    
    try:
        # Test generation with no data
        # First, backup current data
        courses_response = requests.get(f"{API_BASE}/courses")
        if courses_response.status_code == 200:
            original_courses = courses_response.json()
            
            # Clear courses temporarily
            for course in original_courses:
                requests.delete(f"{API_BASE}/courses/{course['id']}")
            
            # Try generation
            response = requests.post(f"{API_BASE}/generate")
            if response.status_code == 400:
                print_result(True, "Generation properly fails with no courses")
            else:
                print_result(False, f"Expected 400 for no courses, got {response.status_code}")
            
            # Restore courses
            for course in original_courses:
                requests.post(f"{API_BASE}/courses", 
                            json=course,
                            headers={'Content-Type': 'application/json'})
            
        # Test duplicate course code
        duplicate_course = {
            "code": "CS101",  # Assuming this exists
            "name": "Duplicate Course",
            "sessions_per_week": 2,
            "course_type": "Theory"
        }
        
        response = requests.post(f"{API_BASE}/courses",
                               json=duplicate_course,
                               headers={'Content-Type': 'application/json'})
        
        if response.status_code == 400:
            print_result(True, "Duplicate course code properly rejected")
        else:
            print_result(False, f"Expected 400 for duplicate code, got {response.status_code}")
        
        return True
        
    except Exception as e:
        print_result(False, f"Error testing edge cases: {str(e)}")
        return False

def test_ui_pages():
    """Test that all UI pages are accessible"""
    print_test_header("UI Pages")
    
    pages = [
        ("/", "Dashboard"),
        ("/courses", "Manage Courses"),
        ("/teachers", "Manage Teachers"),
        ("/rooms", "Manage Rooms"),
        ("/timeslots", "Manage Time Slots"),
        ("/groups", "Manage Groups"),
        ("/generate", "Generate Timetable"),
        ("/view-timetable", "View Timetable")
    ]
    
    all_passed = True
    
    for page, name in pages:
        try:
            response = requests.get(f"{BASE_URL}{page}", timeout=5)
            if response.status_code == 200:
                print_result(True, f"{name} page accessible")
            else:
                print_result(False, f"{name} page returned {response.status_code}")
                all_passed = False
        except Exception as e:
            print_result(False, f"{name} page error: {str(e)}")
            all_passed = False
    
    return all_passed

def main():
    """Run all tests"""
    print("SmartTable - Complete Workflow Test")
    print("=" * 60)
    
    tests = [
        ("Server Connection", test_server_connection),
        ("API Endpoints", test_api_endpoints),
        ("Data Validation", test_data_validation),
        ("CRUD Operations", test_crud_operations),
        ("UI Pages", test_ui_pages),
        ("Timetable Generation", test_timetable_generation),
        ("Edge Cases", test_edge_cases)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print_result(False, f"Test {test_name} crashed: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print_test_header("Test Summary")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"[{status}]: {test_name}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n[SUCCESS] All tests passed! The application is ready for demonstration.")
        return 0
    else:
        print(f"\n[WARNING] {total - passed} tests failed. Please fix issues before demonstration.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
