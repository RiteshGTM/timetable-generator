# SmartTable - College Timetable Generator

A modern, intelligent timetable generation system for colleges and universities using Constraint Satisfaction Problem (CSP) algorithms.

## 🚀 Features

- **Intelligent Timetable Generation**: Uses advanced CSP algorithms to automatically generate conflict-free timetables
- **Modern Web Interface**: Beautiful, responsive UI built with Bootstrap 5 and Flask
- **Complete Data Management**: Add, edit, and delete courses, teachers, rooms, time slots, and student groups
- **Multiple View Modes**: View timetables by student group, teacher, or room
- **Real-time Validation**: Client-side and server-side validation with helpful error messages
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile devices
- **Professional UI**: Modern admin dashboard with smooth animations and transitions

## 🛠️ Technology Stack

- **Backend**: Flask (Python web framework)
- **Frontend**: Bootstrap 5.3, HTML5, CSS3, JavaScript
- **Icons**: Font Awesome 6
- **Fonts**: Google Fonts (Inter, Poppins)
- **Algorithm**: Constraint Satisfaction Problem (CSP) with backtracking
- **Data Storage**: JSON files (easily extensible to database)

## 📋 Requirements

- Python 3.7 or higher
- Flask 3.0.0
- Modern web browser (Chrome, Firefox, Safari, Edge)

## 🚀 Installation

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd college-timetable-generator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:5000`

## 📖 How to Use

### 1. **Add Data**
   - **Courses**: Add course codes, names, sessions per week, and type (Theory/Lab)
   - **Teachers**: Add teacher names and subjects
   - **Rooms**: Add room numbers, types (Theory/Lab), and capacity
   - **Time Slots**: Define daily periods and time ranges
   - **Student Groups**: Add group names and sizes

### 2. **Generate Timetable**
   - Click "Generate Timetable" button
   - The system automatically creates a conflict-free schedule
   - View results in multiple formats (Group/Teacher/Room views)

### 3. **View and Manage**
   - Browse generated timetables
   - Edit data as needed
   - Regenerate timetables with updated constraints

## 🎯 Key Features

### **Smart Algorithm**
- **Constraint Satisfaction**: Ensures no teacher, room, or group conflicts
- **Room Type Matching**: Theory courses in theory rooms, lab courses in lab rooms
- **Automatic Scheduling**: Finds optimal time slots for all sessions
- **Conflict Resolution**: Handles complex scheduling constraints automatically

### **User Experience**
- **Intuitive Interface**: Easy-to-use forms with real-time validation
- **Visual Feedback**: Toast notifications, loading states, and confirmation dialogs
- **Responsive Design**: Works on all device sizes
- **Professional Styling**: Modern admin dashboard with smooth animations

### **Data Management**
- **CRUD Operations**: Create, Read, Update, Delete for all entities
- **Validation**: Comprehensive client-side and server-side validation
- **Error Handling**: Graceful error handling with helpful messages
- **Data Persistence**: JSON file storage with automatic backup

## 📁 Project Structure

```
timetable-generator/
├── app.py                 # Main Flask application
├── models.py              # Data models (Course, Teacher, Room, etc.)
├── utils.py               # Utility functions for JSON operations
├── csp_solver.py          # CSP algorithm implementation
├── requirements.txt       # Python dependencies
├── data/                  # JSON data files
│   ├── courses.json
│   ├── teachers.json
│   ├── rooms.json
│   ├── timeslots.json
│   ├── groups.json
│   └── timetable.json
├── static/
│   ├── css/
│   │   └── style.css      # Custom styling
│   └── js/
│       └── script.js      # JavaScript functionality
└── templates/
    ├── base.html          # Base template
    ├── index.html         # Dashboard
    ├── manage_courses.html
    ├── manage_teachers.html
    ├── manage_rooms.html
    ├── manage_timeslots.html
    ├── manage_groups.html
    ├── generate.html      # Timetable generation
    ├── view_timetable.html
    └── 404.html
```

## 🔧 API Endpoints

### **Data Management**
- `GET /api/courses` - Get all courses
- `POST /api/courses` - Add new course
- `PUT /api/courses/<id>` - Update course
- `DELETE /api/courses/<id>` - Delete course
- Similar endpoints for teachers, rooms, timeslots, groups

### **Timetable Generation**
- `POST /api/generate` - Generate new timetable
- `GET /api/timetable` - Get current timetable

## 🎨 Customization

### **Adding New Course Colors**
Edit `static/css/style.css` to add new course color classes:
```css
.course-newcolor {
    background: linear-gradient(135deg, #color1, #color2);
    border-left: 4px solid #border-color;
}
```

### **Modifying Time Slots**
Update the time slot generation in `utils.py`:
```python
def create_sample_data():
    # Modify time slots here
    timeslots = [
        {'id': '1', 'period': 1, 'start_time': '09:00', 'end_time': '10:00'},
        # Add more periods
    ]
```

## 🐛 Troubleshooting

### **Common Issues**

1. **"No module named 'flask'"**
   ```bash
   pip install -r requirements.txt
   ```

2. **"Port 5000 already in use"**
   ```bash
   # Kill process using port 5000
   netstat -ano | findstr :5000
   taskkill /PID <process_id> /F
   ```

3. **"Timetable generation fails"**
   - Ensure you have at least one course, teacher, room, timeslot, and group
   - Check that room types match course types (Theory/Lab)
   - Verify sufficient time slots for all sessions

### **Performance Tips**
- For large datasets (100+ courses), consider database storage
- Optimize time slot ranges for better generation speed
- Use pagination for large data tables

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🎓 Educational Use

This project is perfect for:
- **Computer Science Education**: Demonstrates CSP algorithms
- **Software Engineering**: Shows full-stack development
- **College Administration**: Real-world timetable management
- **Algorithm Study**: Constraint satisfaction problem implementation

## 📞 Support

For questions or issues:
1. Check the troubleshooting section above
2. Review the code comments for implementation details
3. Create an issue in the repository

---

**SmartTable** - Making timetable generation intelligent and effortless! 🎯

