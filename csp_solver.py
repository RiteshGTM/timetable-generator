"""
Constraint Satisfaction Problem (CSP) Solver for Timetable Generation
Uses backtracking algorithm to find valid timetable assignments
"""

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
    
    def solve(self):
        """
        Main solving method using backtracking algorithm
        
        Returns:
            List of assignments if solution found, None if no solution
        """
        print("Starting CSP solver...")
        
        # Try to schedule each course
        for course in self.courses:
            print(f"Processing course: {course['code']} - {course['name']}")
            
            # For each student group
            for group in self.groups:
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
        # Try all possible combinations of teacher, room, and timeslot
        for teacher in self.teachers:
            # Get rooms that match the course type
            valid_rooms = self.get_rooms_for_course(course, self.rooms)
            
            for room in valid_rooms:
                for timeslot in self.timeslots:
                    # Check if this assignment is valid
                    if self.is_valid(course, teacher, room, timeslot, group):
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
                                               timeslot['day'], timeslot['period'])
                        
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
        
        # All constraints satisfied
        return True
    
    def _update_assignments(self, teacher_id, room_id, group_id, day, period):
        """
        Update tracking dictionaries after successful assignment
        
        Args:
            teacher_id: ID of assigned teacher
            room_id: ID of assigned room
            group_id: ID of assigned group
            day: Day of assignment
            period: Period of assignment
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

