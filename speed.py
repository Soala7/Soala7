import time
import csv
import os

# Default scores if file is missing or empty
default_scores = {
    "soala": 3.5,
    "desmond": 3.8
}

csv_filename = 'time.csv'

try:
    # Load scores from CSV if it exists and has content
    scores = {}
    if os.path.exists(csv_filename) and os.path.getsize(csv_filename) > 0:
        with open(csv_filename, mode='r') as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip header
            scores = {row[0]: float(row[1]) for row in reader if row}
    else:
        # Create the file and add default scores
        with open(csv_filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Time"])
            for name, time_taken in default_scores.items():
                writer.writerow([name, time_taken])
        scores = default_scores.copy()

    # Start the typing test
    print("Welcome to the typing speed test!")
    print("You will be asked to type a sentence as fast as you can.")
    print("Let's begin!\n")

    sentence = "The quick brown fox jumps over the lazy dog"
    print(f"Type this sentence exactly:\n\n{sentence}\n")

    input("Press ENTER when you're ready...")

    start = time.time()
    typed = input("\nStart typing: ").capitalize()
    end = time.time()
    time_taken = round(end - start, 2)

    # Check if the sentence was typed correctly
    if typed.strip() != sentence:
        print("\n❌ You typed the sentence incorrectly. Try again!")
    else:
        name = input("\n✅ Well done! Now enter your name: ")
        print(f"You spent {time_taken} seconds typing the sentence.")

        # Save to CSV
        with open(csv_filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name, time_taken])
            scores[name] = time_taken

        # Find the fastest typer
        fastest = min(scores, key=scores.get)
        print(f"\n🏆 Fastest typer is {fastest} with {scores[fastest]} seconds!")

except FileNotFoundError as fnf_error:
    print(f"File not found: {fnf_error}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

