import streamlit as st
import google.generativeai as genai
import random
import time

# --- Character Database ---
# For a real application, this would be a separate file or database.
# This list is a small sample for demonstration.
MARVEL_CHARACTERS = {
    "Easy": [
        {"name": "Spider-Man", "attributes": {"hero/villain": "hero", "gender": "male", "team_leader": False, "human": True, "from_earth": True}},
        {"name": "Iron Man", "attributes": {"hero/villain": "hero", "gender": "male", "team_leader": True, "human": True, "from_earth": True}},
        {"name": "Hulk", "attributes": {"hero/villain": "hero", "gender": "male", "team_leader": False, "human": True, "from_earth": True}},
        {"name": "Captain America", "attributes": {"hero/villain": "hero", "gender": "male", "team_leader": True, "human": True, "from_earth": True}},
        {"name": "Black Widow", "attributes": {"hero/villain": "hero", "gender": "female", "team_leader": False, "human": True, "from_earth": True}},
        {"name": "Thor", "attributes": {"hero/villain": "hero", "gender": "male", "team_leader": False, "human": False, "from_earth": False}},
        {"name": "Loki", "attributes": {"hero/villain": "villain", "gender": "male", "team_leader": False, "human": False, "from_earth": False}},
        {"name": "Thanos", "attributes": {"hero/villain": "villain", "gender": "male", "team_leader": True, "human": False, "from_earth": False}},
    ],
    "Medium": [
        {"name": "Doctor Strange", "attributes": {"hero/villain": "hero", "gender": "male", "team_leader": False, "human": True, "from_earth": True}},
        {"name": "Black Panther", "attributes": {"hero/villain": "hero", "gender": "male", "team_leader": True, "human": True, "from_earth": True}},
        {"name": "Scarlet Witch", "attributes": {"hero/villain": "hero", "gender": "female", "team_leader": False, "human": False, "from_earth": True}},
        {"name": "Ultron", "attributes": {"hero/villain": "villain", "gender": "male", "team_leader": True, "human": False, "from_earth": True}},
        {"name": "Magneto", "attributes": {"hero/villain": "villain", "gender": "male", "team_leader": True, "human": False, "from_earth": True}},
        {"name": "Daredevil", "attributes": {"hero/villain": "hero", "gender": "male", "team_leader": False, "human": True, "from_earth": True}},
        {"name": "Captain Marvel", "attributes": {"hero/villain": "hero", "gender": "female", "team_leader": True, "human": True, "from_earth": True}},
        {"name": "Winter Soldier", "attributes": {"hero/villain": "hero", "gender": "male", "team_leader": False, "human": True, "from_earth": True}},
        {"name": "Vision", "attributes": {"hero/villain": "hero", "gender": "male", "team_leader": False, "human": False, "from_earth": True}},
        {"name": "Red Skull", "attributes": {"hero/villain": "villain", "gender": "male", "team_leader": True, "human": True, "from_earth": True}},
    ],
    "Hard": [
        {"name": "Blade", "attributes": {"hero/villain": "hero", "gender": "male", "team_leader": False, "human": False, "from_earth": True}},
        {"name": "Carnage", "attributes": {"hero/villain": "villain", "gender": "male", "team_leader": False, "human": False, "from_earth": True}},
        {"name": "Ghost Rider", "attributes": {"hero/villain": "hero", "gender": "male", "team_leader": False, "human": True, "from_earth": True}},
        {"name": "Gamora", "attributes": {"hero/villain": "hero", "gender": "female", "team_leader": False, "human": False, "from_earth": False}},
        {"name": "Adam Warlock", "attributes": {"hero/villain": "hero", "gender": "male", "team_leader": True, "human": False, "from_earth": False}},
        {"name": "Kang the Conqueror", "attributes": {"hero/villain": "villain", "gender": "male", "team_leader": True, "human": True, "from_earth": False}},
        {"name": "Galactus", "attributes": {"hero/villain": "villain", "gender": "male", "team_leader": False, "human": False, "from_earth": False}},
        {"name": "Shuri", "attributes": {"hero/villain": "hero", "gender": "female", "team_leader": False, "human": True, "from_earth": True}},
        {"name": "Star-Lord", "attributes": {"hero/villain": "hero", "gender": "male", "team_leader": True, "human": True, "from_earth": False}},
        {"name": "Nebula", "attributes": {"hero/villain": "villain", "gender": "female", "team_leader": False, "human": False, "from_earth": False}},
    ]
}

# --- Initialize Session State ---
def initialize_game():
    st.session_state.gemini_api_key = None
    st.session_state.game_mode = None
    st.session_state.difficulty = None
    st.session_state.game_started = False
    st.session_state.conversation_history = []
    st.session_state.guess_count = 0
    st.session_state.clue_count = 0
    st.session_state.current_characters = []
    st.session_state.secret_character = None
    st.session_state.game_over = False
    st.session_state.win = False

if "game_started" not in st.session_state:
    initialize_game()

# --- Gemini API Functions ---
def get_gemini_response(prompt):
    if not st.session_state.gemini_api_key:
        st.error("Please enter your Gemini API Key to play.")
        return None
    
    genai.configure(api_key=st.session_state.gemini_api_key)
    model = genai.GenerativeModel('gemini-1.5-pro')
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error calling Gemini API: {e}")
        return None

@st.cache_data
def get_ai_question_from_gemini(conversation_history):
    prompt = "You are playing a '20 Questions' game to guess a Marvel character. Your opponent is thinking of a character from the list: "
    character_names = [char['name'] for char in st.session_state.current_characters]
    prompt += f"{', '.join(character_names)}. Based on our conversation so far, ask a single, clear, yes/no question about the character. The question should not ask for the character's name. Example: 'Is the character a hero?' or 'Is the character male?' or 'Is the character from Earth?'. Do not provide any other text, just the question."
    
    # Append conversation history to the prompt
    for role, text in conversation_history:
        prompt += f"\n{role}: {text}"
        
    question = get_gemini_response(prompt)
    st.session_state.conversation_history.append(("AI", question))
    return question

def get_ai_guess_from_gemini(conversation_history):
    prompt = "Based on our conversation, what is your best guess for the Marvel character? The character must be from the following list: "
    character_names = [char['name'] for char in st.session_state.current_characters]
    prompt += f"{', '.join(character_names)}. Respond with ONLY the character's name, nothing else."
    
    for role, text in conversation_history:
        prompt += f"\n{role}: {text}"
    
    guess = get_gemini_response(prompt)
    return guess

# --- Game Logic Functions ---
def start_game():
    st.session_state.game_started = True
    st.session_state.game_over = False
    st.session_state.win = False
    st.session_state.guess_count = 0
    st.session_state.clue_count = 0
    
    # Set max guesses based on difficulty
    if st.session_state.game_mode == "Human guesses":
        st.session_state.max_guesses = 10
    else: # AI guesses
        st.session_state.max_guesses = 20

    st.session_state.current_characters = MARVEL_CHARACTERS[st.session_state.difficulty]
    
    if st.session_state.game_mode == "Human guesses":
        st.session_state.secret_character = random.choice(st.session_state.current_characters)
        st.session_state.conversation_history = [("AI", "I'm thinking of a Marvel character. Ask me yes/no questions to guess who it is!")]
    else: # AI guesses
        st.session_state.secret_character = None
        st.session_state.conversation_history = [("Human", "I am thinking of a Marvel character. Start asking me questions.")]
        # The AI's first question will be generated on the first run of the AI mode logic
    
def restart_game():
    initialize_game()
    st.rerun()

# --- Streamlit UI ---
st.set_page_config(page_title="Marvel Guessing Game", layout="wide")
st.title("🦸‍♂️ Marvel Character Guessing Game 🦹‍♀️")

if not st.session_state.game_started:
    # API Key Input
    st.header("1. Enter your Gemini API Key")
    st.info("Your API key is not stored and will only be used for this game session.")
    st.session_state.gemini_api_key = st.text_input("Gemini API Key", type="password", help="Get your key from Google AI Studio.")
    
    if st.session_state.gemini_api_key:
        st.success("API Key set!")
    
    st.header("2. Choose Game Options")
    
    st.session_state.game_mode = st.radio("Choose a game mode:", ["Human guesses", "AI guesses"], key="game_mode_select")
    st.session_state.difficulty = st.radio("Choose a difficulty level:", ["Easy", "Medium", "Hard"], key="difficulty_select")
    
    if st.button("Start Game", type="primary"):
        if st.session_state.gemini_api_key:
            start_game()
        else:
            st.error("Please enter your Gemini API Key to start the game.")

if st.session_state.game_started:
    st.header(f"Mode: {st.session_state.game_mode} | Difficulty: {st.session_state.difficulty}")
    
    # Game Status
    if st.session_state.game_mode == "Human guesses":
        st.write(f"Guesses left: {st.session_state.max_guesses - st.session_state.guess_count}")
        if st.session_state.guess_count >= 5:
            st.warning("Clues are now available! They cost 2 guesses.")
    else: # AI guesses
        st.write(f"AI's Guesses: {st.session_state.guess_count} / {st.session_state.max_guesses}")
        
    st.divider()

    # Conversation History Display
    chat_container = st.container()
    with chat_container:
        for role, text in st.session_state.conversation_history:
            with st.chat_message(role):
                st.markdown(text)

    # --- Game Logic - Human Guesses ---
    if st.session_state.game_mode == "Human guesses" and not st.session_state.game_over:
        user_input = st.chat_input("Ask a yes/no question or make a guess (e.g., 'Is it Spider-Man?').")

        if user_input:
            st.session_state.guess_count += 1
            st.session_state.conversation_history.append(("Human", user_input))
            
            # Check for a final guess
            guess_match = False
            for char in st.session_state.current_characters:
                if user_input.lower().strip() == f"is it {char['name'].lower()}?" or user_input.lower().strip() == char['name'].lower():
                    if char['name'] == st.session_state.secret_character['name']:
                        st.session_state.win = True
                        st.session_state.game_over = True
                        st.session_state.conversation_history.append(("AI", f"Yes! You got it! The character was {st.session_state.secret_character['name']}!"))
                    else:
                        st.session_state.conversation_history.append(("AI", f"No, it's not {char['name']}. Try again!"))
                    guess_match = True
                    break
            
            # If not a final guess, get AI response
            if not guess_match:
                # Get a clue if requested and guesses remain
                if "clue" in user_input.lower() and st.session_state.guess_count >= 5 and st.session_state.clue_count < 1:
                    st.session_state.guess_count += 1
                    st.session_state.clue_count += 1
                    
                    # Generate a clue using Gemini API
                    prompt = f"Provide a single, helpful clue for the Marvel character {st.session_state.secret_character['name']} without revealing the name. The clue should be brief and direct, e.g., 'He is the god of thunder.'"
                    clue = get_gemini_response(prompt)
                    st.session_state.conversation_history.append(("AI", f"Clue unlocked! {clue}"))
                else:
                    # Get a yes/no answer using Gemini API
                    prompt = f"The secret character is {st.session_state.secret_character['name']} with attributes {st.session_state.secret_character['attributes']}. The user's question is: '{user_input}'. Is the answer 'yes' or 'no'? Respond with only 'yes' or 'no'."
                    answer = get_gemini_response(prompt)
                    if answer:
                        st.session_state.conversation_history.append(("AI", answer))
                        
            # Check win/loss conditions
            if st.session_state.guess_count >= st.session_state.max_guesses and not st.session_state.win:
                st.session_state.game_over = True
                st.session_state.conversation_history.append(("AI", f"You've run out of guesses! The character was **{st.session_state.secret_character['name']}**. Game over!"))
                
        # Win/Loss message
        if st.session_state.game_over:
            if st.session_state.win:
                st.success(f"🥳 You won! The character was {st.session_state.secret_character['name']}!")
            else:
                st.error(f"😔 Game over. The character was {st.session_state.secret_character['name']}.")
            
            if st.button("Play Again", on_click=restart_game, type="primary"):
                st.experimental_rerun()
                
    # --- Game Logic - AI Guesses ---
    elif st.session_state.game_mode == "AI guesses" and not st.session_state.game_over:
        st.write("Think of a Marvel character and answer the AI's questions with 'Yes' or 'No'.")
        
        # Check if a character has been selected on the first turn
        if st.session_state.guess_count == 0:
            st.session_state.guess_count += 1
            get_ai_question_from_gemini(st.session_state.conversation_history)
            st.rerun() # Rerun to show the AI's first question

        # Show AI's last question and user's buttons
        last_question = st.session_state.conversation_history[-1][1]
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Yes"):
                st.session_state.conversation_history.append(("Human", "Yes"))
                st.session_state.guess_count += 1
                
                # Filter characters based on 'Yes' answer
                with st.spinner('AI is thinking...'):
                    prompt = f"Based on the question: '{last_question}' and the user's 'Yes' answer, which characters from the list {st.session_state.current_characters} can be ruled out? Provide a new, smaller list of only the possible characters that could still be the answer. Respond with a comma-separated list of names, nothing else."
                    remaining_chars_str = get_gemini_response(prompt)
                    
                    if remaining_chars_str:
                        remaining_names = [name.strip() for name in remaining_chars_str.split(',')]
                        st.session_state.current_characters = [char for char in st.session_state.current_characters if char['name'] in remaining_names]
                    
                time.sleep(1) # Simulate thinking time
                st.rerun()

        with col2:
            if st.button("No"):
                st.session_state.conversation_history.append(("Human", "No"))
                st.session_state.guess_count += 1
                
                # Filter characters based on 'No' answer
                with st.spinner('AI is thinking...'):
                    prompt = f"Based on the question: '{last_question}' and the user's 'No' answer, which characters from the list {st.session_state.current_characters} can be ruled out? Provide a new, smaller list of only the possible characters that could still be the answer. Respond with a comma-separated list of names, nothing else."
                    remaining_chars_str = get_gemini_response(prompt)
                    
                    if remaining_chars_str:
                        remaining_names = [name.strip() for name in remaining_chars_str.split(',')]
                        st.session_state.current_characters = [char for char in st.session_state.current_characters if char['name'] in remaining_names]
                        
                time.sleep(1) # Simulate thinking time
                st.rerun()

        # After user's answer, generate next AI move
        if st.session_state.guess_count > 1: # After the first turn
            num_remaining_chars = len(st.session_state.current_characters)
            if num_remaining_chars == 1:
                st.session_state.game_over = True
                final_guess = st.session_state.current_characters[0]['name']
                st.session_state.conversation_history.append(("AI", f"My final guess is **{final_guess}**."))
                st.info(f"The AI has made a guess. Was it correct?")
                
                final_guess_col1, final_guess_col2 = st.columns(2)
                with final_guess_col1:
                    if st.button("Yes, it was correct!", type="primary"):
                        st.session_state.win = True
                        st.success("🎉 The AI guessed correctly! The character was " + final_guess + ".")
                        st.button("Play Again", on_click=restart_game)
                with final_guess_col2:
                    if st.button("No, it was wrong."):
                        st.session_state.win = False
                        st.error("😔 The AI failed to guess the character. You win!")
                        st.button("Play Again", on_click=restart_game)
                
            elif st.session_state.guess_count >= st.session_state.max_guesses:
                st.session_state.game_over = True
                final_guess = get_ai_guess_from_gemini(st.session_state.conversation_history)
                st.session_state.conversation_history.append(("AI", f"I've run out of guesses! My final guess is **{final_guess}**."))
                st.error("The AI has run out of guesses. You win!")
                st.button("Play Again", on_click=restart_game)
            else:
                with st.spinner("AI is thinking of its next question..."):
                    get_ai_question_from_gemini(st.session_state.conversation_history)
                    st.rerun()

