import streamlit as st
import sqlite3
from typing import Optional, Tuple
def get_performance_message(score: int) -> tuple:
    """
    Return performance message and color based on score.
    Returns tuple of (message, color)
    """
    if score < 3:
        return "Oops you failed! 😔", "red"
    elif 3 <= score < 5:
        return "Poor performance! Need more practice! 📚", "orange"
    elif 5 <= score <= 8:
        return "Goooooood!! Keep it up! 🌟", "green"
    else:
        return "Excellent!! Outstanding performance! 🏆", "blue"

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

    # Show final score and performance feedback
    if st.session_state.quiz_completed:
        st.success("Quiz Completed! 🎉")
        
        # Calculate final score and accuracy
        final_score = st.session_state.score
        accuracy = (final_score / MAX_QUESTIONS) * 100
        
        # Create three columns for better layout
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            st.metric("Final Score", f"{final_score}/{MAX_QUESTIONS}")
        
        with col2:
            st.metric("Accuracy", f"{accuracy:.1f}%")
        
        # Get performance message and display with appropriate styling
        message, color = get_performance_message(final_score)
        
        # Display performance message with custom styling
        st.markdown(
            f"""
            <div style='padding: 20px; 
                        border-radius: 10px; 
                        text-align: center;
                        margin: 20px 0;
                        background-color: {color}20;
                        border: 2px solid {color};'>
                <h2 style='color: {color}; margin: 0;'>{message}</h2>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # Add some performance tips based on score
        if final_score < 5:
            st.info("""
            Tips for improvement:
            - Review the topics you're unsure about
            - Take practice quizzes regularly
            - Focus on understanding concepts rather than memorizing
            """)
        
        # Restart button
        if st.button("Start New Quiz", key="restart_button"):
            reset_quiz()
            st.rerun()

if __name__ == "__main__":
    main()