import streamlit as st
import sqlite3
from typing import Optional, Tuple

def create_connection() -> sqlite3.Connection:
    """Create a database connection to SQLite database."""
    try:
        conn = sqlite3.connect('mcq_questions.db')
        return conn
    except sqlite3.Error as e:
        st.error(f"Error connecting to database: {e}")
        return None

def initialize_database() -> None:
    """Initialize the database with a questions table if it doesn't exist."""
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS questions (
                    id INTEGER PRIMARY KEY,
                    question TEXT NOT NULL,
                    option1 TEXT NOT NULL,
                    option2 TEXT NOT NULL,
                    option3 TEXT NOT NULL,
                    option4 TEXT NOT NULL,
                    correct_answer TEXT NOT NULL
                )
            ''')
            conn.commit()
        except sqlite3.Error as e:
            st.error(f"Error initializing database: {e}")
        finally:
            conn.close()

def get_random_question(used_questions: list) -> Optional[Tuple]:
    """Retrieve a random question from the database."""
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            
            # Convert used_questions list to tuple for SQL
            used_ids = tuple(used_questions) if used_questions else (-1,)
            
            # Using parameterized query for safety
            cursor.execute('''
                SELECT * FROM questions 
                WHERE id NOT IN ({})
                ORDER BY RANDOM() 
                LIMIT 1
            '''.format(','.join('?' * len(used_ids))), used_ids)
            
            question = cursor.fetchone()
            return question
        except sqlite3.Error as e:
            st.error(f"Error retrieving question: {e}")
            return None
        finally:
            conn.close()
    return None

def insert_sample_questions():
    """Insert sample questions into the database."""
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            # Sample questions data
            questions = [
                ('What is Python?', 'Programming Language', 'Snake', 'Movie', 'Animal', 'Programming Language'),
                ('Who developed Python?', 'Guido van Rossum', 'Elon Musk', 'Ada Lovelace', 'Alan Turing', 'Guido van Rossum'),
                ('What is 2 + 2?', '3', '4', '5', '6', '4'),
                ('Which planet is known as the Red Planet?', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Mars'),
                ('What is the chemical symbol for water?', 'H2O', 'CO2', 'NaCl', 'O2', 'H2O'),
                ('What is the largest mammal?', 'Elephant', 'Blue Whale', 'Giraffe', 'Polar Bear', 'Blue Whale'),
                ('Who painted the Mona Lisa?', 'Vincent van Gogh', 'Pablo Picasso', 'Leonardo da Vinci', 'Claude Monet', 'Leonardo da Vinci'),
                ('What is the capital of France?', 'Berlin', 'Madrid', 'Paris', 'Rome', 'Paris'),
                ('What is the speed of light?', '300,000 km/s', '150,000 km/s', '400,000 km/s', '100,000 km/s', '300,000 km/s'),
                ('Who wrote "Hamlet"?', 'Charles Dickens', 'William Shakespeare', 'Mark Twain', 'J.K. Rowling', 'William Shakespeare')
            ]
            
            cursor.execute('SELECT COUNT(*) FROM questions')
            count = cursor.fetchone()[0]
            
            if count == 0:
                cursor.executemany('''
                    INSERT INTO questions (question, option1, option2, option3, option4, correct_answer)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', questions)
                conn.commit()
                st.success("Sample questions loaded successfully!")
        except sqlite3.Error as e:
            st.error(f"Error inserting sample questions: {e}")
        finally:
            conn.close()

def check_answer(selected_option: str, correct_answer: str) -> None:
    """Check the selected answer and update score."""
    if selected_option == correct_answer:
        st.session_state.score += 1
        st.success("Correct! 🎉")
    else:
        st.error(f"Wrong! The correct answer was: {correct_answer}")

def initialize_session_state() -> None:
    """Initialize session state variables."""
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "question_count" not in st.session_state:
        st.session_state.question_count = 0
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
    if "quiz_completed" not in st.session_state:
        st.session_state.quiz_completed = False
    if "used_questions" not in st.session_state:
        st.session_state.used_questions = []

def reset_quiz() -> None:
    """Reset all session state variables for a new quiz."""
    st.session_state.score = 0
    st.session_state.question_count = 0
    st.session_state.current_question = None
    st.session_state.quiz_completed = False
    st.session_state.used_questions = []

def main() -> None:
    """Main function to run the Streamlit app."""
    st.title("Random MCQ Generator")
    
    # Initialize database and session state
    initialize_database()
    initialize_session_state()
    
    # Insert sample questions if database is empty
    insert_sample_questions()

    # Set maximum number of questions
    MAX_QUESTIONS = 10

    if not st.session_state.quiz_completed:
        if st.session_state.question_count < MAX_QUESTIONS:
            # Get new question if needed
            if st.session_state.current_question is None:
                question = get_random_question(st.session_state.used_questions)
                if question:
                    st.session_state.current_question = question
                    if question[0] not in st.session_state.used_questions:
                        st.session_state.used_questions.append(question[0])
                else:
                    st.error("No more questions available!")
                    st.session_state.quiz_completed = True
                    return

            # Display current question
            if st.session_state.current_question:
                question = st.session_state.current_question
                st.subheader(f"Question {st.session_state.question_count + 1} of {MAX_QUESTIONS}")
                st.write(question[1])  # Question text

                # Display options
                options = [question[2], question[3], question[4], question[5]]
                selected_option = st.radio("Choose your answer:", options, key=f"q_{st.session_state.question_count}")

                # Submit button
                if st.button("Submit Answer", key=f"submit_{st.session_state.question_count}"):
                    check_answer(selected_option, question[6])
                    st.session_state.question_count += 1
                    st.session_state.current_question = None
                    
                    # Force rerun to update the page
                    st.rerun()

            # Display current score
            st.sidebar.metric("Current Score", f"{st.session_state.score}/{st.session_state.question_count}")

        else:
            st.session_state.quiz_completed = True

    # Show final score and restart option
    if st.session_state.quiz_completed:
        st.success("Quiz Completed! 🎉")
        st.metric("Final Score", f"{st.session_state.score}/{MAX_QUESTIONS}")
        
        accuracy = (st.session_state.score / MAX_QUESTIONS) * 100
        st.write(f"Accuracy: {accuracy:.1f}%")

        if st.button("Start New Quiz"):
            reset_quiz()
            st.rerun()

if __name__ == "__main__":
    main()