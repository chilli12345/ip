import mysql.connector
import random

def connect_to_db():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="2007",
        database="ip"
    )
    return connection

def generate_user_id():
    return str(random.randint(1000, 9999))

def create_user_table(connection, user_id):
    cursor = connection.cursor()
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS user_{user_id} (
        test_id INT AUTO_INCREMENT PRIMARY KEY,
        question_id INT,
        question TEXT,
        answer INT,
        test_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    cursor.execute(create_table_query)
    connection.commit()

def insert_user_answers(connection, user_id, questions, answers):
    cursor = connection.cursor()
    for question_id, (question, answer) in enumerate(zip(questions, answers), start=1):
        insert_query = f"INSERT INTO user_{user_id} (question_id, question, answer) VALUES (%s, %s, %s);"
        cursor.execute(insert_query, (question_id, question, answer))
    connection.commit()

def fetch_latest_two_tests(connection, user_id):
    cursor = connection.cursor()
    fetch_query = f"""
    SELECT question_id, question, answer, test_date
    FROM user_{user_id}
    ORDER BY test_date DESC, question_id ASC
    LIMIT 20
    """
    cursor.execute(fetch_query)
    results = cursor.fetchall()
    return results

def compare_tests(test1, test2):
    comparison = []
    for (qid1, q1, a1, _), (qid2, q2, a2, _) in zip(test1, test2):
        if qid1 == qid2 and q1 == q2:
            comparison.append((q1, a1, a2))
    return comparison

def read_lines(file_path, num_lines):
    lines = []
    with open(file_path, 'r') as file:
        for _ in range(num_lines):
            line = file.readline()
            if not line:
                break
            lines.append(line.strip())
    return lines

pre_teen=read_lines(r'C:\Users\Admin\Desktop\questions.txt',18)
teen=read_lines(r'C:\Users\Admin\Desktop\questions.txt',36)
y_adult=read_lines(r'C:\Users\Admin\Desktop\questions.txt',54)
adult=read_lines(r'C:\Users\Admin\Desktop\questions.txt',72)
o_adult=read_lines(r'C:\Users\Admin\Desktop\questions.txt',90)
old=read_lines(r'C:\Users\Admin\Desktop\questions.txt',108)

ans=[]#diff file

sol1=read_lines(r'C:\Users\Admin\Desktop\solutions.txt',3)
sol2=read_lines(r'C:\Users\Admin\Desktop\solutions.txt',21)
sol3=read_lines(r'C:\Users\Admin\Desktop\solutions.txt',42)

# Introductions
print("Hi there! I hope you're doing okay.")
print("It's great that you're taking this step—it shows a lot of strength and self-awareness.")
print("Remember, this test is just a tool to help understand how you're feeling, and there's no judgment in whatever the results may be.")
print("Take your time, and know that support is always available.")

# Input data of person
name=input('Enter your name: ')
gender=input('Enter your gender: ')
age=int(input('Enter your age: '))

# Generate user ID
user_id = generate_user_id()
print(f"Your User ID is: {user_id}")

# Questionnaire based on age group
questions = []
if age >= 12 and age <= 14:
    questions = pre_teen[4:]
elif age >= 15 and age <= 17:
    questions = teen[22:]
elif age >= 18 and age <= 26:
    questions = y_adult[40:]
elif age >= 27 and age <= 36:
    questions = adult[58:]
elif age >= 37 and age <= 45:
    questions = o_adult[76:]
else:
    questions = old[93:]

for question in questions:
    print(question)
    print("1: Never, 2: Sometimes, 3: Often, 4: Always")
    ch = int(input('Enter option: '))
    while ch > 4 or ch < 1:
        ch = int(input('Enter correct option: '))
    ans.append(ch)

slvl = sum(ans)
if slvl <= 30:
    print('\n' + '\n')
    print("Stress level: Normal")
    print('\n' + '\n')
    for i in range(len(sol1)):
        print(sol1[i])
elif slvl >= 31 and slvl <= 45:
    print('\n' + '\n')
    print("Stress level: Elevated (Manageable)")
    print('\n' + '\n')
    for i in range(6, len(sol2)):
        print(sol2[i])
elif slvl >= 46 and slvl <= 60:
    print('\n' + '\n')
    print("Stress level: High")
    print('\n' + '\n')
    for i in range(24, len(sol3)):
        print(sol3[i])

# Connect to MySQL and create user table
connection = connect_to_db()
create_user_table(connection, user_id)
insert_user_answers(connection, user_id, questions, ans)

# Fetch and compare latest two tests
latest_tests = fetch_latest_two_tests(connection, user_id)
if len(latest_tests) >= 20:
    test1 = latest_tests[:len(latest_tests)//2]
    test2 = latest_tests[len(latest_tests)//2:]
    comparison = compare_tests(test1, test2)
    print("\nComparison of latest two tests:")
    print("Question | Previous Answer | Current Answer")
    for question, prev_answer, curr_answer in comparison:
        print(f"{question} | {prev_answer} | {curr_answer}")

# Ask user if they want to see the answers
show_answers = input("Would you like to see your answers? (yes/no): ").strip().lower()
if show_answers == 'yes':
    cursor = connection.cursor()
    fetch_query = f"SELECT * FROM user_{user_id};"
    cursor.execute(fetch_query)
    user_answers = cursor.fetchall()
    print("\nUser Answers Table:")
    print("question_id | question | answer")
    for row in user_answers:
        print(row)

connection.close()
