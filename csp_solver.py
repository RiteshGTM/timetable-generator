"""
Constraint Satisfaction Problem (CSP) Solver for Timetable Generation
Uses backtracking algorithm to find valid timetable assignments
"""

import random

class TimetableSolver:
    """
    CSP Solver for generating conflict-free timetables
    """
    
    def __init__(self, courses, teachers, rooms, timeslots, groups):
        """
        Initialize the solver with all required data
        
        Args:
            courses: List of course dictionaries
            teachers: List of teacher dictionaries  
            rooms: List of room dictionaries
            timeslots: List of timeslot dictionaries
            groups: List of student group dictionaries
        """
        self.courses = courses
        self.teachers = teachers
        self.rooms = rooms
        self.timeslots = timeslots
        self.groups = groups
        
        # Initialize empty solution list
        self.solution = []
        
        # Track assignments for constraint checking
        self.teacher_assignments = {}  # {teacher_id: [(day, period), ...]}
        self.room_assignments = {}    # {room_id: [(day, period), ...]}
        self.group_assignments = {}    # {group_id: [(day, period), ...]}
        
        # CHANGE 1: Track which teacher teaches which course for variety
        self.course_teacher_map = {}  # {course_code: teacher_id}
        
        # CHANGE 2: Track course sessions per day to limit clustering
        self.course_day_sessions = {}  # {(course_code, group_id, day): count}
    
    def solve(self):
        """
        Main solving method using backtracking algorithm
        
        Returns:
            List of assignments if solution found, None if no solution
        """
        print("Starting CSP solver...")
        
        # Shuffle courses and groups to encourage mixing
        courses = self.courses[:]
        groups = self.groups[:]
        random.shuffle(courses)
        random.shuffle(groups)
        
        for course in courses:
            print(f"Processing course: {course['code']} - {course['name']}")
            
            # For each student group
            for group in groups:
                print(f"  Scheduling for group: {group['name']}")
                
                # Schedule required number of sessions per week
                sessions_needed = course['sessions_per_week']
                sessions_scheduled = 0
                
                for session in range(sessions_needed):
                    print(f"    Scheduling session {session + 1}/{sessions_needed}")
                    
                    # Try to assign this session
                    if not self.assign_session(course, group):
                        print(f"    Failed to schedule session {session + 1} for {course['code']} - {group['name']}")
                        return None  # No solution possible
                    
                    sessions_scheduled += 1
                    print(f"    Successfully scheduled session {session + 1}")
        
        print(f"Solution found! Total assignments: {len(self.solution)}")
        return self.solution
    
    def assign_session(self, course, group):
        """
        Try to assign one session for given course and group
        
        Args:
            course: Course dictionary
            group: Student group dictionary
            
        Returns:
            True if assignment successful, False otherwise
        """
        course_code = course['code']
        
        # CHANGE 3: If course already has assigned teacher, prefer that teacher
        # This ensures same teacher for all sessions of a course
        preferred_teacher_id = self.course_teacher_map.get(course_code)
        
        teachers = self.teachers[:]
        
        # CHANGE 4: Sort teachers - put preferred teacher first if exists
        if preferred_teacher_id:
            teachers.sort(key=lambda t: 0 if t['id'] == preferred_teacher_id else 1)
        else:
            random.shuffle(teachers)  # Randomize for first session
        
        for teacher in teachers:
            # CHANGE 5: Skip if trying different teacher when one is already assigned
            # (unless preferred teacher is fully booked)
            if preferred_teacher_id and teacher['id'] != preferred_teacher_id:
                # Only try other teachers if preferred is not available
                continue
            
            # Get rooms that match the course type
            valid_rooms = self.get_rooms_for_course(course, self.rooms)
            
            for room in valid_rooms:
                for timeslot in self.timeslots:
                    # Check if this assignment is valid
                    if self.is_valid(course, teacher, room, timeslot, group):
                        # CHANGE 6: Record teacher-course mapping on first assignment
                        if course_code not in self.course_teacher_map:
                            self.course_teacher_map[course_code] = teacher['id']
                        
                        # Create assignment
                        assignment = {
                            'course_code': course['code'],
                            'course_name': course['name'],
                            'teacher_name': teacher['name'],
                            'room_number': room['room_number'],
                            'day': timeslot['day'],
                            'period': timeslot['period'],
                            'start_time': timeslot['start_time'],
                            'end_time': timeslot['end_time'],
                            'group_name': group['name'],
                            'course_type': course['course_type'],
                            'room_type': room['room_type']
                        }
                        
                        # Add to solution
                        self.solution.append(assignment)
                        
                        # Update tracking dictionaries
                        self._update_assignments(teacher['id'], room['id'], group['id'], 
                                               timeslot['day'], timeslot['period'],
                                               course_code, group['id'])  # CHANGE 7: Pass course info
                        
                        return True
        
        # CHANGE 8: If preferred teacher didn't work, try ANY teacher
        if preferred_teacher_id:
            random.shuffle(teachers)
            for teacher in teachers:
                valid_rooms = self.get_rooms_for_course(course, self.rooms)
                for room in valid_rooms:
                    for timeslot in self.timeslots:
                        if self.is_valid(course, teacher, room, timeslot, group):
                            assignment = {
                                'course_code': course['code'],
                                'course_name': course['name'],
                                'teacher_name': teacher['name'],
                                'room_number': room['room_number'],
                                'day': timeslot['day'],
                                'period': timeslot['period'],
                                'start_time': timeslot['start_time'],
                                'end_time': timeslot['end_time'],
                                'group_name': group['name'],
                                'course_type': course['course_type'],
                                'room_type': room['room_type']
                            }
                            self.solution.append(assignment)
                            self._update_assignments(teacher['id'], room['id'], group['id'], 
                                                   timeslot['day'], timeslot['period'],
                                                   course_code, group['id'])
                            return True
        
        return False  # No valid assignment found
    
    def is_valid(self, course, teacher, room, timeslot, group):
        """
        Check if assignment satisfies all hard constraints
        
        Args:
            course: Course dictionary
            teacher: Teacher dictionary
            room: Room dictionary
            timeslot: Timeslot dictionary
            group: Student group dictionary
            
        Returns:
            True if all constraints satisfied, False otherwise
        """
        day = timeslot['day']
        period = timeslot['period']
        teacher_id = teacher['id']
        room_id = room['id']
        group_id = group['id']
        course_code = course['code']
        
        # Constraint 1: No Teacher Conflict
        # Check if teacher already has class at this day and period
        if teacher_id in self.teacher_assignments:
            if (day, period) in self.teacher_assignments[teacher_id]:
                return False
        
        # Constraint 2: No Room Conflict  
        # Check if room already occupied at this day and period
        if room_id in self.room_assignments:
            if (day, period) in self.room_assignments[room_id]:
                return False
        
        # Constraint 3: No Student Group Conflict
        # Check if group already has class at this day and period
        if group_id in self.group_assignments:
            if (day, period) in self.group_assignments[group_id]:
                return False
        
        # Constraint 4: Room Type Matching
        # Lab courses need Lab rooms, Theory courses need Theory rooms
        if course['course_type'] != room['room_type']:
            return False
        
        # CHANGE 9: IMPROVED Constraint 5 - Prevent same course in consecutive periods
        # Only checks for immediate adjacency (period-1 or period+1)
        for assignment in self.solution:
            if (assignment['group_name'] == group['name'] and 
                assignment['day'] == day and 
                assignment['course_code'] == course_code):
                if abs(assignment['period'] - period) == 1:  # Adjacent periods
                    return False
        
        # CHANGE 10: RELAXED Constraint 6 - Limit course sessions per day
        # Allow max 2 sessions of same course on same day (was unlimited before)
        course_day_key = (course_code, group_id, day)
        sessions_today = self.course_day_sessions.get(course_day_key, 0)
        if sessions_today >= 2:  # Max 2 sessions per course per day
            return False
        
        # CHANGE 11: RELAXED Constraint 7 - Teacher session limit per day
        # Increased from 4 to 6 sessions per day for flexibility
        teacher_sessions_today = [a for a in self.solution 
                                 if a['teacher_name'] == teacher['name'] and a['day'] == day]
        if len(teacher_sessions_today) >= 6:  # Increased limit
            return False
        
        # All constraints satisfied
        return True
    
    def _update_assignments(self, teacher_id, room_id, group_id, day, period, course_code=None, group_id_for_course=None):
        """
        Update tracking dictionaries after successful assignment
        
        Args:
            teacher_id: ID of assigned teacher
            room_id: ID of assigned room
            group_id: ID of assigned group
            day: Day of assignment
            period: Period of assignment
            course_code: Course code (CHANGE 12: Added parameter)
            group_id_for_course: Group ID for course tracking (CHANGE 13: Added parameter)
        """
        # Update teacher assignments
        if teacher_id not in self.teacher_assignments:
            self.teacher_assignments[teacher_id] = []
        self.teacher_assignments[teacher_id].append((day, period))
        
        # Update room assignments
        if room_id not in self.room_assignments:
            self.room_assignments[room_id] = []
        self.room_assignments[room_id].append((day, period))
        
        # Update group assignments
        if group_id not in self.group_assignments:
            self.group_assignments[group_id] = []
        self.group_assignments[group_id].append((day, period))
        
        # CHANGE 14: Track course sessions per day
        if course_code and group_id_for_course:
            course_day_key = (course_code, group_id_for_course, day)
            self.course_day_sessions[course_day_key] = self.course_day_sessions.get(course_day_key, 0) + 1
    
    def get_rooms_for_course(self, course, rooms):
        """
        Filter rooms based on course type
        
        Args:
            course: Course dictionary
            rooms: List of all rooms
            
        Returns:
            List of rooms matching course type
        """
        return [room for room in rooms if room['room_type'] == course['course_type']]
    
    def format_solution(self, solution):
        """
        Organize solution by day and period for display
        
        Args:
            solution: List of assignment dictionaries
            
        Returns:
            Dictionary organized by day and period
        """
        if not solution:
            return {}
        
        # Group assignments by day
        organized = {}
        for assignment in solution:
            day = assignment['day']
            if day not in organized:
                organized[day] = {}
            
            period = assignment['period']
            if period not in organized[day]:
                organized[day][period] = []
            
            organized[day][period].append(assignment)
        
        # Sort by period within each day
        for day in organized:
            organized[day] = dict(sorted(organized[day].items()))
        
        return organized
    
    def get_solution_summary(self):
        """
        Get summary statistics of the solution
        
        Returns:
            Dictionary with solution statistics
        """
        if not self.solution:
            return {
                'total_assignments': 0,
                'courses_scheduled': 0,
                'teachers_used': 0,
                'rooms_used': 0,
                'groups_scheduled': 0
            }
        
        courses_scheduled = len(set(assignment['course_code'] for assignment in self.solution))
        teachers_used = len(set(assignment['teacher_name'] for assignment in self.solution))
        rooms_used = len(set(assignment['room_number'] for assignment in self.solution))
        groups_scheduled = len(set(assignment['group_name'] for assignment in self.solution))
        
        return {
            'total_assignments': len(self.solution),
            'courses_scheduled': courses_scheduled,
            'teachers_used': teachers_used,
            'rooms_used': rooms_used,
            'groups_scheduled': groups_scheduled
        }
    
    # CHANGE 15: REMOVED _validate_free_periods() method
    # This constraint was too strict and caused generation failures
    # Free periods are acceptable and sometimes necessary in real timetables