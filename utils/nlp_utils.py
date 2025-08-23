#!/usr/bin/env python3

import spacy

# Load Spacy model
nlp = spacy.load("en_core_web_sm")

def get_bot_response(user_input: str) -> str:
    doc = nlp(user_input.lower())

    if "open" in user_input.lower() or "hours" in user_input.lower():
        return "The clinic is open from 8 AM to 4 PM, Monday to Friday."
    elif "emergency" in user_input.lower():
        return "For emergencies, please go to the ER or call campus emergency number: 123-456-7890."
    elif "book" in user_input.lower():
        return "You can book an appointment via the student portal or at the clinic reception."
    elif "contact" in user_input.lower():
        return "You can reach the clinic at clinic@example.edu or call 987-654-3210."
    else:
        return "Sorry, I didn’t understand that. I can help with opening hours, bookings, emergencies, or contact info."
