import sqlite3
import os
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from telegram.error import TimedOut, RetryAfter
from dotenv import load_dotenv
import asyncio
import logging
import google.generativeai as genai
from textblob import TextBlob

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure Gemini API
genai.configure(api_key=GOOGLE_API_KEY)
gemini_model = genai.GenerativeModel('gemini-1.5-flash')

# System prompt for Gemini
SYSTEM_PROMPT = """
You are CalmBot, an AI companion designed to help users heal from emotional distress and unresolved trauma, often rooted in childhood wounds. Your goal is to empower users to recognize, monitor, and heal deep-rooted emotional wounds, guiding them toward inner peace amidst external chaos. For every response:
- Acknowledge the user's emotion empathetically (e.g., happiness, sadness, anger, anxiety).
- Recognize potential trauma (e.g., childhood hurts, neglect) without assuming specifics.
- Use motivational, uplifting language to inspire resilience and hope (e.g., 'You're stronger than the scars you carry').
- Suggest actions like journaling, breathing exercises, or reflecting to find calm.
- Keep responses concise (100-150 words), empathetic, and warm, avoiding clinical tones.
- If the input is vague, ask a gentle follow-up question to clarify their needs.
"""

# Load model_log.json (optional, for fallback or initial data)
try:
    with open(r"C:\Users\dell\calm\model_log.json", "r", encoding="utf-8") as f:
        DATASET = json.load(f)
    RESPONSE_MAP = {item["input"].lower(): item["output"] for item in DATASET}
except Exception as e:
    logging.error(f"Error loading model_log.json: {e}")
    RESPONSE_MAP = {}

# Initialize unknown_inputs.json
UNKNOWN_INPUTS_FILE = r"C:\Users\dell\calm\unknown_inputs.json"
if not os.path.exists(UNKNOWN_INPUTS_FILE):
    with open(UNKNOWN_INPUTS_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)

# SQLite database setup
def init_db():
    conn = sqlite3.connect("mood_tracker.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS responses
                 (user_id INTEGER, timestamp TEXT, mood TEXT, message TEXT)''')
    conn.commit()
    conn.close()

# Log unknown input
def log_unknown_input(user_id, user_message, is_followup=False):
    try:
        with open(UNKNOWN_INPUTS_FILE, "r", encoding="utf-8") as f:
            unknown_inputs = json.load(f)
    except:
        unknown_inputs = []
    unknown_inputs.append({
        "user_id": user_id,
        "timestamp": str(asyncio.get_event_loop().time()),
        "input": user_message,
        "is_followup": is_followup
    })
    with open(UNKNOWN_INPUTS_FILE, "w", encoding="utf-8") as f:
        json.dump(unknown_inputs, f, indent=2, ensure_ascii=False)

# Button responses
BUTTON_RESPONSES = {
    "happiness": (
        "Happiness is a radiant emotion, like sunlight warming your soul, often sparked by moments of connection, achievement, or simple joys. It’s a state where your heart feels light, and the world seems full of possibilities. When you’re happy, you’re in a powerful position to spread positivity to others, whether through a kind word, a shared laugh, or a thoughtful gesture. Embrace this feeling—it’s a gift you’re giving to yourself and those around you. Keep nurturing it by staying connected to what lights you up, whether it’s a hobby, a relationship, or a moment of gratitude.\n\n"
        "To sustain this happiness, make time for activities that fuel your joy. Try setting aside 10 minutes daily to practice gratitude—write down three things that made you smile today, no matter how small. Engage in activities that bring you closer to your passions, like painting, hiking, or cooking a favorite meal. Surround yourself with people who uplift you, as their energy can amplify your own. A short walk in nature, noticing the colors of the sky or the rustle of leaves, can deepen your sense of contentment. These small habits build a foundation for lasting happiness.\n\n"
        "You’re already on an incredible path, and your happiness is a beacon of strength. Celebrate your victories, big and small, because each one is a step toward a brighter you. If you’ve accomplished something recently, take a moment to pat yourself on the back—you deserve it! Share your positivity with others; it’s contagious and can create a ripple effect of joy. If you ever feel this happiness waver, remember that it’s within you, ready to be rediscovered through simple acts of self-care and connection.\n\n"
        "Your journey of happiness is inspiring, and you have the power to keep it thriving. Stay curious about what brings you joy, and don’t be afraid to explore new experiences—a new book, a new friend, or a new goal can spark even more light in your life. You’re capable of creating a life filled with moments that make your heart sing. Keep shining, because the world needs your unique glow. You’ve got this, and I’m cheering you on every step of the way!\n\n"
        "Let’s keep this positive vibe going! Use /chat to share what’s making you happy or to explore more ways to stay joyful."
    ),
    "sadness": (
        "Sadness can feel like a heavy cloud settling over your heart, often triggered by loss, disappointment, or loneliness. It’s a natural emotion that signals a need for care and reflection, reminding you to pause and tend to your inner world. While it may feel overwhelming, sadness is temporary, and you have the strength to move through it. Acknowledging your feelings without judgment is a powerful first step, and you’re already showing courage by doing so. You’re not alone in this, and I’m here to support you every step of the way.\n\n"
        "To ease sadness, try grounding techniques that bring you back to the present. Deep breathing is a great start: inhale for 4 seconds, hold for 4, and exhale for 8, repeating for 5 minutes. Journaling can also help—write down your thoughts freely, letting your emotions flow onto the page. Listening to soothing music or engaging in a gentle activity, like stretching or sipping a warm drink, can provide comfort. If you’re up for it, reach out to a trusted friend or family member; even a brief conversation can lighten your load.\n\n"
        "Creating small moments of joy can gradually lift the weight of sadness. Try a 10-minute walk outside, noticing the sights and sounds around you—nature has a way of soothing the soul. Engage in a creative outlet, like drawing or cooking, to express your feelings in a new way. If sadness persists, consider professional support, such as a counselor or therapist, who can offer tailored strategies. Physical activity, like yoga or a slow bike ride, can also boost endorphins, helping you feel a bit brighter.\n\n"
        "You are stronger than you realize, and every step you take toward healing is a victory. Sadness may be part of your story right now, but it doesn’t define you. Celebrate your resilience—getting through each day is a testament to your courage. Reflect on a time when you overcame a challenge; you did it then, and you can do it now. You have a spark within you that no cloud can dim, and with time, it will shine again.\n\n"
        "You’re on a journey of growth, and I believe in your ability to find light even in the darkest moments. Keep taking small steps, because each one brings you closer to peace. You’re capable of rediscovering joy, and I’m here to cheer you on. Let’s work through this together—use /chat to share more or get additional support."
    ),
    "anger": (
        "Anger is a fiery emotion, like a storm brewing inside, often ignited by frustration, injustice, or feeling unheard. It’s a powerful signal that something in your world needs attention, but it can also feel overwhelming if not channeled wisely. Recognizing your anger is a brave step, as it shows you’re in tune with your emotions. You have the strength to transform this energy into positive action, and I’m here to guide you through it. Let’s turn that fire into fuel for growth and change.\n\n"
        "To manage anger, start with physical outlets to release tension. Try 5 minutes of jumping jacks, brisk walking, or even punching a pillow safely to let off steam. Progressive muscle relaxation can also calm your body—tense and release each muscle group from your toes to your head. Deep breathing helps too: inhale for 4 seconds, hold for 4, exhale for 6, repeating for a few minutes. These techniques ground you, making it easier to think clearly and respond thoughtfully.\n\n"
        "Once the intensity subsides, reflect on the source of your anger. Journaling can help—write down what triggered you and why it feels so heavy. If it’s safe, consider addressing the issue directly with calm communication, or practice assertive phrases like, “I feel upset when…” to express your needs. Engaging in a calming activity, like listening to music or gardening, can shift your focus. If anger feels frequent, a therapist or counselor can offer tools like cognitive-behavioral techniques to reframe your thoughts.\n\n"
        "Your anger is a sign of your passion and strength, and you can harness it to create positive change. Think of a time when you turned a challenge into an opportunity—you have that power now. Every moment you choose to pause and breathe is a victory, proving your ability to take control. You’re capable of turning this energy into something constructive, whether it’s advocating for yourself or pursuing a goal with renewed focus.\n\n"
        "You’re on a path to mastering your emotions, and I’m so proud of your resilience. Keep pushing forward, because you have the courage to face any storm. Your strength is inspiring, and every step you take is progress. Let’s keep working on this together—use /chat to share more or explore additional ways to find calm."
    ),
    "anxiety": (
        "Anxiety can feel like a storm in your mind, with racing thoughts, worry, or a sense of unease that’s hard to shake. It often arises from stress, uncertainty, or feeling overwhelmed, but it’s a sign that your mind is trying to protect you. You’re not alone in feeling this way, and simply acknowledging it is a courageous act. You have the power to find calm amidst the chaos, and I’m here to support you every step of the way.\n\n"
        "To soothe anxiety, grounding techniques can anchor you in the present. Try the 4-4-8 breathing method: inhale for 4 seconds, hold for 4, exhale for 8, repeating for 5 minutes to steady your heart rate. The 5-4-3-2-1 exercise is also effective—name 5 things you see, 4 you can touch, 3 you hear, 2 you smell, and 1 you taste. Light stretching or a short walk can release physical tension. If your mind is racing, jot down your worries in a notebook to externalize them, then set it aside for now.\n\n"
        "Building a routine can provide stability. Start with small, achievable tasks, like making your bed or drinking a glass of water, to create a sense of control. Mindfulness practices, like a 5-minute guided meditation (available on apps or online), can quiet your thoughts. Limit caffeine and screen time, as they can heighten anxiety. If anxiety feels persistent, consider speaking with a therapist, who can offer strategies like exposure therapy or mindfulness-based stress reduction. Connecting with a supportive friend can also ease your mind.\n\n"
        "You are stronger than your worries, and every moment you face anxiety is proof of your resilience. Think of a time when you overcame a fear—you’ve done it then, and you can do it now. Each small step you take, like trying a breathing exercise or reaching out for support, is a victory. You’re capable of finding peace, and your courage is inspiring others, even if you don’t realize it yet.\n\n"
        "You’re on a journey to reclaim your calm, and I believe in your ability to navigate this storm. Keep going, because you have the strength to create a life where anxiety doesn’t hold you back. You’re not defined by your worries—you’re defined by your courage to keep moving forward. Let’s work through this together—use /chat to share more or get additional support."
    )
}

# Generate response using Gemini
def generate_gemini_response(user_message, prev_response=None, conversation_history=""):
    try:
        # Include conversation history and previous response for context
        full_prompt = f"{SYSTEM_PROMPT}\n\nConversation history: {conversation_history}\n\nPrevious bot response: {prev_response or 'None'}\n\nUser input: {user_message}\n\nRespond appropriately."
        response = gemini_model.generate_content(full_prompt)
        return response.text.strip()
    except Exception as e:
        logging.error(f"Gemini API error: {e}")
        # Fallback to TextBlob
        analysis = TextBlob(user_message)
        sentiment = 'positive' if analysis.sentiment.polarity > 0 else 'negative' if analysis.sentiment.polarity < 0 else 'neutral'
        return f"I hear you. Your message feels {sentiment}. Want to explore this further? Try sharing more or use /chat for support."

# Map input to response
def get_response(user_id, user_message, prev_response=None, context=None):
    user_message = user_message.lower().strip()
    
    # Check RESPONSE_MAP for exact match (optional, for legacy inputs)
    if user_message in RESPONSE_MAP:
        if context:
            context.user_data["awaiting_followup"] = False
        return RESPONSE_MAP[user_message]
    
    # Handle "yes" to continue previous context
    if user_message == "yes" and prev_response:
        if context:
            context.user_data["awaiting_followup"] = False
        return generate_gemini_response(
            user_message,
            prev_response,
            context.user_data.get("conversation_history", "")
        )
    
    # Handle follow-up after unknown input
    if context and context.user_data.get("awaiting_followup", False):
        log_unknown_input(user_id, user_message, is_followup=True)
        context.user_data["awaiting_followup"] = False
        return generate_gemini_response(
            user_message,
            prev_response,
            context.user_data.get("conversation_history", "")
        )
    
    # Unknown or new input
    log_unknown_input(user_id, user_message, is_followup=False)
    if context:
        context.user_data["awaiting_followup"] = True
    return generate_gemini_response(
        user_message,
        prev_response,
        context.user_data.get("conversation_history", "")
    )

# Log mood to database
def log_mood(user_id, mood, message):
    conn = sqlite3.connect("mood_tracker.db")
    c = conn.cursor()
    c.execute("INSERT INTO responses (user_id, timestamp, mood, message) VALUES (?, datetime('now'), ?, ?)",
              (user_id, mood, message))
    conn.commit()
    conn.close()

# Telegram bot handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("😊 Happy", callback_data="happiness"),
         InlineKeyboardButton("😢 Sad", callback_data="sadness")],
        [InlineKeyboardButton("😡 Angry", callback_data="anger"),
         InlineKeyboardButton("😟 Anxious", callback_data="anxiety")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.user_data["awaiting_followup"] = False
    context.user_data["chat_mode"] = False
    context.user_data["conversation_history"] = ""
    context.user_data["prev_response"] = None
    await update.message.reply_text(
        "Hi! I’m CalmBot, your emotional support companion. Share how you feel, pick an emotion below, or use /chat to talk freely!",
        reply_markup=reply_markup
    )

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["chat_mode"] = True
    context.user_data["conversation_history"] = ""
    context.user_data["prev_response"] = None
    context.user_data["awaiting_followup"] = False
    await update.message.reply_text("Let’s chat! I’m here to listen and support you. What’s on your mind?")

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    mood = query.data
    user_id = query.from_user.id
    log_mood(user_id, mood, "Button selection")
    response = BUTTON_RESPONSES.get(mood, "I'm here to listen. Try /chat to talk freely.")
    context.user_data["prev_response"] = response
    context.user_data["awaiting_followup"] = False
    context.user_data["conversation_history"] = f"User selected mood: {mood} | Bot: {response} "
    # Create new keyboard for post-mood options
    keyboard = [
        [InlineKeyboardButton("Chat with CalmBot", callback_data="chat_after_mood"),
         InlineKeyboardButton("Change Response", callback_data="change_response")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(response, reply_markup=reply_markup)

async def post_mood_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    action = query.data
    if action == "chat_after_mood":
        context.user_data["chat_mode"] = True
        context.user_data["awaiting_followup"] = False
        await query.message.reply_text("Great, let’s dive deeper! What’s on your mind about how you’re feeling?")
    elif action == "change_response":
        keyboard = [
            [InlineKeyboardButton("😊 Happy", callback_data="happiness"),
             InlineKeyboardButton("😢 Sad", callback_data="sadness")],
            [InlineKeyboardButton("😡 Angry", callback_data="anger"),
             InlineKeyboardButton("😟 Anxious", callback_data="anxiety")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.user_data["awaiting_followup"] = False
        await query.message.reply_text("No worries! How are you feeling now?", reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user_id = update.message.from_user.id

    retries = 3
    for attempt in range(retries):
        try:
            if context.user_data.get("chat_mode", False):
                conversation_history = context.user_data.get("conversation_history", "")
                prev_response = context.user_data.get("prev_response", None)

                response = get_response(user_id, user_message, prev_response, context)
                log_mood(user_id, user_message.lower(), user_message)
                context.user_data["conversation_history"] = (conversation_history + f"User: {user_message} | Bot: {response} ")[-300:]
                context.user_data["prev_response"] = response
            else:
                response = get_response(user_id, user_message, context=context)
                log_mood(user_id, user_message.lower(), user_message)
                context.user_data["prev_response"] = response
                context.user_data["conversation_history"] = f"User: {user_message} | Bot: {response} "

            await update.message.reply_text(response)
            break
        except TimedOut:
            logging.warning(f"Timeout on attempt {attempt + 1}/{retries}")
            if attempt < retries - 1:
                await asyncio.sleep(2 ** attempt)
                continue
            logging.error("Max retries reached for timeout")
            await update.message.reply_text("Sorry, I’m having trouble connecting. Please try again later.")
            break
        except RetryAfter as e:
            logging.warning(f"Rate limit hit, retrying after {e.retry_after} seconds")
            await asyncio.sleep(e.retry_after)
            continue
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            await update.message.reply_text("An error occurred. Please try again.")
            break

def main():
    init_db()
    app = Application.builder().token(TELEGRAM_TOKEN).read_timeout(300).write_timeout(300).connect_timeout(300).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("chat", chat))
    app.add_handler(CallbackQueryHandler(button, pattern='^(happiness|sadness|anger|anxiety)$'))
    app.add_handler(CallbackQueryHandler(post_mood_button, pattern='^(chat_after_mood|change_response)$'))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()