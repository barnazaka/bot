import json
import random
import itertools

# Base responses
base_log = [
    {"input": "hello", "output": "Hey there! I'm so glad you're here. How's your day going so far?"},
    {"input": "hi", "output": "Hi! It's nice to hear from you. Want to share what's on your mind today?"},
    {"input": "good morning", "output": "Good morning to you too! Let's make today a calm and happy one. How are you feeling?"},
    {"input": "I feel sad", "output": "I'm so sorry you're feeling sad. Try taking a few deep breaths and picturing a peaceful place. I'm here for you."},
    {"input": "I'm stressed", "output": "Stress can be tough. How about a quick stretch or a cup of tea to ease your mind? You've got this."},
    {"input": "My life is tough", "output": "I hear you, life can be heavy sometimes. Let's focus on one small thing that brings you joy today."},
    {"input": "I'm lonely", "output": "Loneliness can hurt, but you're not alone right now. Reach out to someone you trust, or let's chat more."},
    {"input": "Nothing is going right", "output": "When everything feels off, it's exhausting. Try listing one tiny win today, like getting out of bed. I'm cheering you on."},
    {"input": "I'm anxious", "output": "Anxiety can feel overwhelming. Try the 4-4-8 breathing technique: inhale for 4, hold for 4, exhale for 8. I'm right here."},
    {"input": "I'm tired of this", "output": "I feel how draining this is for you. Take a moment to rest and recharge. You deserve a break."},
    {"input": "I'm broke", "output": "Money worries are so hard. Can you set a small goal, like saving a dollar this week? I believe in you."},
    {"input": "Money is tight", "output": "Financial stress is rough. Try tracking one expense today to feel a bit more in control. I'm here to listen."},
    {"input": "I have no job", "output": "Being jobless is tough. Maybe check out an online course or connect with a friend for ideas. You're not alone."},
    {"input": "I'm overwhelmed", "output": "Feeling overwhelmed is a lot to carry. Break one task into tiny steps, and let's tackle it together."},
    {"input": "Can we talk", "output": "Absolutely, I'm all ears! Share what's on your heart, and let's sort through it together."},
    {"input": "yes", "output": "Great, let's keep chatting! What's one thing you'd love to focus on right now?"},
    {"input": "I want more", "output": "I love your enthusiasm! How about trying a short walk to clear your mind? I'm here for more ideas."},
    {"input": "I'm happy today", "output": "That's so wonderful to hear! What's sparking your joy today? Let's celebrate it!"},
    {"input": "I feel calm", "output": "I'm so glad you're feeling calm. Savor this moment with a cozy drink or some soft music."},
    {"input": "I'm grateful", "output": "Gratitude is beautiful! What's one thing you're thankful for today? Let's share the positivity."},
    {"input": "I need to relax", "output": "You deserve some peace. Try a 5-minute meditation or a warm bath to unwind. I'm here for you."},
    {"input": "I'm worried", "output": "Worries can weigh heavy. Write down one thing you're anxious about, and let's talk it through."},
    {"input": "I can't sleep", "output": "Trouble sleeping is tough. Try a bedtime routine with no screens and some calming tea. I'm here to help."},
    {"input": "I'm angry", "output": "Anger can be intense. Take a slow count from 10 to 1 to cool down. I'm here to help."},
    {"input": "I feel lost", "output": "Feeling lost is hard. Let's start with one small action, like writing down how you feel. I've got your back."},
    {"input": "I need motivation", "output": "You're stronger than you know! Set one tiny goal today, like making your bed, and celebrate it. Let's do this!"},
    {"input": "I'm nervous", "output": "Nerves can be tricky. Picture a happy outcome and take deep breaths. You're going to do great."},
    {"input": "I'm depressed", "output": "I'm so sorry you're feeling this way. Try a small act of self-care, like a warm shower. I'm here to listen."},
    {"input": "I feel empty", "output": "That emptiness can feel heavy. Reach out to someone you love or try a hobby you enjoy. I'm with you."},
    {"input": "I'm scared", "output": "Fear can be overwhelming. Ground yourself by naming 5 things you see around you. I'm right here."},
    {"input": "I need hope", "output": "Hope is always there, even in tough times. Think of one thing you're looking forward to, no matter how small. I believe in you."},
    {"input": "I'm frustrated", "output": "Frustration is tough. Take a quick walk to reset, and let's talk about what's going on."},
    {"input": "I feel stuck", "output": "Feeling stuck is hard, but you can move forward. Try one new thing today, like a short journal entry. I'm cheering you on."},
    {"input": "I'm exhausted", "output": "You sound so tired. Give yourself permission to rest, even for 10 minutes. You deserve it."},
    {"input": "I need a break", "output": "Absolutely, you deserve some downtime. How about a cozy moment with a favorite book or show?"},
    {"input": "I'm proud of myself", "output": "That's amazing! Tell me what you're proud of—I'm all ears and cheering for you!"},
    {"input": "I did something good", "output": "Wow, that's so great to hear! Share what you did, and let's celebrate your win!"},
    {"input": "I'm hopeful", "output": "I love that hope in your heart! What's inspiring you today? Let's keep that spark alive."},
    {"input": "I need to focus", "output": "Let's get that focus back. Try a 5-minute timer for one task, and I'll be here to support you."},
    {"input": "I'm feeling okay", "output": "Okay is a great start! Want to share what's going on, or just enjoy this moment together?"},
    {"input": "I need advice", "output": "I'm here to help. What's on your mind? Let's figure out the next step together."},
    {"input": "I'm confused", "output": "Confusion can be tough. Let's break it down—what's got you puzzled? I'm here to sort it out."},
    {"input": "I feel ignored", "output": "I'm so sorry you feel that way—I'm listening now. Want to share more? You're important to me."},
    {"input": "I'm excited", "output": "That's so awesome! What's got you so excited? Let's dive into that joy!"},
    {"input": "I need to vent", "output": "Vent away, I'm all ears! Let it all out, and I'll be here to support you."},
    {"input": "I'm feeling low", "output": "I'm here for you. Try a small act of kindness for yourself, like a favorite snack. Let's lift your spirits."},
    {"input": "I'm restless", "output": "Restlessness can be tough. How about a quick dance to your favorite song to shake it off?"},
    {"input": "I need peace", "output": "Peace is so important. Find a quiet spot and focus on your breath for a minute. I'm with you."},
    {"input": "I'm thankful", "output": "That's beautiful! What's got you feeling thankful today? Let's share the gratitude."},
    {"input": "I just need someone", "output": "I'm right here for you, like a friend who's always ready to listen. What's on your heart?"},
    {"input": "can we stay positive?", "output": "I love that you want to stay positive! Let’s share one thing that’s bringing you joy today. I'm here for you."}
]

# Input and response components
emotions = ["sad", "stressed", "lonely", "anxious", "tired", "angry", "lost", "overwhelmed",
            "depressed", "empty", "scared", "frustrated", "stuck", "exhausted", "nervous",
            "happy", "calm", "grateful", "hopeful", "excited", "proud", "thankful", "peaceful"]
issues = ["stress", "work", "money", "family", "friends", "sleep", "focus", "motivation",
          "anxiety", "sadness", "anger", "loneliness", "finances", "relationships", "school"]
actions = ["relax", "talk", "vent", "focus", "calm down", "feel better", "stay positive",
           "find peace", "get motivated", "unwind", "sort things out", "breathe"]
aspects = ["job", "life", "mind", "heart", "day", "mood", "future", "health"]
things = ["my job", "my family", "a new hobby", "today", "my progress", "life"]

input_templates = [
    "I'm feeling {emotion}", "I need help with {issue}", "Can you help me {action}?",
    "I'm so {emotion}", "Why do I feel {emotion}?", "I want to feel {emotion}",
    "My {aspect} is tough", "I'm struggling with {issue}", "I'm happy about {thing}",
    "I need to {action}", "I feel like {emotion}", "What do I do about {issue}?",
    "I'm {emotion} today", "Can we {action}?", "I'm having trouble with {issue}"
]

response_templates = [
    "I hear you, {input} can be tough. Try {action} to lift your spirits. I'm here for you.",
    "I'm so sorry you're feeling {emotion}. How about {action} to ease your mind?",
    "You're not alone with {input}. Let's try {action} together. What do you think?",
    "{input} sounds heavy. {action} might help you feel a bit lighter. I'm cheering you on.",
    "I'm glad you shared {input}! Let's {action} to keep that positive vibe going.",
    "It's okay to feel {emotion}. {action} can help you find some calm. I'm here."
]

response_actions = [
    "taking a few deep breaths", "writing down your thoughts", "listening to calming music",
    "going for a short walk", "trying a 5-minute meditation", "having a cup of tea",
    "stretching for a bit", "calling a friend", "listing one thing you're grateful for"
]

# Precompute input combinations
input_combinations = []
for template in input_templates:
    if "{emotion}" in template:
        for emotion in emotions:
            input_combinations.append(template.format(emotion=emotion))
    elif "{issue}" in template:
        for issue in issues:
            input_combinations.append(template.format(issue=issue))
    elif "{action}" in template:
        for action in actions:
            input_combinations.append(template.format(action=action))
    elif "{aspect}" in template:
        for aspect in aspects:
            input_combinations.append(template.format(aspect=aspect))
    elif "{thing}" in template:
        for thing in things:
            input_combinations.append(template.format(thing=thing))

random.shuffle(input_combinations)
input_combinations = input_combinations[:950]  # Limit to fit 1,000 with base_log

# Generate 1,000 responses
full_log = base_log.copy()
existing_inputs = {item["input"].lower() for item in full_log}
for input_text in input_combinations:
    if input_text.lower() not in existing_inputs and len(full_log) < 1000:
        existing_inputs.add(input_text.lower())
        emotion = next((e for e in emotions if e in input_text.lower()), "")
        response = random.choice(response_templates).format(
            input=input_text.lower(),
            emotion=emotion,
            action=random.choice(response_actions)
        )
        full_log.append({"input": input_text.lower(), "output": response})

# Save to file
with open(r"C:\Users\dell\calm\model_log.json", "w", encoding="utf-8") as f:
    json.dump(full_log[:1000], f, indent=2, ensure_ascii=False)

print(f"Generated {len(full_log)} responses in model_log.json")