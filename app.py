import streamlit as st
import random

# Define Marvel characters and their clues
MARVEL_CHARACTERS = {
    "Iron Man": {
        "clues": [
            "He's a genius billionaire, playboy, philanthropist.",
            "He built his first armored suit in a cave with a box of scraps.",
            "His real name is Tony Stark.",
            "He often says, 'I am Iron Man.'"
        ],
        "image": "https://placehold.co/400x200/FF0000/FFFFFF?text=Iron+Man"
    },
    "Captain America": {
        "clues": [
            "He was a scrawny kid from Brooklyn who became a super-soldier.",
            "His shield is made of vibranium.",
            "His real name is Steve Rogers.",
            "He's known for his strong moral compass and leadership."
        ],
        "image": "https://placehold.co/400x200/0000FF/FFFFFF?text=Captain+America"
    },
    "Thor": {
        "clues": [
            "He's the God of Thunder.",
            "His primary weapon is Mjolnir (or Stormbreaker).",
            "He hails from Asgard.",
            "He's a member of the Avengers and often struggles with Earth customs."
        ],
        "image": "https://placehold.co/400x200/00FFFF/000000?text=Thor"
    },
    "Hulk": {
        "clues": [
            "He transforms into a giant, green, rage-filled monster.",
            "His real name is Bruce Banner.",
            "He's incredibly strong when angry.",
            "He often says, 'Hulk smash!'"
        ],
        "image": "https://placehold.co/400x200/00FF00/FFFFFF?text=Hulk"
    },
    "Black Widow": {
        "clues": [
            "She's a highly skilled spy and assassin.",
            "Her real name is Natasha Romanoff.",
            "She was trained in the Red Room.",
            "She's an expert in martial arts and espionage."
        ],
        "image": "https://placehold.co/400x200/000000/FF0000?text=Black+Widow"
    },
    "Spider-Man": {
        "clues": [
            "He's a friendly neighborhood superhero.",
            "He gained his powers after being bitten by a radioactive spider.",
            "His real name is Peter Parker.",
            "He has a strong sense of responsibility, often saying, 'With great power comes great responsibility.'"
        ],
        "image": "https://placehold.co/400x200/FF0000/000000?text=Spider-Man"
    },
    "Doctor Strange": {
        "clues": [
            "He was a brilliant but arrogant surgeon who lost the use of his hands.",
            "He became the Sorcerer Supreme.",
            "He wields magic and manipulates time with the Eye of Agamotto.",
            "His real name is Stephen Strange."
        ],
        "image": "https://placehold.co/400x200/800080/FFFFFF?text=Doctor+Strange"
    },
    "Black Panther": {
        "clues": [
            "He is the king and protector of Wakanda.",
            "His suit is made of vibranium.",
            "His real name is T'Challa.",
            "He possesses enhanced senses and strength due to the heart-shaped herb."
        ],
        "image": "https://placehold.co/400x200/000000/00FFFF?text=Black+Panther"
    },
    "Scarlet Witch": {
        "clues": [
            "She has powerful reality-warping abilities.",
            "Her real name is Wanda Maximoff.",
            "She can manipulate chaos magic.",
            "She often struggles with controlling her vast powers."
        ],
        "image": "https://placehold.co/400x200/FF00FF/000000?text=Scarlet+Witch"
    },
    "Deadpool": {
        "clues": [
            "He's the 'Merc with a Mouth'.",
            "He has a regenerative healing factor.",
            "He frequently breaks the fourth wall.",
            "His real name is Wade Wilson."
        ],
        "image": "https://placehold.co/400x200/800000/FFFFFF?text=Deadpool"
    }
}

def initialize_game_state():
    """Initializes or resets the game state in Streamlit's session_state."""
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'current_character' not in st.session_state:
        st.session_state.current_character = None
    if 'clues_given' not in st.session_state:
        st.session_state.clues_given = []
    if 'guessed_correctly' not in st.session_state:
        st.session_state.guessed_correctly = False
    if 'game_started' not in st.session_state:
        st.session_state.game_started = False
    if 'game_over' not in st.session_state:
        st.session_state.game_over = False
    if 'feedback_message' not in st.session_state:
        st.session_state.feedback_message = ""
    if 'available_characters' not in st.session_state:
        st.session_state.available_characters = list(MARVEL_CHARACTERS.keys())
    if 'attempts' not in st.session_state:
        st.session_state.attempts = 0

def start_new_round():
    """Starts a new guessing round."""
    # Reset for a new round
    st.session_state.clues_given = []
    st.session_state.guessed_correctly = False
    st.session_state.feedback_message = ""
    st.session_state.attempts = 0

    if not st.session_state.available_characters:
        st.session_state.game_over = True
        st.session_state.feedback_message = "You've guessed all characters! Game over!"
        st.session_state.current_character = None
        return

    # Select a random character that hasn't been guessed yet
    st.session_state.current_character = random.choice(st.session_state.available_characters)
    
    # Remove the character from available_characters to avoid repetition in the same game
    st.session_state.available_characters.remove(st.session_state.current_character)
    
    st.session_state.game_started = True


def give_clue():
    """Gives a new clue for the current character."""
    if not st.session_state.current_character:
        st.session_state.feedback_message = "Please start a new round first!"
        return

    character_info = MARVEL_CHARACTERS[st.session_state.current_character]
    available_clues = [
        clue for clue in character_info["clues"] if clue not in st.session_state.clues_given
    ]

    if available_clues:
        new_clue = random.choice(available_clues)
        st.session_state.clues_given.append(new_clue)
        st.session_state.feedback_message = "" # Clear previous feedback
    else:
        st.session_state.feedback_message = "No more clues for this character!"

def check_guess(guess):
    """Checks the user's guess against the current character."""
    st.session_state.attempts += 1
    if st.session_state.current_character and guess.lower() == st.session_state.current_character.lower():
        st.session_state.score += 1
        st.session_state.guessed_correctly = True
        st.session_state.feedback_message = f"🎉 Correct! It was {st.session_state.current_character}!"
    else:
        st.session_state.feedback_message = "❌ Incorrect guess. Try again or get another clue!"


def reset_game():
    """Resets the entire game."""
    st.session_state.score = 0
    st.session_state.current_character = None
    st.session_state.clues_given = []
    st.session_state.guessed_correctly = False
    st.session_state.game_started = False
    st.session_state.game_over = False
    st.session_state.feedback_message = ""
    st.session_state.available_characters = list(MARVEL_CHARACTERS.keys())
    st.session_state.attempts = 0

# --- Streamlit App Layout ---
st.set_page_config(
    page_title="Marvel Guessing Game",
    page_icon="🦸‍♂️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.title("Guess the Marvel Character! 🦸‍♀️")

# Initialize game state on first run
initialize_game_state()

# Display current score
st.sidebar.header(f"Score: {st.session_state.score}")
st.sidebar.button("Reset Game", on_click=reset_game)

if not st.session_state.game_started and not st.session_state.game_over:
    st.write("Welcome to the Marvel Guessing Game! Click 'Start New Game' to begin.")
    if st.button("Start New Game", key="start_game_button"):
        start_new_round()
        give_clue() # Give the first clue immediately
        st.rerun() # Rerun to display the clue

if st.session_state.game_over:
    st.success(st.session_state.feedback_message)
    st.image("https://placehold.co/400x200/008000/FFFFFF?text=Game+Over!")
    if st.button("Play Again", key="play_again_button"):
        reset_game()
        start_new_round()
        give_clue()
        st.rerun()

elif st.session_state.game_started and not st.session_state.guessed_correctly:
    st.subheader("Can you guess this Marvel Character?")

    # Display clues
    for i, clue in enumerate(st.session_state.clues_given):
        st.info(f"Clue {i+1}: {clue}")

    # Input for guess
    with st.form(key="guess_form"):
        user_guess = st.text_input("Your Guess:", key="user_guess_input").strip()
        col1, col2 = st.columns(2)
        with col1:
            submit_button = st.form_submit_button("Submit Guess")
        with col2:
            get_clue_button = st.form_submit_button("Get Another Clue")

    if submit_button and user_guess:
        check_guess(user_guess)
        st.rerun() # Rerun to update feedback
    elif get_clue_button:
        give_clue()
        st.rerun() # Rerun to display new clue

    if st.session_state.feedback_message:
        if "Correct" in st.session_state.feedback_message:
            st.success(st.session_state.feedback_message)
            # Display character image upon correct guess
            if st.session_state.current_character in MARVEL_CHARACTERS:
                st.image(MARVEL_CHARACTERS[st.session_state.current_character]["image"], caption=st.session_state.current_character)
            if st.button("Next Character", key="next_character_button"):
                start_new_round()
                give_clue() # Give the first clue for the new character
                st.rerun()
        elif "Incorrect" in st.session_state.feedback_message:
            st.error(st.session_state.feedback_message)
        else:
            st.warning(st.session_state.feedback_message)

    st.markdown(f"**Attempts for this character:** {st.session_state.attempts}")

elif st.session_state.game_started and st.session_state.guessed_correctly:
    st.success(st.session_state.feedback_message)
    # Display character image upon correct guess
    if st.session_state.current_character in MARVEL_CHARACTERS:
        st.image(MARVEL_CHARACTERS[st.session_state.current_character]["image"], caption=st.session_state.current_character)
    
    if st.session_state.available_characters:
        if st.button("Next Character", key="next_character_after_correct_guess"):
            start_new_round()
            give_clue() # Give the first clue for the new character
            st.rerun()
    else:
        st.session_state.game_over = True
        st.session_state.feedback_message = "You've guessed all characters! Game over!"
        st.rerun()

# Styling for the app
st.markdown("""
<style>
    .reportview-container {
        background: #0e1117;
        color: #fff;
    }
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    h1 {
        color: #ff4b4b; /* Marvel-like red */
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    h2, h3, h4, h5, h6 {
        color: #00bcd4; /* Light blue/cyan for subheadings */
    }
    .stButton>button {
        background-color: #ff4b4b;
        color: white;
        border-radius: 12px;
        border: 2px solid #cc0000;
        padding: 10px 20px;
        font-size: 18px;
        font-weight: bold;
        box-shadow: 3px 3px 5px rgba(0,0,0,0.3);
        transition: all 0.2s ease-in-out;
    }
    .stButton>button:hover {
        background-color: #cc0000;
        border-color: #990000;
        transform: translateY(-2px);
        box-shadow: 5px 5px 8px rgba(0,0,0,0.4);
    }
    .stButton>button:active {
        transform: translateY(0);
        box-shadow: 2px 2px 3px rgba(0,0,0,0.2);
    }
    .stTextInput>div>div>input {
        border-radius: 12px;
        border: 2px solid #00bcd4;
        padding: 10px;
        font-size: 16px;
        color: #fff;
        background-color: #262730;
    }
    .stTextInput>div>div>input:focus {
        border-color: #ff4b4b;
        box-shadow: 0 0 8px rgba(255, 75, 75, 0.6);
    }
    .stAlert {
        border-radius: 12px;
        padding: 10px;
        margin-bottom: 10px;
    }
    .stAlert.info {
        background-color: #3f51b530; /* Blue-ish with transparency */
        color: #3f51b5;
        border-left: 5px solid #3f51b5;
    }
    .stAlert.success {
        background-color: #4CAF5030; /* Green-ish with transparency */
        color: #4CAF50;
        border-left: 5px solid #4CAF50;
    }
    .stAlert.error {
        background-color: #F4433630; /* Red-ish with transparency */
        color: #F44336;
        border-left: 5px solid #F44336;
    }
    .stAlert.warning {
        background-color: #FFC10730; /* Yellow-ish with transparency */
        color: #FFC107;
        border-left: 5px solid #FFC107;
    }
    .sidebar .sidebar-content {
        background-image: linear-gradient(180deg, #1e1e2d, #0e1117);
        color: #fff;
    }
    .css-1d391kg { /* For score in sidebar */
        font-size: 2em;
        font-weight: bold;
        color: #ff4b4b;
        text-align: center;
        margin-top: 1em;
    }
    /* Style for the image placeholder text */
    .stImage > img {
        border-radius: 12px;
        border: 2px solid #00bcd4;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)
