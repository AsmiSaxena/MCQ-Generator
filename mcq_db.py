import sqlite3

def create_connection():
    """Create a database connection."""
    conn = sqlite3.connect('mcq_questions.db')
    return conn

def create_table():
    """Create a table for storing questions."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            option_a TEXT NOT NULL,
            option_b TEXT NOT NULL,
            option_c TEXT NOT NULL,
            option_d TEXT NOT NULL,
            answer TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def insert_multiple_questions(questions):
    """
    Insert multiple questions into the questions table.
    
    Parameters:
        questions (list of tuples): Each tuple contains
        (question, option_a, option_b, option_c, option_d, answer)
    """
    conn = create_connection()
    cursor = conn.cursor()
    cursor.executemany('''
        INSERT INTO questions (question, option_a, option_b, option_c, option_d, answer)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', questions)
    conn.commit()
    conn.close()

# Example usage
questions_data = [
    # Programming & Technology
    ('What is JavaScript primarily used for?', 'Web Development', 'Mobile Apps', 'Operating Systems', 'Database Management', 'Web Development'),
    ('Who founded Microsoft?', 'Bill Gates', 'Steve Jobs', 'Mark Zuckerberg', 'Jeff Bezos', 'Bill Gates'),
    ('What does CPU stand for?', 'Central Processing Unit', 'Computer Personal Unit', 'Central Program Utility', 'Computer Processing Unit', 'Central Processing Unit'),
    ('Which programming language is known for Android development?', 'Java', 'Swift', 'Python', 'Ruby', 'Java'),
    ('What is the primary function of HTML?', 'Structuring Web Content', 'Database Management', 'Server Programming', 'Image Editing', 'Structuring Web Content'),

    # Science & Nature
    ('What is the largest organ in the human body?', 'Skin', 'Heart', 'Brain', 'Liver', 'Skin'),
    ('Which gas do plants absorb from the atmosphere?', 'Carbon Dioxide', 'Oxygen', 'Nitrogen', 'Hydrogen', 'Carbon Dioxide'),
    ('What is the atomic number of Gold?', '79', '47', '29', '82', '79'),
    ('Which planet has the most moons?', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Saturn'),
    ('What is the smallest unit of life?', 'Cell', 'Atom', 'Molecule', 'Gene', 'Cell'),

    # Mathematics
    ('What is the square root of 144?', '12', '14', '10', '16', '12'),
    ('What is the value of π (pi) to two decimal places?', '3.14', '3.16', '3.12', '3.18', '3.14'),
    ('What is 15% of 200?', '30', '25', '35', '40', '30'),
    ('What is the next number in the sequence: 2, 4, 8, 16...?', '32', '24', '28', '20', '32'),
    ('What is the sum of angles in a triangle?', '180°', '360°', '90°', '270°', '180°'),

    # History
    ('When did World War II end?', '1945', '1944', '1946', '1943', '1945'),
    ('Who was the first President of the United States?', 'George Washington', 'Thomas Jefferson', 'John Adams', 'Benjamin Franklin', 'George Washington'),
    ('In which year did the Berlin Wall fall?', '1989', '1991', '1987', '1985', '1989'),
    ('Who was the first woman to win a Nobel Prize?', 'Marie Curie', 'Mother Teresa', 'Jane Addams', 'Pearl Buck', 'Marie Curie'),
    ('Which empire was ruled by Caesar?', 'Roman Empire', 'Greek Empire', 'Persian Empire', 'Ottoman Empire', 'Roman Empire'),

    # Geography
    ('Which is the largest ocean?', 'Pacific', 'Atlantic', 'Indian', 'Arctic', 'Pacific'),
    ('What is the capital of Japan?', 'Tokyo', 'Seoul', 'Beijing', 'Bangkok', 'Tokyo'),
    ('Which country has the largest population?', 'India', 'China', 'USA', 'Indonesia', 'India'),
    ('What is the longest river in the world?', 'Nile', 'Amazon', 'Mississippi', 'Yangtze', 'Nile'),
    ('On which continent is the Sahara Desert?', 'Africa', 'Asia', 'South America', 'Australia', 'Africa'),

    # Literature
    ('Who wrote "1984"?', 'George Orwell', 'Aldous Huxley', 'Ray Bradbury', 'Ernest Hemingway', 'George Orwell'),
    ('What is the first book in the Harry Potter series?', 'Philosopher\'s Stone', 'Chamber of Secrets', 'Prisoner of Azkaban', 'Goblet of Fire', 'Philosopher\'s Stone'),
    ('Who wrote "The Great Gatsby"?', 'F. Scott Fitzgerald', 'Ernest Hemingway', 'John Steinbeck', 'Mark Twain', 'F. Scott Fitzgerald'),
    ('Which Shakespeare play features Romeo?', 'Romeo and Juliet', 'Hamlet', 'Macbeth', 'Othello', 'Romeo and Juliet'),
    ('Who wrote "Pride and Prejudice"?', 'Jane Austen', 'Emily Brontë', 'Virginia Woolf', 'Charlotte Brontë', 'Jane Austen'),

    # Arts & Entertainment
    ('Which artist painted "The Starry Night"?', 'Vincent van Gogh', 'Pablo Picasso', 'Claude Monet', 'Salvador Dalí', 'Vincent van Gogh'),
    ('What instrument has 88 keys?', 'Piano', 'Guitar', 'Violin', 'Drums', 'Piano'),
    ('Who directed "Jurassic Park"?', 'Steven Spielberg', 'James Cameron', 'George Lucas', 'Martin Scorsese', 'Steven Spielberg'),
    ('Which band performed "Bohemian Rhapsody"?', 'Queen', 'The Beatles', 'Led Zeppelin', 'Pink Floyd', 'Queen'),
    ('What is the highest-grossing movie of all time?', 'Avatar', 'Titanic', 'Avengers: Endgame', 'Star Wars', 'Avatar'),

    # Science & Technology
    ('What is the smallest planet in our solar system?', 'Mercury', 'Mars', 'Venus', 'Pluto', 'Mercury'),
    ('What is the hardest natural substance?', 'Diamond', 'Gold', 'Iron', 'Platinum', 'Diamond'),
    ('What is the speed of sound in air?', '343 m/s', '299 m/s', '400 m/s', '500 m/s', '343 m/s'),
    ('What is the main component of the Sun?', 'Hydrogen', 'Helium', 'Oxygen', 'Carbon', 'Hydrogen'),
    ('What is the chemical symbol for gold?', 'Au', 'Ag', 'Fe', 'Cu', 'Au'),

    # Sports
    ('In which sport would you perform a slam dunk?', 'Basketball', 'Football', 'Tennis', 'Golf', 'Basketball'),
    ('How many players are on a soccer team?', '11', '9', '10', '12', '11'),
    ('Which country won the first FIFA World Cup?', 'Uruguay', 'Brazil', 'Argentina', 'Germany', 'Uruguay'),
    ('In which sport is a "shuttlecock" used?', 'Badminton', 'Tennis', 'Table Tennis', 'Squash', 'Badminton'),
    ('How many Olympic rings are there?', '5', '4', '6', '3', '5'),

    # General Knowledge
    ('What is the currency of Japan?', 'Yen', 'Won', 'Yuan', 'Ringgit', 'Yen'),
    ('Which animal is known as the "King of the Jungle"?', 'Lion', 'Tiger', 'Elephant', 'Gorilla', 'Lion'),
    ('How many continents are there?', '7', '5', '6', '8', '7'),
    ('What is the main ingredient in guacamole?', 'Avocado', 'Tomato', 'Onion', 'Lime', 'Avocado'),
    ('What is the most spoken language in the world?', 'Mandarin Chinese', 'English', 'Spanish', 'Hindi', 'Mandarin Chinese')
]



insert_multiple_questions(questions_data)
print("Multiple questions inserted successfully.")



if __name__ == "__main__":
    create_table()  # Create the table when running this script.