# 📖 Study Tracker

A comprehensive Python application to track your daily to weekly study progress and become an effective learner.

## ✨ Features

✅ **Track Study Sessions** - Log your study sessions with date, duration, and subject
🎯 **Set Goals & Targets** - Define study goals with target hours and due dates
📊 **Progress Reports** - View detailed progress reports for any time period
🔔 **Reminders** - Set automated study reminders at specific times
💾 **Data Persistence** - All data is stored in SQLite database
📈 **Progress Analytics** - Track progress by subject and view daily breakdowns

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/OMSINGH030/Studytracker.git
cd Studytracker
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python study_tracker.py
```

## 📋 Usage Guide

### Main Menu Options

```
1. ➕ Add Study Session
   - Log a new study session
   - Provide: Subject, Duration (minutes), and optional notes

2. 📊 View Sessions
   - View all study sessions from the last N days
   - Filter by subject if needed

3. 🎯 Add Study Goal
   - Set a target study hours for a subject
   - Choose how many days to complete the goal

4. 👁️  View Goals
   - See all your study goals
   - Track progress towards each goal

5. ✔️  Mark Goal Complete
   - Mark a goal as completed when achieved
   - Track goal completion status

6. 🔔 Add Reminder
   - Set daily study reminders at specific times
   - Format: HH:MM (24-hour format)

7. 🔊 View Reminders
   - See all active reminders
   - Manage your reminder schedule

8. 📈 Generate Progress Report
   - View comprehensive progress analytics
   - See study time by subject and daily breakdowns

9. 🚀 Start Reminder Service
   - Start background reminder notifications
   - Reminders run automatically based on schedule

0. ❌ Exit
   - Close the application
```

## 📊 Example Workflow

### 1. Add a Study Session
```
Subject: Mathematics
Duration: 60 minutes
Notes: Completed Chapter 5 exercises
```

### 2. Set a Goal
```
Subject: Mathematics
Target: 10 hours
Days to complete: 7
```

### 3. Add a Reminder
```
Subject: Mathematics
Time: 18:00
Message: Time to study Mathematics!
```

### 4. View Progress Report
```
Get a detailed report showing:
- Total study time
- Breakdown by subject
- Daily study schedule
- Progress towards goals
- Goal completion status
```

## 💾 Database Structure

The application uses SQLite with three main tables:

### Sessions Table
- Stores individual study sessions
- Fields: date, subject, duration_minutes, notes

### Goals Table
- Stores study goals
- Fields: subject, target_hours, target_date, completed status

### Reminders Table
- Stores study reminders
- Fields: subject, reminder_time, message, active status

## 🎨 Features in Detail

### Study Sessions
- Track every study session with date and duration
- Add optional notes for each session
- View sessions filtered by date range or subject

### Goal Tracking
- Set realistic study goals with deadlines
- Track progress towards each goal
- See percentage completion
- Mark goals as complete when achieved

### Progress Reports
- **Daily Breakdown**: See how much you studied each day
- **Subject Analysis**: Track total hours per subject
- **Goal Progress**: Monitor advancement towards targets
- **Performance Metrics**: View study patterns and trends

### Reminder System
- Set reminders at specific times (24-hour format)
- Background reminder service runs continuously
- Get notified about upcoming study sessions
- Customize reminder messages

## 🔧 Advanced Usage

### View Goals with Filters
```python
# View only pending goals
# View only completed goals
```

### Generate Custom Reports
```bash
# Generate report for last 30 days
# Generate report for specific subject
```

## 📝 Tips for Effective Studying

1. **Log Consistently** - Record every study session immediately
2. **Set Realistic Goals** - Break large objectives into manageable targets
3. **Use Reminders** - Set reminders for optimal study times
4. **Review Progress** - Generate weekly reports to track trends
5. **Adjust Goals** - Update goals based on progress and feedback

## 🐛 Troubleshooting

### Module Not Found Error
```bash
pip install -r requirements.txt
```

### Database Lock Error
- Ensure only one instance of the application is running
- Close the application and restart

### Reminders Not Working
- Ensure the reminder service is started (option 9)
- Check that the time format is correct (HH:MM)
- The application must be running for reminders to work

## 📈 Data Export

All data is stored in `study_tracker.db` (SQLite format).

To export data:
```bash
# View sessions
sqlite3 study_tracker.db "SELECT * FROM sessions;"

# View goals
sqlite3 study_tracker.db "SELECT * FROM goals;"

# View reminders
sqlite3 study_tracker.db "SELECT * FROM reminders;"
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 🎯 Future Enhancements

- [ ] Web interface (Flask/Django)
- [ ] Statistics and visualization (graphs/charts)
- [ ] Export to CSV/PDF
- [ ] Cloud synchronization
- [ ] Mobile app
- [ ] Calendar view
- [ ] Subject difficulty tracking
- [ ] Study break recommendations

## 📧 Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Happy Studying! 📚** Keep tracking your progress and become an effective learner! 🚀
