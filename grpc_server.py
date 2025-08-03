import grpc
from concurrent import futures
import sqlite3
import os
from textblob import TextBlob
import google.generativeai as genai
from dotenv import load_dotenv
import calmbot_pb2
import calmbot_pb2_grpc

def init_db():
    conn = sqlite3.connect('mood_tracker.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS moods (
            user_id TEXT,
            mood TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS journal (
            user_id TEXT,
            mood TEXT,
            entry TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Load configuration and set up Gemini AI
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
gemini_model = genai.GenerativeModel("gemini-1.5-flash")

SYSTEM_PROMPT = """
You are CalmBot, an AI companion designed to help users heal from emotional distress and unresolved trauma.
"""

def generate_response(text: str) -> str:
    try:
        prompt = f"""{SYSTEM_PROMPT}
User input: {text}
Respond appropriately."""
        response = gemini_model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        # fallback on TextBlob sentiment
        polarity = TextBlob(text).sentiment.polarity
        label = 'positive' if polarity > 0 else 'negative' if polarity < 0 else 'neutral'
        return f"I hear you. Your input feels {label}."

class CalmbotService(calmbot_pb2_grpc.CalmbotServiceServicer):
    def LogMood(self, request, context):
        conn = sqlite3.connect('mood_tracker.db')
        c = conn.cursor()
        c.execute("INSERT INTO moods (user_id, mood) VALUES (?, ?)",
                  (request.user_id, request.mood))
        conn.commit()
        conn.close()
        reply = generate_response(f"User is feeling {request.mood}.")
        return calmbot_pb2.LogMoodResponse(reply=reply)

    def Chat(self, request, context):
        reply = generate_response(request.message)
        return calmbot_pb2.ChatResponse(reply=reply)

    def SaveJournal(self, request, context):
        conn = sqlite3.connect('mood_tracker.db')
        c = conn.cursor()
        c.execute(
            "INSERT INTO journal (user_id, mood, entry) VALUES (?, ?, ?)",
            (request.user_id, request.mood or '', request.entry)
        )
        conn.commit()
        conn.close()
        reply = generate_response(request.entry)
        return calmbot_pb2.JournalResponse(reply=reply)

    def GetProgress(self, request, context):
        conn = sqlite3.connect('mood_tracker.db')
        c = conn.cursor()
        c.execute(
            "SELECT mood, COUNT(*) FROM moods WHERE user_id = ? GROUP BY mood",
            (request.user_id,)
        )
        rows = c.fetchall()
        conn.close()

        emotion_map = {e: 0 for e in ['happiness', 'sadness', 'anger', 'anxiety']}
        for mood, count in rows:
            emotion_map[mood] = count

        summary = (
            f"You've logged {sum(emotion_map.values())} moods: "
            + ", ".join(f"{e} ({c})" for e, c in emotion_map.items())
        )
        return calmbot_pb2.ProgressResponse(
            emotions=list(emotion_map.keys()),
            counts=list(emotion_map.values()),
            summary=summary
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    calmbot_pb2_grpc.add_CalmbotServiceServicer_to_server(CalmbotService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()