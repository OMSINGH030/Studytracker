#!/usr/bin/env python3
"""
Example usage script for the Study Tracker application.
Demonstrates all major features.
"""

from study_tracker import StudyTracker
from datetime import datetime, timedelta


def example_usage():
    """Run example usage of the Study Tracker."""
    
    print("="*60)
    print("🎓 STUDY TRACKER - Example Usage")
    print("="*60)
    
    # Initialize tracker
    tracker = StudyTracker("example_tracker.db")
    
    # Example 1: Add study sessions
    print("\n1️⃣  Adding study sessions...")
    tracker.add_session("Mathematics", 60, notes="Algebra exercises")
    tracker.add_session("Python Programming", 90, notes="Object-oriented design")
    tracker.add_session("History", 45, notes="Ancient Rome chapter")
    tracker.add_session("Mathematics", 30, notes="Problem set 3")
    
    # Example 2: View sessions
    print("\n2️⃣  Viewing recent sessions...")
    sessions = tracker.get_sessions(days=7)
    print(f"Found {len(sessions)} sessions in the last 7 days")
    
    # Example 3: Add goals
    print("\n3️⃣  Setting study goals...")
    tracker.add_goal("Mathematics", 10, days_ahead=7)
    tracker.add_goal("Python Programming", 15, days_ahead=14)
    tracker.add_goal("History", 5, days_ahead=7)
    
    # Example 4: View goals
    print("\n4️⃣  Viewing all goals...")
    goals = tracker.get_goals()
    print(f"Total goals: {len(goals)}")
    
    # Example 5: Add reminders
    print("\n5️⃣  Setting study reminders...")
    tracker.add_reminder("Mathematics", "18:00", "Time for your daily Math study!")
    tracker.add_reminder("Python Programming", "19:30", "Let's code some Python!")
    tracker.add_reminder("History", "20:00", "Time to read that history chapter")
    
    # Example 6: View reminders
    print("\n6️⃣  Viewing active reminders...")
    reminders = tracker.get_reminders()
    print(f"Total reminders: {len(reminders)}")
    
    # Example 7: Generate progress report
    print("\n7️⃣  Generating progress report...")
    tracker.generate_progress_report(days=7)
    
    # Example 8: Update goal status
    print("\n8️⃣  Marking a goal as complete...")
    if goals:
        tracker.update_goal_status(goals[0]['id'], True)
    
    print("\n" + "="*60)
    print("✅ Example complete! Now run 'python study_tracker.py'")
    print("="*60)


if __name__ == "__main__":
    example_usage()
