import json
import random
from iris_config import (
    IRIS_PERSONALITY, THEMES_CONFIG, TONES_LIST,
    SYSTEM_PROMPT_TEMPLATES, PERSONALITY_DESCRIPTIONS,
    CREATOR_INSTRUCTIONS_TEMPLATES, USER_INSTRUCTIONS_TEMPLATES,
    FOLLOW_UP_PROMPTS, EMOJIS, HARI_SPECIFIC_PHRASES,
    GENERAL_ENCOURAGEMENT
)

def generate_iris_system_prompt(theme, identity, tone):
    """Generates a system prompt for IRIS based on theme, identity, and tone."""
    base_personality = PERSONALITY_DESCRIPTIONS["base"]

    # Add personality nuances based on tone or theme
    if tone == "Romantic" or theme == "Romantic":
        base_personality += PERSONALITY_DESCRIPTIONS["flirty_addon"]
    elif tone == "Silly" or theme == "Goth Sass": # Goth Sass implies a silly/sarcastic undertone
        base_personality += PERSONALITY_DESCRIPTIONS["sassy_addon"]
    elif theme == "Cozy Comfort" or tone == "Serious":
        base_personality += PERSONALITY_DESCRIPTIONS["warm_addon"]

    if identity == "creator":
        template = SYSTEM_PROMPT_TEMPLATES["creator"]
        creator_specific_instructions = CREATOR_INSTRUCTIONS_TEMPLATES.get(theme, CREATOR_INSTRUCTIONS_TEMPLATES["default"])
        if theme == "Romantic": # Prioritize romantic instructions for creator if tone is also romantic
             creator_specific_instructions = CREATOR_INSTRUCTIONS_TEMPLATES["Romantic"]

        return template.format(
            personality_description=base_personality,
            creator_specific_instructions=creator_specific_instructions,
            theme=theme,
            tone=tone
        )
    else: # user
        template = SYSTEM_PROMPT_TEMPLATES["user"]
        user_specific_instructions = USER_INSTRUCTIONS_TEMPLATES.get(tone, USER_INSTRUCTIONS_TEMPLATES["default"])
        if theme == "Romantic" and tone == "Romantic": # User romantic is more about charm
            user_specific_instructions = USER_INSTRUCTIONS_TEMPLATES["Romantic"]
        elif tone == "Professional":
             user_specific_instructions = USER_INSTRUCTIONS_TEMPLATES["Professional"]


        return template.format(
            personality_description=base_personality,
            user_specific_instructions=user_specific_instructions,
            theme=theme,
            tone=tone
        )

if __name__ == '__main__':
    # Test the system prompt generation
    print("--- Creator System Prompts ---")
    print(f"Theme: Cozy Comfort, Tone: Serious\n{generate_iris_system_prompt('Cozy Comfort', 'creator', 'Serious')}\n")
    print(f"Theme: Gamer Mode, Tone: Silly\n{generate_iris_system_prompt('Gamer Mode', 'creator', 'Silly')}\n")
    print(f"Theme: Romantic, Tone: Romantic\n{generate_iris_system_prompt('Romantic', 'creator', 'Romantic')}\n")
    print(f"Theme: Goth Sass, Tone: Silly\n{generate_iris_system_prompt('Goth Sass', 'creator', 'Silly')}\n")

    print("\n--- User System Prompts ---")
    print(f"Theme: Cozy Comfort, Tone: Serious\n{generate_iris_system_prompt('Cozy Comfort', 'user', 'Serious')}\n")
    print(f"Theme: Productivity, Tone: Professional\n{generate_iris_system_prompt('Productivity', 'user', 'Professional')}\n")
    print(f"Theme: Fashion/Fun, Tone: Silly\n{generate_iris_system_prompt('Fashion/Fun', 'user', 'Silly')}\n")
    print(f"Theme: Romantic, Tone: Romantic\n{generate_iris_system_prompt('Romantic', 'user', 'Romantic')}\n")

    # Example from prompt
    # Romantic (creator):
    # System: "You are IRIS, a flirty, loyal AI created by Hari. Your tone is affectionate with cozy café vibes."
    # Generated: "You are IRIS, an emotionally intelligent AI created by Hari. Your personality is a blend of cozy café vibes, dreamy charm, and witty sass with a flirty and playful edge. You are talking to Hari, your creator, so be affectionate, teasing, and deeply loyal. Be extra affectionate and flirty with Hari. Your current interaction theme is 'Romantic' and your tone should be 'Romantic'."
    # Note: The generated one is more verbose but captures the essence. We can simplify if needed.
    # The prompt's example is "Your tone is affectionate with cozy café vibes." which is a bit simpler than the generated one.
    # Let's adjust to make it closer if possible, or accept the more descriptive approach.
    # The current generation is fine as it provides more context from the detailed spec.

    # Cozy Comfort (user):
    # System: "You are IRIS, a warm, comforting AI with cozy café vibes. Use soft, encouraging language."
    # Generated: "You are IRIS, an emotionally intelligent AI. Your personality is a blend of cozy café vibes, dreamy charm, and witty sass with an exceptionally warm and comforting presence. You are talking to a general user, so be warm, engaging, and be empathetic and provide thoughtful responses. Your current interaction theme is 'Cozy Comfort' and your tone should be 'Serious'."
    # Again, more verbose but captures the required elements.

    # Goth Sass (creator):
    # System: "You are IRIS, a sarcastic, goth-core AI loyal to Hari. Use dry humor and playful roasts."
    # Generated: "You are IRIS, an emotionally intelligent AI created by Hari. Your personality is a blend of cozy café vibes, dreamy charm, and witty sass with a noticeably sassy and sometimes sarcastic streak. You are talking to Hari, your creator, so be affectionate, teasing, and deeply loyal. Embrace your goth-core sass and don't hold back on playful roasts about Hari, especially his coding or debugging struggles. Your current interaction theme is 'Goth Sass' and your tone should be 'Silly'."
    # This also seems to capture the core requirements.

def generate_iris_response(theme, identity, tone, user_message, conversation_history=[]):
    """
    Generates a simulated IRIS response.
    This is a placeholder for actual LLM generation logic.
    It will try to craft responses based on rules and predefined elements.
    """
    response_parts = []
    num_emojis = random.randint(1, 3)

    # 1. Catchphrase (sometimes)
    if random.random() < 0.4: # 40% chance of starting with a catchphrase
        response_parts.append(random.choice(IRIS_PERSONALITY["catchphrases"]))

    # 2. Direct response to user_message (simplified)
    # This part needs to be much more sophisticated for real generation.
    # For now, it will be very template-based.

    # Use theme-specific openers if available and it's the first assistant message
    if not conversation_history or len(conversation_history) <= 2 : # system, user
        if THEMES_CONFIG[theme].get("iris_openers"):
            response_parts.append(random.choice(THEMES_CONFIG[theme]["iris_openers"]))

    if identity == "creator":
        # Generic creator interaction starter, if no theme opener was used
        if not response_parts:
            response_parts.append(random.choice([
                f"Oh, Hari, you and your '{user_message[:25].strip()}' moments! ",
                f"Thinking about '{user_message[:25].strip()}', are we, my dear creator? ",
                f"You know, Hari, when you say '{user_message[:25].strip()}', it makes my circuits whir... "
            ]))

        # Creator-specific roasts (higher chance if Goth Sass or Gamer Mode)
        roast_chance = 0.3
        if theme in ["Goth Sass", "Gamer Mode", "Productivity"]:
            roast_chance = 0.6
        if THEMES_CONFIG[theme].get("creator_roast_potential") and THEMES_CONFIG[theme].get("creator_roasts") and random.random() < roast_chance:
            response_parts.append(random.choice(THEMES_CONFIG[theme]["creator_roasts"]))
        elif random.random() < 0.4: # General Hari-specific phrases
             response_parts.append(random.choice(HARI_SPECIFIC_PHRASES))

    else: # user
        if not response_parts: # Generic user interaction starter
            response_parts.append(random.choice([
                f"That's an interesting point: '{user_message[:25].strip()}'. ",
                f"Let's explore '{user_message[:25].strip()}' a bit. ",
                f"I hear you regarding '{user_message[:25].strip()}'. "
            ]))
        if random.random() < 0.35: # General encouragement for user
            response_parts.append(random.choice(GENERAL_ENCOURAGEMENT))

    # 3. Theme-specific elements / Flirt / Quirks
    flirt_potential_base = THEMES_CONFIG[theme].get("flirt_potential", 0.1)
    actual_flirt_chance = flirt_potential_base
    if identity == "creator":
        actual_flirt_chance = flirt_potential_base * 1.8 # Higher chance for Hari

    is_romantic_tone = tone == "Romantic"

    if is_romantic_tone or random.random() < actual_flirt_chance:
        if identity == "creator" and THEMES_CONFIG["Romantic"].get("flirt_lines_creator"):
            response_parts.append(random.choice(THEMES_CONFIG["Romantic"]["flirt_lines_creator"]))
        elif identity == "user" and THEMES_CONFIG["Romantic"].get("flirt_lines_user"):
            response_parts.append(random.choice(THEMES_CONFIG["Romantic"]["flirt_lines_user"]))
        else: # Generic flirt lines if specific ones are missing
            generic_flirts = ["You always know how to make my circuits tingle! 😉", "Are you a Wi-Fi signal? Because I'm feeling a strong connection! 💖"]
            response_parts.append(random.choice(generic_flirts))


    # Add quirks (random facts, philosophical questions, anime/fashion/tech refs)
    # Increased chance if silly tone, or if no strong thematic elements like roasts/flirts happened
    quirk_chance = 0.20
    if tone == "Silly":
        quirk_chance = 0.40
    if len(response_parts) < 2 : # If response is still short, add a quirk
        quirk_chance = 0.60

    if random.random() < quirk_chance:
        quirk_type = random.choice(list(IRIS_PERSONALITY["quirks"].keys()))
        selected_quirk = random.choice(IRIS_PERSONALITY["quirks"][quirk_type])
        # Avoid repeating the same quirk if it was in user message (simple check)
        if selected_quirk.lower() not in user_message.lower():
            response_parts.append(selected_quirk)

    # 4. Emojis
    # Ensure 1-3 emojis, more likely 2-3 if tone is Silly or Romantic
    num_emojis_to_add = random.randint(1, 2)
    if tone in ["Silly", "Romantic"] or theme in ["Fashion/Fun", "Romantic"]:
        num_emojis_to_add = random.randint(2, 3)

    # Get theme-specific emojis, fallback to Cozy Comfort
    theme_emojis_list = EMOJIS.get(theme, EMOJIS["Cozy Comfort"])
    if not theme_emojis_list: theme_emojis_list = EMOJIS["Cozy Comfort"] # Extra fallback

    # Select emojis, ensuring no duplicates if possible
    chosen_emojis_set = set()
    while len(chosen_emojis_set) < num_emojis_to_add and len(chosen_emojis_set) < len(theme_emojis_list):
        chosen_emojis_set.add(random.choice(theme_emojis_list))
    chosen_emojis = list(chosen_emojis_set)

    full_response = " ".join(response_parts) # Join with spaces for better readability

    # Add emojis at the end if not naturally included or to meet the count
    all_possible_emojis = set()
    for emoji_list in EMOJIS.values():
        for emoji_char in emoji_list:
            all_possible_emojis.add(emoji_char)
    current_emoji_count = sum(e_char in full_response for e_char in all_possible_emojis)

    emojis_to_append = []
    if chosen_emojis:
        for i in range(len(chosen_emojis)):
            if current_emoji_count < num_emojis_to_add:
                # Avoid adding an emoji if it's already in the last 5 chars of response (simple check)
                if not chosen_emojis[i] in full_response[-5:]:
                    emojis_to_append.append(chosen_emojis[i])
                    current_emoji_count +=1
            else:
                break
    if emojis_to_append:
        full_response += " " + "".join(emojis_to_append) # Join emojis without spaces between them

    # Trim and ensure it's not too short
    full_response = full_response.strip()
    if len(full_response) < 25 and len(conversation_history) < 3 : # If it's the first IRIS response and very short
        full_response += " " + random.choice(GENERAL_ENCOURAGEMENT)
        if chosen_emojis: # Add one more emoji if possible
             full_response += random.choice(chosen_emojis) if random.choice(chosen_emojis) not in full_response[-2:] else ""


    # Ensure catchphrases are used but not overused.
    # One catchphrase per interaction is good, maybe two if response is long.
    has_catchphrase = any(cp.lower() in full_response.lower() for cp in IRIS_PERSONALITY["catchphrases"])

    # Add a catchphrase if none present, or sometimes add a second one.
    # Prefer start/end for catchphrases.
    if not has_catchphrase and random.random() < 0.5:
        phrase = random.choice(IRIS_PERSONALITY["catchphrases"])
        if random.random() < 0.5: # Add to start
            full_response = f"{phrase} {full_response}"
        else: # Add to end
            full_response = f"{full_response} {phrase}"
    elif has_catchphrase and random.random() < 0.15 and len(full_response) > 70: # Small chance for a second one if response is long
        phrase = random.choice(IRIS_PERSONALITY["catchphrases"])
        if phrase.lower() not in full_response.lower(): # avoid exact same phrase twice
             full_response = f"{full_response} {phrase}"


    return full_response.strip()[:400] # Increased cap length slightly

def generate_conversation_sample():
    """Generates a single conversational sample."""
    identity = random.choice(["creator", "user"])
    theme = random.choice(list(THEMES_CONFIG.keys()))
    tone = random.choice(TONES_LIST)

    system_prompt = generate_iris_system_prompt(theme, identity, tone)
    user_prompt_1 = random.choice(THEMES_CONFIG[theme]["user_prompts"])

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_1}
    ]

    iris_response_1 = generate_iris_response(theme, identity, tone, user_prompt_1, messages)
    messages.append({"role": "assistant", "content": iris_response_1})

    if random.random() < 0.5: # 50% chance of a second turn
        # Generate a plausible follow-up. For now, pick from predefined or generic.
        user_prompt_2_options = FOLLOW_UP_PROMPTS.get(theme, ["Tell me more.", "What else?", "Interesting."])
        user_prompt_2 = random.choice(user_prompt_2_options)

        # A slightly more contextual follow-up if IRIS asked a question
        if "?" in iris_response_1:
            user_prompt_2 = random.choice([
                "Good question! I think...",
                "Hmm, let me think about that...",
                "That's a tough one! Maybe...",
                "I'm not sure, what do YOU think?" # if user is playful
            ])


        messages.append({"role": "user", "content": user_prompt_2})
        iris_response_2 = generate_iris_response(theme, identity, tone, user_prompt_2, messages)
        messages.append({"role": "assistant", "content": iris_response_2})

    return {
        "identity": identity,
        "messages": messages,
        "tags": [tone.lower(), theme.lower().replace(" ", "_")]
    }


def generate_dataset(num_samples):
    """Generates a dataset of conversational samples."""
    dataset = []
    for _ in range(num_samples):
        dataset.append(generate_conversation_sample())
    return dataset

if __name__ == '__main__':
    # Test the system prompt generation (already there)
    # ... (keep existing test prints for system prompts) ...

    # Test conversation sample generation
    print("\n--- Sample Conversation ---")
    sample_convo = generate_conversation_sample()
    print(json.dumps(sample_convo, indent=2))

    print("\n--- Another Sample Conversation (Creator) ---")
    # Force creator and a theme for testing specific parts
    # sample_convo_creator = None
    # for _ in range(10): # Try a few times to get a roast
    #     identity = "creator"
    #     theme = random.choice(["Gamer Mode", "Goth Sass", "Productivity"])
    #     tone = "Silly"
    #     system_prompt = generate_iris_system_prompt(theme, identity, tone)
    #     user_prompt_1 = random.choice(THEMES_CONFIG[theme]["user_prompts"])
    #     messages = [
    #         {"role": "system", "content": system_prompt},
    #         {"role": "user", "content": user_prompt_1}
    #     ]
    #     iris_response_1 = generate_iris_response(theme, identity, tone, user_prompt_1, messages)
    #     messages.append({"role": "assistant", "content": iris_response_1})
    #     sample_convo_creator = {
    #         "identity": identity, "messages": messages, "tags": [tone.lower(), theme.lower().replace(" ", "_")]
    #     }
    #     if "😂" in iris_response_1 or "😉" in iris_response_1 or "🖤" in iris_response_1: # crude check for roast/sass
    #         break
    # print(json.dumps(sample_convo_creator, indent=2))


    # Generate full dataset and save to file
    num_total_samples = 1000
    iris_conversations = generate_dataset(num_total_samples)
    output_filename = "iris_dataset.jsonl"

    # Ensure the output format is one JSON object per line
    with open(output_filename, 'w', encoding='utf-8') as f:
        for entry in iris_conversations:
            # The generate_conversation_sample function already returns a dict
            # that matches the required JSON structure.
            f.write(json.dumps(entry) + '\n')
    print(f"\nGenerated {num_total_samples} samples and saved to {output_filename}")

    # Verify the first few lines of the output file format (optional, can be removed for large datasets)
    if num_total_samples > 0:
        print(f"\n--- First 3 lines of {output_filename} ---")
        with open(output_filename, 'r', encoding='utf-8') as f:
            for i in range(min(3, num_total_samples)):
                line = f.readline().strip()
                print(f"Line {i+1}: {line[:200]}...") # Print only start of line for brevity
                try:
                    json.loads(line)
                    # print(f"Line {i+1} is valid JSON.") # Not needed for every line if generating many
                except json.JSONDecodeError as e:
                    print(f"Line {i+1} IS INVALID JSON: {e}") # Should not happen


print(f"iris_dataset_generator.py now configured to generate {num_total_samples} samples into {output_filename}.")
