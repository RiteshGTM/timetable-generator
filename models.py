"""
Data models for SmartTable - College Timetable Generator
"""

class Course:
    """Course model for managing course information"""
    
    def __init__(self, id=None, code="", name="", sessions_per_week=0, course_type="Theory"):
        self.id = id
        self.code = code
        self.name = name
        self.sessions_per_week = sessions_per_week
        self.course_type = course_type
    
    def to_dict(self):
        """Convert Course object to dictionary for JSON storage"""
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'sessions_per_week': self.sessions_per_week,
            'course_type': self.course_type
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create Course object from dictionary"""
        return cls(
            id=data.get('id'),
            code=data.get('code', ''),
            name=data.get('name', ''),
            sessions_per_week=data.get('sessions_per_week', 0),
            course_type=data.get('course_type', 'Theory')
        )


class Teacher:
    """Teacher model for managing teacher information"""
    
    def __init__(self, id=None, name="", department=""):
        self.id = id
        self.name = name
        self.department = department
    
    def to_dict(self):
        """Convert Teacher object to dictionary for JSON storage"""
        return {
            'id': self.id,
            'name': self.name,
            'department': self.department
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create Teacher object from dictionary"""
        return cls(
            id=data.get('id'),
            name=data.get('name', ''),
            department=data.get('department', '')
        )


class Room:
    """Room model for managing room information"""
    
    def __init__(self, id=None, room_number="", capacity=0, room_type="Theory"):
        self.id = id
        self.room_number = room_number
        self.capacity = capacity
        self.room_type = room_type
    
    def to_dict(self):
        """Convert Room object to dictionary for JSON storage"""
        return {
            'id': self.id,
            'room_number': self.room_number,
            'capacity': self.capacity,
            'room_type': self.room_type
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create Room object from dictionary"""
        return cls(
            id=data.get('id'),
            room_number=data.get('room_number', ''),
            capacity=data.get('capacity', 0),
            room_type=data.get('room_type', 'Theory')
        )


class TimeSlot:
    """TimeSlot model for managing time slot information"""
    
    def __init__(self, id=None, day="", period=0, start_time="", end_time=""):
        self.id = id
        self.day = day
        self.period = period
        self.start_time = start_time
        self.end_time = end_time
    
    def to_dict(self):
        """Convert TimeSlot object to dictionary for JSON storage"""
        return {
            'id': self.id,
            'day': self.day,
            'period': self.period,
            'start_time': self.start_time,
            'end_time': self.end_time
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create TimeSlot object from dictionary"""
        return cls(
            id=data.get('id'),
            day=data.get('day', ''),
            period=data.get('period', 0),
            start_time=data.get('start_time', ''),
            end_time=data.get('end_time', '')
        )


class StudentGroup:
    """StudentGroup model for managing student group information"""
    
    def __init__(self, id=None, name="", semester=0, department=""):
        self.id = id
        self.name = name
        self.semester = semester
        self.department = department
    
    def to_dict(self):
        """Convert StudentGroup object to dictionary for JSON storage"""
        return {
            'id': self.id,
            'name': self.name,
            'semester': self.semester,
            'department': self.department
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create StudentGroup object from dictionary"""
        return cls(
            id=data.get('id'),
            name=data.get('name', ''),
            semester=data.get('semester', 0),
            department=data.get('department', '')
        )
