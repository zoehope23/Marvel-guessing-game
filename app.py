import streamlit as st
import random

# Use st.session_state to persist data across reruns
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'game_mode' not in st.session_state:
    st.session_state.game_mode = 'user_guesses'
if 'secret_character' not in st.session_state:
    st.session_state.secret_character = None
if 'user_tries' not in st.session_state:
    st.session_state.user_tries = 0
if 'computer_tries' not in st.session_state:
    st.session_state.computer_tries = 0
if 'user_hints' not in st.session_state:
    st.session_state.user_hints = []
if 'computer_guess' not in st.session_state:
    st.session_state.computer_guess = None
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'available_characters' not in st.session_state:
    st.session_state.available_characters = []
if 'question_index' not in st.session_state:
    st.session_state.question_index = 0
if 'question_list' not in st.session_state:
    st.session_state.question_list = []
if 'last_answer' not in st.session_state:
    st.session_state.last_answer = None


# A dictionary of Marvel characters and their attributes for the game
# The computer will use these attributes for its hints and guesses.
marvel_characters = {
    "Iron Man": {
        "powers": ["Genius-level intellect", "Powered armor", "Flight", "Energy projection"],
        "affiliation": "Avengers",
        "gender": "Male",
        "hint1": "This character is a brilliant inventor and billionaire.",
        "hint2": "His alias comes from the suit of armor he built.",
        "hint3": "He is a founding member of the Avengers.",
        "hint4": "His name is Tony Stark."
    },
    "Captain America": {
        "powers": ["Super-soldier serum", "Peak human strength", "Indestructible shield"],
        "affiliation": "Avengers",
        "gender": "Male",
        "hint1": "He is a super-soldier from World War II.",
        "hint2": "He wields an indestructible shield made of vibranium.",
        "hint3": "He is a symbol of justice and freedom.",
        "hint4": "His name is Steve Rogers."
    },
    "Spider-Man": {
        "powers": ["Superhuman strength", "Web-shooting", "Wall-crawling", "Spider-Sense"],
        "affiliation": "Solo hero",
        "gender": "Male",
        "hint1": "He was bitten by a radioactive spider.",
        "hint2": "He has the proportional strength of a spider and can shoot webs.",
        "hint3": "He lives in New York City and is often a target for the Daily Bugle.",
        "hint4": "His name is Peter Parker."
    },
    "Thor": {
        "powers": ["God of Thunder", "Superhuman strength", "Control over lightning", "Mjolnir"],
        "affiliation": "Avengers",
        "gender": "Male",
        "hint1": "He is a god from a mythological realm.",
        "hint2": "He wields a powerful enchanted hammer.",
        "hint3": "He is the God of Thunder.",
        "hint4": "His name is Thor Odinson."
    },
    "Black Widow": {
        "powers": ["Master spy", "Expert martial artist", "Peak human physical condition"],
        "affiliation": "Avengers",
        "gender": "Female",
        "hint1": "She is a highly trained spy and assassin.",
        "hint2": "Her main weapons are her martial arts skills and 'Widow's Bite' gauntlets.",
        "hint3": "She's a founding member of the Avengers, but has no superhuman powers.",
        "hint4": "Her name is Natasha Romanoff."
    },
    "Hulk": {
        "powers": ["Incredible strength", "Healing factor", "Invulnerability"],
        "affiliation": "Avengers",
        "gender": "Male",
        "hint1": "He is a scientist who was exposed to gamma radiation.",
        "hint2": "He becomes a giant green rage monster when angry.",
        "hint3": "He's the strongest one there is.",
        "hint4": "His name is Bruce Banner."
    }
}

def generate_questions():
    """Generates a list of all possible yes/no questions based on character attributes."""
    questions = []
    # Collect all unique affiliations, genders, and powers
    all_affiliations = set(char['affiliation'] for char in marvel_characters.values())
    all_genders = set(char['gender'] for char in marvel_characters.values())
    all_powers = set(power for char in marvel_characters.values() for power in char['powers'])

    for affiliation in all_affiliations:
        questions.append({"type": "affiliation", "value": affiliation, "text": f"Is your character part of the **{affiliation}**?"})
    for gender in all_genders:
        questions.append({"type": "gender", "value": gender, "text": f"Is your character **{gender}**?"})
    for power in all_powers:
        questions.append({"type": "powers", "value": power, "text": f"Does your character have the power of **{power}**?"})

    random.shuffle(questions)
    return questions

def start_new_game():
    """Resets the game state and picks a new character."""
    st.session_state.game_started = True
    st.session_state.game_over = False
    st.session_state.user_tries = 0
    st.session_state.computer_tries = 0
    st.session_state.user_hints = []
    st.session_state.computer_guess = None
    st.session_state.secret_character = random.choice(list(marvel_characters.keys()))
    
    # Reset state for the computer guessing mode
    st.session_state.available_characters = list(marvel_characters.keys())
    st.session_state.question_index = 0
    st.session_state.question_list = generate_questions()
    st.session_state.last_answer = None
    
    st.success(f"New game started! You are in **'{st.session_state.game_mode.replace('_', ' ').capitalize()}'** mode. Good luck!")

def reset_game():
    """Resets the entire app state."""
    st.session_state.game_started = False
    st.session_state.game_over = False
    st.session_state.user_tries = 0
    st.session_state.computer_tries = 0
    st.session_state.user_hints = []
    st.session_state.computer_guess = None
    st.session_state.secret_character = None
    st.session_state.game_mode = 'user_guesses'
    
    st.session_state.available_characters = []
    st.session_state.question_index = 0
    st.session_state.question_list = []
    st.session_state.last_answer = None

    st.success("Game reset. Select a mode to start a new game.")

# Start a new game automatically on first load
if not st.session_state.game_started:
    start_new_game()

st.title("Marvel Guessing Game")
st.write("Guess the Marvel character! You can choose to guess yourself or let the computer guess.")

# Sidebar for game mode selection
st.sidebar.header("Game Mode")
mode = st.sidebar.radio("Choose a mode:", ["You Guess", "Computer Guesses"])

if st.sidebar.button("Start/Restart Game"):
    st.session_state.game_mode = mode.replace(" ", "_").lower()
    start_new_game()

if st.session_state.game_started:
    st.write(f"### Current Mode: {st.session_state.game_mode.replace('_', ' ').capitalize()}")

    # --- Mode 1: User Guesses ---
    if st.session_state.game_mode == 'user_guesses':
        if st.session_state.game_over:
            st.warning("The game is over. Please click 'Start/Restart Game' to play again.")
        else:
            st.write(f"You have used {st.session_state.user_tries} out of 15 tries.")
            
            # Hints after every 5 tries
            character_data = marvel_characters[st.session_state.secret_character]
            
            if st.session_state.user_tries >= 15:
                st.error(f"You have reached 15 tries. You lose! The character was **{st.session_state.secret_character}**.")
                st.session_state.game_over = True
            elif st.session_state.user_tries == 0:
                st.info("Your first hint is: " + character_data["hint1"])
            elif st.session_state.user_tries == 5:
                st.info("Second hint: " + character_data["hint2"])
            elif st.session_state.user_tries == 10:
                st.info("Third hint: " + character_data["hint3"])
            elif st.session_state.user_tries == 14:
                st.info("Last hint: " + character_data["hint4"])
            
            guess = st.text_input("Enter your guess:", help="You can ignore capitalization and hyphens.", key="user_guess_input").lower()

            if st.button("Submit Guess"):
                st.session_state.user_tries += 1
                if guess == st.session_state.secret_character.lower():
                    st.balloons()
                    st.success(f"Correct! You guessed the character in {st.session_state.user_tries} tries. You win!")
                    st.session_state.game_over = True
                else:
                    st.warning("Incorrect guess. Try again!")
                    if st.session_state.user_tries == 15:
                        st.error(f"You have reached 15 tries. You lose! The character was **{st.session_state.secret_character}**.")
                        st.session_state.game_over = True
                    

    # --- Mode 2: Computer Guesses ---
    if st.session_state.game_mode == 'computer_guesses':
        st.write("Think of a Marvel character from our list! I will try to guess it with a series of yes/no questions.")
        
        # Logic for computer guessing
        if st.session_state.game_over:
            st.warning("The game is over. Please click 'Start/Restart Game' to play again.")
        elif not st.session_state.available_characters:
            st.warning("I have run out of characters based on your answers! You win!")
            st.session_state.game_over = True
        elif len(st.session_state.available_characters) == 1:
            st.session_state.computer_guess = st.session_state.available_characters[0]
            st.info(f"I think your character is **{st.session_state.computer_guess}**! Am I right?")
            
            final_guess_feedback = st.radio(
                "Select an option:",
                ("Yes, you got it!", "No, you're wrong.")
            )
            if final_guess_feedback == "Yes, you got it!":
                st.success("I won! Thanks for playing!")
                st.balloons()
                st.session_state.game_over = True
            elif final_guess_feedback == "No, you're wrong.":
                st.error("Darn! You win, I couldn't guess your character. Please reset the game.")
                st.session_state.game_over = True
        elif st.session_state.question_index >= len(st.session_state.question_list):
            st.error("I have run out of questions and can't narrow it down further. You win!")
            st.session_state.game_over = True
        else:
            # Display the question
            current_question = st.session_state.question_list[st.session_state.question_index]
            st.write(f"### Question {st.session_state.computer_tries + 1}:")
            answer = st.radio(current_question["text"], ["Yes", "No"], key=f"question_{st.session_state.question_index}")
            
            if st.button("Submit Answer"):
                st.session_state.computer_tries += 1
                
                # Filter the list of available characters based on the user's answer
                filtered_chars = []
                for char in st.session_state.available_characters:
                    char_data = marvel_characters[char]
                    match = False
                    if current_question["type"] == "powers":
                        if current_question["value"] in char_data["powers"]:
                            match = True
                    elif current_question["type"] == "affiliation":
                        if current_question["value"] == char_data["affiliation"]:
                            match = True
                    elif current_question["type"] == "gender":
                        if current_question["value"] == char_data["gender"]:
                            match = True

                    if (answer == "Yes" and match) or (answer == "No" and not match):
                        filtered_chars.append(char)

                st.session_state.available_characters = filtered_chars
                st.session_state.question_index += 1
                st.write(f"Okay, I've got it. There are now {len(st.session_state.available_characters)} characters left.")
                st.rerun()


# Display a reset button outside of the game logic
if st.session_state.game_started and not st.session_state.game_over:
    st.write("---")
    st.button("Reset Game", on_click=reset_game)

st.write("---")
st.write("Developed with Streamlit.")
