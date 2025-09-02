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
if 'question_index' in st.session_state:
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
    },
    "Black Panther": {
        "powers": ["Superhuman strength", "Genius-level intellect", "Advanced vibranium suit", "Kinetic energy absorption"],
        "affiliation": "Avengers",
        "gender": "Male",
        "hint1": "He is the king of a technologically advanced African nation.",
        "hint2": "His suit is made from a nearly indestructible metal.",
        "hint3": "He is a protector of his people.",
        "hint4": "His name is T'Challa."
    },
    "Doctor Strange": {
        "powers": ["Magic", "Spellcasting", "Teleportation", "Eye of Agamotto"],
        "affiliation": "Solo hero",
        "gender": "Male",
        "hint1": "He was once a brilliant but arrogant neurosurgeon.",
        "hint2": "He became a powerful sorcerer after a life-altering accident.",
        "hint3": "He protects Earth from magical threats.",
        "hint4": "His name is Stephen Strange."
    },
    "Deadpool": {
        "powers": ["Accelerated healing", "Superhuman agility", "Expert swordsman", "Witty humor"],
        "affiliation": "Solo hero",
        "gender": "Male",
        "hint1": "He is known for his unique sense of humor and breaking the fourth wall.",
        "hint2": "He has a powerful healing factor that can regenerate him from almost any injury.",
        "hint3": "He is a mercenary who often uses two katanas.",
        "hint4": "His name is Wade Wilson."
    },
    "Loki": {
        "powers": ["Magic", "Shapeshifting", "Illusions", "Telekinesis"],
        "affiliation": "Villain",
        "gender": "Male",
        "hint1": "He is the adopted brother of another major hero.",
        "hint2": "He is known as the God of Mischief.",
        "hint3": "He often causes chaos and mayhem with his magical tricks.",
        "hint4": "He is from the realm of Asgard."
    },
    "Scarlet Witch": {
        "powers": ["Chaos magic", "Telekinesis", "Reality-warping", "Energy manipulation"],
        "affiliation": "Avengers",
        "gender": "Female",
        "hint1": "She has incredibly powerful magic abilities.",
        "hint2": "She's a twin, and her brother had super speed.",
        "hint3": "Her powers were enhanced by an Infinity Stone.",
        "hint4": "Her abilities are often unpredictable and tied to her emotions."
    },
    "Vision": {
        "powers": ["Superhuman strength", "Flight", "Intangibility", "Energy beam"],
        "affiliation": "Avengers",
        "gender": "Male",
        "hint1": "He is a synthezoid, a being of artificial flesh and machinery.",
        "hint2": "His body was created using a powerful artifact.",
        "hint3": "He can pass through solid objects.",
        "hint4": "A yellow stone is embedded in his forehead."
    },
    "Groot": {
        "powers": ["Regeneration", "Superhuman strength", "Wood manipulation", "Growth"],
        "affiliation": "Guardians of the Galaxy",
        "gender": "Male",
        "hint1": "He's a sentient, tree-like creature from an alien planet.",
        "hint2": "He can regenerate from a tiny piece of himself.",
        "hint3": "He has a very limited vocabulary, often saying only one phrase.",
        "hint4": "His friend is a raccoon."
    },
    "Ant-Man": {
        "powers": ["Size-changing", "Superhuman strength", "Communication with ants"],
        "affiliation": "Avengers",
        "gender": "Male",
        "hint1": "He is a former thief who can shrink down to a tiny size.",
        "hint2": "His suit allows him to control a special kind of insect.",
        "hint3": "He uses Pym Particles to change his size.",
        "hint4": "He once fought Falcon at the Avengers Compound."
    },
    "Captain Marvel": {
        "powers": ["Flight", "Superhuman strength", "Energy projection", "Cosmic power"],
        "affiliation": "Avengers",
        "gender": "Female",
        "hint1": "She is an Air Force pilot who gained cosmic powers after an accident.",
        "hint2": "She is one of the most powerful heroes in the universe.",
        "hint3": "Her cat is a Flerken.",
        "hint4": "Her powers are tied to the Tesseract."
    },
    "War Machine": {
        "powers": ["Powered armor", "Flight", "Advanced weaponry", "Tactical combat"],
        "affiliation": "Avengers",
        "gender": "Male",
        "hint1": "He is a military officer and an expert pilot.",
        "hint2": "He is a close friend of Iron Man.",
        "hint3": "His suit is equipped with a wide variety of armaments.",
        "hint4": "His name is James Rhodes."
    },
    "Gamora": {
        "powers": ["Superhuman strength", "Expert combatant", "Accelerated healing"],
        "affiliation": "Guardians of the Galaxy",
        "gender": "Female",
        "hint1": "She is the adopted daughter of a powerful titan.",
        "hint2": "She is known as the 'most dangerous woman in the galaxy'.",
        "hint3": "Her main weapon is a sword called Godslayer.",
        "hint4": "She is a member of the Guardians of the Galaxy."
    },
    "Star-Lord": {
        "powers": ["Expert pilot", "Master tactician", "Element gun"],
        "affiliation": "Guardians of the Galaxy",
        "gender": "Male",
        "hint1": "He is the leader of an unlikely group of heroes.",
        "hint2": "He was abducted from Earth as a child.",
        "hint3": "He loves to listen to music from the 70s and 80s.",
        "hint4": "His alias comes from a powerful celestial being."
    },
    "Rocket": {
        "powers": ["Genius-level intellect", "Expert marksman", "Cybernetic enhancements"],
        "affiliation": "Guardians of the Galaxy",
        "gender": "Male",
        "hint1": "He is a genetically engineered raccoon.",
        "hint2": "He is a master of weapons and military tactics.",
        "hint3": "He has a best friend who is a tree.",
        "hint4": "He loves collecting things, especially body parts."
    },
    "Drax": {
        "powers": ["Superhuman strength", "Enhanced durability", "Expert combatant"],
        "affiliation": "Guardians of the Galaxy",
        "gender": "Male",
        "hint1": "He is a warrior who takes everything literally.",
        "hint2": "He is an expert with knives and hand-to-hand combat.",
        "hint3": "He has a deep desire to avenge his family.",
        "hint4": "He is known for his large, muscular physique and tattoos."
    },
    "Falcon": {
        "powers": ["Advanced flight suit", "Expert pilot", "Close-quarters combat"],
        "affiliation": "Avengers",
        "gender": "Male",
        "hint1": "He is a close friend of Captain America.",
        "hint2": "He is a former pararescueman.",
        "hint3": "He flies with a specialized winged suit.",
        "hint4": "He is the new Captain America."
    },
    "Winter Soldier": {
        "powers": ["Superhuman strength", "Cybernetic arm", "Expert assassin"],
        "affiliation": "Avengers",
        "gender": "Male",
        "hint1": "He was a brainwashed assassin and a former friend of Captain America.",
        "hint2": "He has a powerful bionic arm.",
        "hint3": "He was thought to be dead for many years.",
        "hint4": "He is also known as Bucky Barnes."
    },
    "Wasp": {
        "powers": ["Size-changing", "Flight", "Energy blasters"],
        "affiliation": "Avengers",
        "gender": "Female",
        "hint1": "She is a partner to Ant-Man.",
        "hint2": "She uses a shrinking suit to change her size and fly.",
        "hint3": "Her father is a genius scientist who invented the Pym Particles.",
        "hint4": "Her name is Hope van Dyne."
    },
    "Nick Fury": {
        "powers": ["Master spy", "Expert tactician", "Skilled combatant"],
        "affiliation": "S.H.I.E.L.D.",
        "gender": "Male",
        "hint1": "He is the former director of a global peacekeeping organization.",
        "hint2": "He is known for bringing the Avengers together.",
        "hint3": "He has a black eye patch and is very mysterious.",
        "hint4": "He is a master spy and strategist."
    },
    "Hawkeye": {
        "powers": ["Expert archer", "Master marksman", "Expert combatant"],
        "affiliation": "Avengers",
        "gender": "Male",
        "hint1": "He is a master with a bow and arrow.",
        "hint2": "He has no superpowers, but is an expert marksman.",
        "hint3": "He is a founding member of the Avengers.",
        "hint4": "His name is Clint Barton."
    },
    "Shuri": {
        "powers": ["Genius-level intellect", "Master of technology", "Tactical combat"],
        "affiliation": "Solo hero",
        "gender": "Female",
        "hint1": "She is a genius inventor from a technologically advanced nation.",
        "hint2": "She is the princess of Wakanda.",
        "hint3": "She designs the Black Panther's suit and weapons.",
        "hint4": "She is the sister of King T'Challa."
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
            
            # Use st.form to make the guessing process smoother
            with st.form(key='user_guess_form'):
                guess = st.text_input("Enter your guess:", help="You can ignore capitalization and hyphens.").lower()
                submit_button = st.form_submit_button(label='Submit Guess')

            if submit_button:
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
                    st.rerun()
                    

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
            st.session_state.last_answer = final_guess_feedback # Store the user's final answer
            
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
            # Wrap the radio button and submit button in a form
            with st.form(key='computer_guess_form'):
                current_question = st.session_state.question_list[st.session_state.question_index]
                st.write(f"### Question {st.session_state.computer_tries + 1}:")
                answer = st.radio(current_question["text"], ["Yes", "No"], key=f"question_{st.session_state.question_index}")
                submit_answer_button = st.form_submit_button(label="Submit Answer")

            if submit_answer_button:
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

# --- Game over image display ---
if st.session_state.game_over:
    st.write("---")
    st.header("Game Over!")
    
    # Check if the user won or lost to display the correct message and image
    if st.session_state.game_mode == 'user_guesses' and st.session_state.user_tries < 15:
        st.success("You won! Here is the character you guessed!")
    elif st.session_state.game_mode == 'computer_guesses' and st.session_state.computer_guess is not None and st.session_state.last_answer == 'Yes, you got it!':
        st.success("I won! Here is the character I guessed!")
    else:
        st.error("You lost! Here is the character you were trying to guess.")
        
    # Create the URL for the placeholder image using the character's name
    character_name_for_url = st.session_state.secret_character.replace(" ", "%20")
    image_url = f"https://placehold.co/600x400?text={character_name_for_url}"
    
    st.image(image_url, caption=f"The secret character was: {st.session_state.secret_character}", width=400)

# Display a reset button outside of the game logic
if st.session_state.game_started and not st.session_state.game_over:
    st.write("---")
    st.button("Reset Game", on_click=reset_game)

st.write("---")
st.write("Developed with Streamlit.")
