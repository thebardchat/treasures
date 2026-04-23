import pyttsx3

engine = pyttsx3.init()
affirmations = """
Every moment I stay goal-oriented, become a better Dad, and feel better, I break free from the chains of procrastination and not working out. 
I am becoming the person who is naturally goal-oriented, a better Dad, and feels better. 
I release anxiety and welcome the joy of being goal-oriented, a better Dad, and feeling better.
"""
engine.save_to_file(affirmations, 'affirmations.mp3')
engine.runAndWait()