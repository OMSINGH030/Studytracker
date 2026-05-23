#!/usr/bin/env python3
"""
Study Tracker Application
Track daily to weekly study progress and become an effective learner.
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
import sqlite3
from typing import List, Dict, Optional
from tabulate import tabulate
import schedule
import time
import threading


class StudyTracker:
    """Main study tracker class for managing study sessions and goals."""
    
    def __init__(self, db_path: str = "study_tracker.db"):
        """Initialize the study tracker with database."""
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database with required tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                subject TEXT NOT NULL,
                duration_minutes INTEGER NOT NULL,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create goals table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT NOT NULL,
                target_hours REAL NOT NULL,
                target_date TEXT NOT NULL,
                completed BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create reminders table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT NOT NULL,
                reminder_time TEXT NOT NULL,
                message TEXT,
                active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_session(self, subject: str, duration_minutes: int, date: Optional[str] = None, notes: str = "") -> bool:
        """Add a new study session."""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        if duration_minutes <= 0:
            print("❌ Duration must be positive!")
            return False
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO sessions (date, subject, duration_minutes, notes)
                VALUES (?, ?, ?, ?)
            ''', (date, subject, duration_minutes, notes))
            conn.commit()
            conn.close()
            print(f"✅ Session added: {subject} - {duration_minutes} minutes on {date}")
            return True
        except Exception as e:
            print(f"❌ Error adding session: {e}")
            return False
    
    def get_sessions(self, days: int = 7, subject: Optional[str] = None) -> List[Dict]:
        """Get study sessions from the last N days."""
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            if subject:
                cursor.execute('''
                    SELECT * FROM sessions 
                    WHERE date >= ? AND subject = ?
                    ORDER BY date DESC
                ''', (start_date, subject))
            else:
                cursor.execute('''
                    SELECT * FROM sessions 
                    WHERE date >= ?
                    ORDER BY date DESC
                ''', (start_date,))
            
            sessions = [dict(row) for row in cursor.fetchall()]
            conn.close()
            return sessions
        except Exception as e:
            print(f"❌ Error retrieving sessions: {e}")
            return []
    
    def add_goal(self, subject: str, target_hours: float, days_ahead: int = 7) -> bool:
        """Add a study goal."""
        target_date = (datetime.now() + timedelta(days=days_ahead)).strftime("%Y-%m-%d")
        
        if target_hours <= 0:
            print("❌ Target hours must be positive!")
            return False
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO goals (subject, target_hours, target_date)
                VALUES (?, ?, ?)
            ''', (subject, target_hours, target_date))
            conn.commit()
            conn.close()
            print(f"✅ Goal added: {subject} - {target_hours} hours by {target_date}")
            return True
        except Exception as e:
            print(f"❌ Error adding goal: {e}")
            return False
    
    def get_goals(self, completed: Optional[bool] = None) -> List[Dict]:
        """Get all goals or filter by completion status."""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            if completed is not None:
                cursor.execute('SELECT * FROM goals WHERE completed = ? ORDER BY target_date', (completed,))
            else:
                cursor.execute('SELECT * FROM goals ORDER BY target_date')
            
            goals = [dict(row) for row in cursor.fetchall()]
            conn.close()
            return goals
        except Exception as e:
            print(f"❌ Error retrieving goals: {e}")
            return []
    
    def update_goal_status(self, goal_id: int, completed: bool) -> bool:
        """Update goal completion status."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('UPDATE goals SET completed = ? WHERE id = ?', (completed, goal_id))
            conn.commit()
            conn.close()
            status = "completed" if completed else "pending"
            print(f"✅ Goal {goal_id} marked as {status}")
            return True
        except Exception as e:
            print(f"❌ Error updating goal: {e}")
            return False
    
    def add_reminder(self, subject: str, reminder_time: str, message: str = "") -> bool:
        """Add a study reminder (format: HH:MM)."""
        try:
            # Validate time format
            datetime.strptime(reminder_time, "%H:%M")
        except ValueError:
            print("❌ Invalid time format. Use HH:MM (24-hour format)")
            return False
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            if not message:
                message = f"Time to study {subject}!"
            cursor.execute('''
                INSERT INTO reminders (subject, reminder_time, message)
                VALUES (?, ?, ?)
            ''', (subject, reminder_time, message))
            conn.commit()
            conn.close()
            print(f"✅ Reminder added: {subject} at {reminder_time}")
            return True
        except Exception as e:
            print(f"❌ Error adding reminder: {e}")
            return False
    
    def get_reminders(self, active_only: bool = True) -> List[Dict]:
        """Get reminders."""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            if active_only:
                cursor.execute('SELECT * FROM reminders WHERE active = 1 ORDER BY reminder_time')
            else:
                cursor.execute('SELECT * FROM reminders ORDER BY reminder_time')
            
            reminders = [dict(row) for row in cursor.fetchall()]
            conn.close()
            return reminders
        except Exception as e:
            print(f"❌ Error retrieving reminders: {e}")
            return []
    
    def generate_progress_report(self, days: int = 7) -> None:
        """Generate a progress report for the past N days."""
        sessions = self.get_sessions(days=days)
        goals = self.get_goals()
        
        print("\n" + "="*60)
        print(f"📊 STUDY PROGRESS REPORT - Last {days} days")
        print("="*60)
        
        if not sessions:
            print("No study sessions recorded in this period.")
        else:
            # Summary by subject
            subject_stats = {}
            for session in sessions:
                subject = session['subject']
                if subject not in subject_stats:
                    subject_stats[subject] = 0
                subject_stats[subject] += session['duration_minutes']
            
            print("\n📚 Study Time by Subject:")
            table_data = [[subject, f"{minutes}m ({minutes/60:.1f}h)"] 
                         for subject, minutes in sorted(subject_stats.items(), key=lambda x: x[1], reverse=True)]
            print(tabulate(table_data, headers=["Subject", "Total Time"], tablefmt="grid"))
            
            total_minutes = sum(subject_stats.values())
            print(f"\n⏱️  Total Study Time: {total_minutes} minutes ({total_minutes/60:.1f} hours)")
            
            # Daily breakdown
            daily_stats = {}
            for session in sessions:
                date = session['date']
                if date not in daily_stats:
                    daily_stats[date] = 0
                daily_stats[date] += session['duration_minutes']
            
            print("\n📅 Daily Breakdown:")
            daily_table = [[date, f"{minutes}m"] for date, minutes in sorted(daily_stats.items())]
            print(tabulate(daily_table, headers=["Date", "Duration"], tablefmt="grid"))
        
        # Goal progress
        print("\n🎯 Goal Progress:")
        if not goals:
            print("No goals set yet.")
        else:
            goal_table = []
            for goal in goals:
                subject = goal['subject']
                target = goal['target_hours']
                target_date = goal['target_date']
                
                # Calculate progress
                subject_sessions = self.get_sessions(subject=subject)
                progress_hours = sum(s['duration_minutes'] for s in subject_sessions) / 60
                percentage = (progress_hours / target * 100) if target > 0 else 0
                status = "✅ Completed" if goal['completed'] else "⏳ In Progress"
                
                goal_table.append([subject, f"{progress_hours:.1f}h / {target}h", f"{min(percentage, 100):.0f}%", status])
            
            print(tabulate(goal_table, headers=["Subject", "Progress", "Percentage", "Status"], tablefmt="grid"))
        
        print("\n" + "="*60 + "\n")


def main_menu():
    """Display main menu and handle user input."""
    tracker = StudyTracker()
    
    while True:
        print("\n" + "="*60)
        print("📖 STUDY TRACKER - Main Menu")
        print("="*60)
        print("1. ➕ Add Study Session")
        print("2. 📊 View Sessions")
        print("3. 🎯 Add Study Goal")
        print("4. 👁️  View Goals")
        print("5. ✔️  Mark Goal Complete")
        print("6. 🔔 Add Reminder")
        print("7. 🔊 View Reminders")
        print("8. 📈 Generate Progress Report")
        print("9. 🚀 Start Reminder Service")
        print("0. ❌ Exit")
        print("="*60)
        
        choice = input("Select an option (0-9): ").strip()
        
        if choice == "1":
            subject = input("Subject: ").strip()
            try:
                duration = int(input("Duration (minutes): ").strip())
                notes = input("Notes (optional): ").strip()
                tracker.add_session(subject, duration, notes=notes)
            except ValueError:
                print("❌ Invalid duration. Please enter a number.")
        
        elif choice == "2":
            try:
                days = int(input("View sessions from last N days (default 7): ") or "7")
            except ValueError:
                days = 7
            
            subject_filter = input("Filter by subject (leave empty for all): ").strip() or None
            sessions = tracker.get_sessions(days=days, subject=subject_filter)
            
            if sessions:
                table_data = [[s['date'], s['subject'], f"{s['duration_minutes']}m", s['notes']] for s in sessions]
                print("\n" + tabulate(table_data, headers=["Date", "Subject", "Duration", "Notes"], tablefmt="grid"))
            else:
                print("No sessions found.")
        
        elif choice == "3":
            subject = input("Subject: ").strip()
            try:
                hours = float(input("Target hours: ").strip())
                days = int(input("Days to complete (default 7): ") or "7")
                tracker.add_goal(subject, hours, days)
            except ValueError:
                print("❌ Invalid input. Please enter numbers.")
        
        elif choice == "4":
            goals = tracker.get_goals()
            if goals:
                table_data = [[g['id'], g['subject'], f"{g['target_hours']}h", g['target_date'], 
                              "✅ Yes" if g['completed'] else "❌ No"] for g in goals]
                print("\n" + tabulate(table_data, headers=["ID", "Subject", "Target", "Due Date", "Completed"], tablefmt="grid"))
            else:
                print("No goals found.")
        
        elif choice == "5":
            try:
                goal_id = int(input("Goal ID: ").strip())
                tracker.update_goal_status(goal_id, True)
            except ValueError:
                print("❌ Invalid ID.")
        
        elif choice == "6":
            subject = input("Subject: ").strip()
            time_str = input("Reminder time (HH:MM, 24-hour format): ").strip()
            message = input("Message (optional): ").strip()
            tracker.add_reminder(subject, time_str, message)
        
        elif choice == "7":
            reminders = tracker.get_reminders()
            if reminders:
                table_data = [[r['id'], r['subject'], r['reminder_time'], r['message']] for r in reminders]
                print("\n" + tabulate(table_data, headers=["ID", "Subject", "Time", "Message"], tablefmt="grid"))
            else:
                print("No reminders found.")
        
        elif choice == "8":
            try:
                days = int(input("Report for last N days (default 7): ") or "7")
            except ValueError:
                days = 7
            tracker.generate_progress_report(days=days)
        
        elif choice == "9":
            print("🚀 Starting reminder service (runs in background)...")
            start_reminder_service(tracker)
            print("Reminder service started! You can continue using the tracker.")
        
        elif choice == "0":
            print("👋 Goodbye! Keep studying!")
            break
        
        else:
            print("❌ Invalid option. Please try again.")


def start_reminder_service(tracker: StudyTracker):
    """Start the reminder service in a background thread."""
    def run_reminders():
        reminders = tracker.get_reminders()
        for reminder in reminders:
            schedule.every().day.at(reminder['reminder_time']).do(
                lambda msg=reminder['message']: print(f"\n🔔 REMINDER: {msg}")
            )
        
        while True:
            schedule.run_pending()
            time.sleep(60)
    
    reminder_thread = threading.Thread(target=run_reminders, daemon=True)
    reminder_thread.start()


if __name__ == "__main__":
    main_menu()
