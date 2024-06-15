import tkinter as tk
from tkinter import messagebox

# Global Variables
current_level = ""
questions = []
current_question_index = 0
points = 0
highest_scores = {"basic": 0, "intermediate": 0, "advanced": 0}
lowest_scores = {"basic": 0, "intermediate": 0, "advanced": 0}

def start_quiz(level):
    global current_level, points, current_question_index
    current_level = level
    points = 0
    current_question_index = 0
    load_questions(level)
    display_question()
    update_buttons_state(in_quiz=True)

def load_questions(level):
    global questions
    questions = []
    question_file = f"{level}_questions.txt"
    try:
        with open(question_file, "r") as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split(",")
                if len(parts) >= 3:  # Check if there are at least three parts (question, options, and answer)
                    question = parts[0]
                    options = [option.strip() for option in parts[1:5]]
                    answer = parts[-1].strip()
                    questions.append((question, options, answer))
                else:
                    print(f"Ignoring invalid line in {question_file}: {line}")
    except FileNotFoundError:
        messagebox.showerror("Error", f"Question file {question_file} not found.")
        reset_quiz()

def display_question():
    global current_question_index
    if current_question_index < len(questions):
        question_label.config(text=questions[current_question_index][0])
        for i, option in enumerate(questions[current_question_index][1]):
            option_buttons[i].config(text=option, state="normal")
        # Hide remaining buttons if there are fewer options than before
        for j in range(len(questions[current_question_index][1]), len(option_buttons)):
            option_buttons[j].config(text="", state="disabled")
        feedback_label.config(text="", fg="black")  # Reset feedback label
        var.set(-1)  # Reset radio button selection
        submit_button.config(state="normal")  # Enable submit button for the next question
        next_button.config(state="disabled")  # Disable next button until an answer is submitted

        # Show question and options in correct order
        question_label.pack()
        for btn in option_buttons:
            btn.pack()
        feedback_label.pack()
        submit_button.pack()

    else:
        quiz_finished()

def check_answer():
    global current_question_index, points
    selected_option = var.get()
    if selected_option == -1:
        messagebox.showerror("Error", "Please select an option.")
        return

    user_answer = selected_option
    correct_answer = int(questions[current_question_index][2]) - 1  # Adjust index for zero-based indexing
    if user_answer == correct_answer:
        points += 10
        feedback_label.config(text="Correct!", fg="green")
    else:
        correct_option = int(questions[current_question_index][2])
        feedback_label.config(text=f"Incorrect. Correct answer is {correct_option}", fg="red")

    # Disable option buttons after submitting answer
    for button in option_buttons:
        button.config(state="disabled")
    submit_button.config(state="disabled")  # Disable submit button after answer is checked
    next_button.config(state="normal")  # Enable next button

def next_question():
    global current_question_index
    current_question_index += 1
    display_question()

def quiz_finished():
    global score
    messagebox.showinfo("Quiz Finished", f"Your final score is: {points}.")
    level = current_level
    if points > highest_scores[level]:
        highest_scores[level] = points
        messagebox.showinfo("New High Score!", f"Congratulations! You achieved a new high score for {level} level.")
    if points < lowest_scores[level] or lowest_scores[level] == 0:
        lowest_scores[level] = points
        messagebox.showinfo("New Low Score!", f"Congratulations! You achieved a new low score for {level} level.")
    save_scores()
    reset_quiz()

def show_leaderboard():
    leaderboard_text = (f"Basic level:\n\tHighest Scores: {highest_scores['basic']} \n\tLowest Scores: {lowest_scores['basic']} \n\nIntermediate level:\n\tHighest Scores: {highest_scores['intermediate']} \n\tLowest Scores: {lowest_scores['intermediate']} \n\nAdvanced level:\n\tHighest Scores: {highest_scores['advanced']} \n\tLowest Scores: {lowest_scores['advanced']}")
    messagebox.showinfo("Leaderboard", leaderboard_text)

def load_scores():
    try:
        with open("highest_scores.txt", "r") as file:
            for line in file:
                level, score = line.strip().split(":")
                highest_scores[level] = int(score)
        with open("lowest_scores.txt", "r") as file:
            for line in file:
                level, score = line.strip().split(":")
                lowest_scores[level] = int(score)
    except FileNotFoundError:
        pass

def save_scores():
    with open("highest_scores.txt", "w") as file:
        for level, score in highest_scores.items():
            file.write(f"{level}:{score}\n")
    with open("lowest_scores.txt", "w") as file:
        for level, score in lowest_scores.items():
            file.write(f"{level}:{score}\n")

def update_buttons_state(in_quiz):
    if in_quiz:
        submit_button.pack()
        next_button.pack()
        for button in option_buttons:
            button.pack()
        leaderboard_button.pack_forget()
    else:
        leaderboard_button.pack(pady=10)

def reset_quiz():
    #hide all the quiz elements
    question_label.pack_forget()
    feedback_label.pack_forget()
    for btn in option_buttons:
        btn.pack_forget()
    submit_button.pack_forget()
    next_button.pack_forget()
    leaderboard_button.pack(pady=10)

    #show the quiz buttons
    basic_button.pack(pady=10)
    intermediate_button.pack(pady=10)
    advance_button.pack(pady=10)

# Create main window
root = tk.Tk()
root.title("Quiz App")
root.geometry("600x450")
root.configure(bg="#f0f0f0")

# Frames
level_frame = tk.Frame(root, bg="#f0f0f0")
level_frame.pack(pady=10)

quiz_frame = tk.Frame(root, bg="#f0f0f0")
quiz_frame.pack(pady=20)

# Level Buttons
basic_button = tk.Button(level_frame, text="Basic", width=10, command=lambda: start_quiz("basic"), bg="#4caf50", fg="white")
basic_button.pack(side=tk.LEFT , padx=5)

intermediate_button = tk.Button(level_frame, text="Intermediate", width=10, command=lambda: start_quiz("intermediate"), bg="#ff9800", fg="white")
intermediate_button.pack(side=tk.LEFT , padx=5)

advance_button = tk.Button(level_frame, text="Advanced", width=10, command=lambda: start_quiz("advanced"), bg="#2196f3", fg="white")
advance_button.pack(side=tk.LEFT , padx=5)

# Quiz Area
question_label = tk.Label(quiz_frame, text="", bg="#f0f0f0", font=("Arial", 12))
question_label.pack(pady=10)

option_buttons = []
var = tk.IntVar()
var.set(-1)
for i in range(4):  # Assuming maximum of 4 options per question
    button = tk.Radiobutton(quiz_frame, text="", variable=var, value=i, width=30, bg="#f0f0f0", font=("Arial", 10))
    button.pack(pady=5)
    option_buttons.append(button)

feedback_label = tk.Label(quiz_frame, text="", width=30, bg="#f0f0f0", font=("Arial", 10))
feedback_label.pack(pady=10)

# Submit Button
submit_button = tk.Button(quiz_frame, text="Submit", width=10, command=check_answer, bg="#009688", fg="white", font=("Arial", 10))
submit_button.pack()

# Next Button
next_button = tk.Button(root, text="Next", width=10, command=next_question, bg="#607d8b", fg="white", font=("Arial", 10))
next_button.pack()

# Leaderboard Button
leaderboard_button = tk.Button(root, text="Leaderboard", width=15, command=show_leaderboard, bg="#795548", fg="white", font=("Arial", 10))
leaderboard_button.pack(pady=10)

# Load scores from files
load_scores()

# Run the application
root.mainloop()
import tkinter as tk
from tkinter import messagebox

# Global Variables
current_level = ""
questions = []
current_question_index = 0
points = 0
highest_scores = {"basic": 0, "intermediate": 0, "advanced": 0}
lowest_scores = {"basic": 0, "intermediate": 0, "advanced": 0}

def start_quiz(level):
    global current_level, points, current_question_index
    current_level = level
    points = 0
    current_question_index = 0
    load_questions(level)
    display_question()
    update_buttons_state(in_quiz=True)

def load_questions(level):
    global questions
    questions = []
    question_file = f"{level}_questions.txt"
    try:
        with open(question_file, "r") as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split(",")
                if len(parts) >= 3:  # Check if there are at least three parts (question, options, and answer)
                    question = parts[0]
                    options = [option.strip() for option in parts[1:5]]
                    answer = parts[-1].strip()
                    questions.append((question, options, answer))
                else:
                    print(f"Ignoring invalid line in {question_file}: {line}")
    except FileNotFoundError:
        messagebox.showerror("Error", f"Question file {question_file} not found.")
        reset_quiz()

def display_question():
    global current_question_index
    if current_question_index < len(questions):
        question_label.config(text=questions[current_question_index][0])
        for i, option in enumerate(questions[current_question_index][1]):
            option_buttons[i].config(text=option, state="normal")
        # Hide remaining buttons if there are fewer options than before
        for j in range(len(questions[current_question_index][1]), len(option_buttons)):
            option_buttons[j].config(text="", state="disabled")
        feedback_label.config(text="", fg="black")  # Reset feedback label
        var.set(-1)  # Reset radio button selection
        submit_button.config(state="normal")  # Enable submit button for the next question
        next_button.config(state="disabled")  # Disable next button until an answer is submitted
    else:
        quiz_finished()

def check_answer():
    global current_question_index, points
    selected_option = var.get()
    if selected_option == -1:
        messagebox.showerror("Error", "Please select an option.")
        return

    user_answer = selected_option
    correct_answer = int(questions[current_question_index][2]) - 1  # Adjust index for zero-based indexing
    if user_answer == correct_answer:
        points += 10
        feedback_label.config(text="Correct!", fg="green")
    else:
        correct_option = int(questions[current_question_index][2])
        feedback_label.config(text=f"Incorrect. Correct answer is {correct_option}", fg="red")

    # Disable option buttons after submitting answer
    for button in option_buttons:
        button.config(state="disabled")
    submit_button.config(state="disabled")  # Disable submit button after answer is checked
    next_button.config(state="normal")  # Enable next button

def next_question():
    global current_question_index
    current_question_index += 1
    display_question()

def quiz_finished():
    global score
    messagebox.showinfo("Quiz Finished", f"Your final score is: {points}.")
    level = current_level
    if points > highest_scores[level]:
        highest_scores[level] = points
        messagebox.showinfo("New High Score!", f"Congratulations! You achieved a new high score for {level} level.")
    if points < lowest_scores[level] or lowest_scores[level] == 0:
        lowest_scores[level] = points
        messagebox.showinfo("New Low Score!", f"Congratulations! You achieved a new low score for {level} level.")
    save_scores()
    reset_quiz()

def show_leaderboard():
    leaderboard_text = f"Highest Scores:\nBasic: {highest_scores['basic']}\nIntermediate: {highest_scores['intermediate']}\nAdvanced: {highest_scores['advanced']}\n\nLowest Scores:\nBasic: {lowest_scores['basic']}\nIntermediate: {lowest_scores['intermediate']}\nAdvanced: {lowest_scores['advanced']}"
    messagebox.showinfo("Leaderboard", leaderboard_text)

def load_scores():
    try:
        with open("highest_scores.txt", "r") as file:
            for line in file:
                level, score = line.strip().split(":")
                highest_scores[level] = int(score)
        with open("lowest_scores.txt", "r") as file:
            for line in file:
                level, score = line.strip().split(":")
                lowest_scores[level] = int(score)
    except FileNotFoundError:
        pass

def save_scores():
    with open("highest_scores.txt", "w") as file:
        for level, score in highest_scores.items():
            file.write(f"{level}:{score}\n")
    with open("lowest_scores.txt", "w") as file:
        for level, score in lowest_scores.items():
            file.write(f"{level}:{score}\n")

def update_buttons_state(in_quiz):
    if in_quiz:
        submit_button.pack()
        next_button.pack()
        for button in option_buttons:
            button.pack()
        leaderboard_button.pack_forget()
    else:
        leaderboard_button.pack(pady=10)

def reset_quiz():
    level_frame.pack(pady=10)
    quiz_frame.pack(pady=10)
    basic_button.pack(pady=10)
    intermediate.button(pady=10)
    advance.button(pady=10)
    question_label.pack_forget()
    feedback_label(pady=10)
    for btn in option_buttons:
        btn.pack_forget()
    submit_button.pack_forget()
    next_button.pack_forget()
    leaderboard_button.pack(pady=10)

# Create main window
root = tk.Tk()
root.title("Quiz App")
root.geometry("600x450")
root.configure(bg="#f0f0f0")

# Frames
level_frame = tk.Frame(root, bg="#f0f0f0")
level_frame.pack(pady=10)

quiz_frame = tk.Frame(root, bg="#f0f0f0")
quiz_frame.pack(pady=10)

# Level Buttons
basic_button = tk.Button(level_frame, text="Basic", width=10, command=lambda: start_quiz("basic"), bg="#4caf50", fg="white")
basic_button.grid(row=0, column=0, padx=5)

intermediate_button = tk.Button(level_frame, text="Intermediate", width=10, command=lambda: start_quiz("intermediate"), bg="#ff9800", fg="white")
intermediate_button.grid(row=0, column=1, padx=5)

advance_button = tk.Button(level_frame, text="Advanced", width=10, command=lambda: start_quiz("advanced"), bg="#2196f3", fg="white")
advance_button.grid(row=0, column=2, padx=5)

# Quiz Area
question_label = tk.Label(quiz_frame, text="", bg="#f0f0f0", font=("Arial", 12))
question_label.pack()

option_buttons = []
var = tk.IntVar()
var.set(-1)
for i in range(4):  # Assuming maximum of 4 options per question
    button = tk.Radiobutton(quiz_frame, text="", variable=var, value=i, width=30, bg="#f0f0f0", font=("Arial", 10))
    button.pack(pady=5)
    option_buttons.append(button)

feedback_label = tk.Label(quiz_frame, text="", width=30, bg="#f0f0f0", font=("Arial", 10))
feedback_label.pack()

# Submit Button
submit_button = tk.Button(quiz_frame, text="Submit", width=10, command=check_answer, bg="#009688", fg="white", font=("Arial", 10))
submit_button.pack(pady=10)

# Next Button
next_button = tk.Button(root, text="Next", width=10, command=next_question, bg="#607d8b", fg="white", font=("Arial", 10))
next_button.pack(pady=10)

# Leaderboard Button
leaderboard_button = tk.Button(root, text="Leaderboard", width=15, command=show_leaderboard, bg="#795548", fg="white", font=("Arial", 10))
leaderboard_button.pack(pady=10)

# Load scores from files
load_scores()

# Run the application
root.mainloop()
