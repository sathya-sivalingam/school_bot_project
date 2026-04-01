from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import sqlite3
import pdb

class ActionFetchAttendance(Action):
    def name(self) -> Text:
        return "action_fetch_attendance"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):
        student_id = tracker.get_slot("student_id")
        user_pin = tracker.get_slot("student_pin")

        if not student_id or not user_pin:
            dispatcher.utter_message(text="Please provide both your Student ID and PIN.")
            return []

        try:
            conn = sqlite3.connect('school_database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT name, attendance_percentage FROM student_attendance WHERE student_id=? AND pin=?", (student_id, user_pin))
            result = cursor.fetchone()
            conn.close()

            if result:
                dispatcher.utter_message(text=f"Verified. {result[0]}, your attendance is {result[1]}%.")
            else:
                dispatcher.utter_message(text="Authentication failed. Check your ID and PIN.")
        except Exception as e:
            dispatcher.utter_message(text="Error connecting to database.")
            
        return [SlotSet("student_pin", None)]
