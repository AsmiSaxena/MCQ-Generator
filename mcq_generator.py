import sqlite3

def create_connection():
    """Create a database connection."""
    conn = sqlite3.connect('mcq_questions.db')
    return conn

def get_random_question():
    """Retrieve a random question from the database."""
    conn = create_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM questions ORDER BY RANDOM() LIMIT 1')
    question = cursor.fetchone()
    
    conn.close()
    
    return question

def ask_question(question):
    """Present a question to the user and check their answer."""
    print("\n" + question[1])  # Print the question text
    print("A:", question[2])
    print("B:", question[3])
    print("C:", question[4])
    print("D:", question[5])
    
    answer = input("Your answer (A/B/C/D): ").strip().upper()
    
    if answer == question[6].upper():
        print("Correct!")
        return True  # Correct answer
    else:
        print(f"Wrong! The correct answer was {question[6]}.")
        return False  # Incorrect answer

if __name__ == "__main__":
    score = 0  # Initialize score
    total_questions = 0  # Initialize total questions asked
    
    while True:
        question = get_random_question()
        if question:
            total_questions += 1
            if ask_question(question):
                score += 1  # Increment score for correct answer
        else:
            print("No more questions available.")
            break
        
        cont = input("Do you want to continue? (yes/no): ").strip().lower()
        if cont != 'yes':
            break
    
    # Display final score
    print(f"\nYour final score is {score}/{total_questions}.")