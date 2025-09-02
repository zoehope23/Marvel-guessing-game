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

def start_new_game():
    """Resets the game state and picks a new character."""
    st.session_state.game_started = True
    st.session_state.game_over = False
    st.session_state.user_tries = 0
    st.session_state.computer_tries = 0
    st.session_state.user_hints = []
    st.session_state.computer_guess = None
    st.session_state.secret_character = random.choice(list(marvel_characters.keys()))
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
    st.success("Game reset. Select a mode to start a new game.")

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
        st.write("Think of a Marvel character from our list! I will try to guess it in 15 tries.")
        
        # Displaying past hints from the user
        if st.session_state.user_hints:
            st.write("### Your Hints:")
            for hint_type, hint_value in st.session_state.user_hints:
                st.write(f"- I am looking for a character with the **{hint_type}** of **'{hint_value}'**.")

        # Logic for computer guessing
        if st.session_state.game_over:
            st.warning("The game is over. Please click 'Start/Restart Game' to play again.")
        elif st.session_state.computer_tries >= 15:
            st.error("I have reached 15 guesses and could not figure it out. You win!")
            st.session_state.game_over = True
        else:
            st.write(f"The computer has used {st.session_state.computer_tries} out of 15 tries.")
            if st.button("Computer's turn to guess!"):
                available_characters = list(marvel_characters.keys())
                
                # Filter characters based on hints given
                for hint_type, hint_value in st.session_state.user_hints:
                    if hint_type == "powers":
                        available_characters = [
                            char for char in available_characters if hint_value in marvel_characters[char]["powers"]
                        ]
                    elif hint_type == "affiliation":
                        available_characters = [
                            char for char in available_characters if marvel_characters[char]["affiliation"] == hint_value
                        ]
                    elif hint_type == "gender":
                        available_characters = [
                            char for char in available_characters if marvel_characters[char]["gender"] == hint_value
                        ]
                
                if not available_characters:
                    st.warning("I'm stumped! My character list is exhausted based on your hints. You win!")
                    st.session_state.game_over = True
                else:
                    st.session_state.computer_tries += 1
                    st.session_state.computer_guess = random.choice(available_characters)
                    st.write(f"My guess is... **{st.session_state.computer_guess}**")
            
            if st.session_state.computer_guess:
                st.markdown("### Was my guess correct?")
                guess_feedback = st.radio(
                    "Select an option:",
                    ("My guess was correct!", "My guess was incorrect, here's a hint.")
                )

                if guess_feedback == "My guess was correct!":
                    st.success(f"I got it! I guessed your character **{st.session_state.computer_guess}** in {st.session_state.computer_tries} tries! I win!")
                    st.balloons()
                    st.session_state.game_over = True
                
                elif guess_feedback == "My guess was incorrect, here's a hint.":
                    st.markdown("### Give me a hint:")
                    hint_type = st.selectbox(
                        "What type of hint would you like to give?",
                        ["powers", "affiliation", "gender"]
                    )
                    hint_value = st.text_input(f"Enter the value for the **{hint_type}** hint (e.g., 'Flight', 'Avengers', 'Male'):")
                    
                    # Store all possible hints for validation
                    valid_hints = []
                    for char in marvel_characters.values():
                        valid_hints.extend(char.get(hint_type, []))

                    if st.button("Submit Hint"):
                        if hint_value:
                            if hint_value in valid_hints:
                                st.session_state.user_hints.append((hint_type, hint_value))
                                st.success("Hint received. I will use this for my next guess.")
                                st.session_state.computer_guess = None # Reset guess to trigger new turn
                            else:
                                st.warning("That hint value doesn't seem to be in my list. Please try a different one.")
                        else:
                            st.warning("Please enter a hint value.")


# Display a reset button outside of the game logic
if st.session_state.game_started and not st.session_state.game_over:
    st.write("---")
    st.button("Reset Game", on_click=reset_game)

st.write("---")
st.write("Developed with Streamlit.")
