import csv
import matplotlib.pyplot as plt

# ------------------ Constants ------------------ #
ASSIGNMENT_SCORE = 5
GRADE_THRESHOLDS = [
    (30, "A", "Excellent"),
    (25, "B", "Very Good"),
    (20, "C", "Good"),
    (15, "D", "Fair"),
    (10, "E", "Pass"),
    (0,  "F", "Fail")
]
ADMIN_PASSWORD = "$0@/@.com#"

# ------------------ Data Loading and Saving ------------------ #
def load_students():
    students = {}
    try:
        with open('students_score.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 2 and row[1].isdigit():
                    students[row[0]] = int(row[1])
    except FileNotFoundError:
        students = {
            "Soala_Amachree": 97, "Desmond_Ozondu": 91, "Obasi_Princewill": 99,
            "Joshua_Eze-ochia": 90, "Christopher_Egere": 65, "Amadi_Greatman": 65,
            "Havilah_Oghenejivwe": 85, "Grace_Chitchuga": 95, "Redeemer_Messiah": 46,
            "Nwandike_Darlington": 75, "Aguma_Michelle": 60, "Jensen_Ogu": 45,
            "Nora_Messiah": 38, "Sarima_Ozondu": 40, "Onyesiuwe_Ella": 43,
            "Flourish_Obasi": 78, "Ibeya_Tekena": 50, "Lilian_Messiah": 64,
            "Melvin_Nick": 20, "Delight_Justice": 0, "Morenike_Abioye": 0, "Prasie_Ogu": 62,
            "Olayinka_Oghenejivwe": 87, "Chatem_Julia": 80, "Sarah_Ozondu": 67,
            "Francis_John": 74, "David_Ernsest": 72
        }
        save_students(students)
    return students

def save_students(students):
    with open('students_score.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        for name, score in students.items():
            writer.writerow([name, score])

# ------------------ Grading and Report Card ------------------ #
def input_score(subject_name):
    cat1 = float(input(f"{subject_name} CAT1: "))
    assignment_score = ASSIGNMENT_SCORE * 2 + cat1
    cat2 = float(input(f"{subject_name} CAT2: "))
    total = assignment_score + cat2
    for threshold, grade, remark in GRADE_THRESHOLDS:
        if total >= threshold:
            break
    return {
        "cat1": cat1, "cat2": cat2, "assignment": assignment_score,
        "total": total, "grade": grade, "remark": remark
    }

def calculate_average(scores):
    return sum(scores) / len(scores) if scores else 0

def generate_report_card(name, students):
    print(f"\nEntering scores for {name}:")
    math_subjects = ["Numbers/Algebra", "Geometry", "Further Math"]
    english_subjects = ["Grammar", "Elocution/Oral", "Literary Writing", "Lexis & Structure"]
    science_subjects = ["Chemistry", "Biology", "Physics", "Geography", "Data Processing"]
    arts_subjects = ["Economics", "Civic Education"]
    scores = {}

    for subject in math_subjects + english_subjects + science_subjects + arts_subjects:
        print(f"\n--- {subject} ---")
        scores[subject] = input_score(subject)

    agric = float(input("Agric Science CAT1 (0 if not offered): "))
    if agric != 0:
        print("\n--- Agric Science ---")
        scores["Agric Science"] = input_score("Agric Science")

    science_keys = science_subjects + (["Agric Science"] if "Agric Science" in scores else [])
    math_avg = calculate_average([scores[sub]["total"] for sub in math_subjects])
    english_avg = calculate_average([scores[sub]["total"] for sub in english_subjects])
    science_avg = calculate_average([scores[sub]["total"] for sub in science_keys])
    arts_avg = calculate_average([scores[sub]["total"] for sub in arts_subjects])
    overall_avg = calculate_average([math_avg, english_avg, science_avg, arts_avg])
    students[name] = overall_avg

    academic_remark = input("Academic Remark: ")
    behavioral_remark = input("Behavioral Remark: ")
    principal_remark = "Excellent performance, keep it up! Work on your weak areas."
    filename = f"{name}.csv"

    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", name])
        writer.writerow(["Class", "SS2"])
        writer.writerow(["Term", "Second Term"])
        writer.writerow(["Year", "2024"])
        writer.writerow(["Academics(cognitive)","ASS", "CW" ,"CA1", "CA1 Total","CAT2", "Total", "Grade", "Remark"])

        for section, subject_list in [
            ("English", english_subjects),
            ("Mathematics", math_subjects),
            ("Science", science_keys),
            ("Arts", arts_subjects)
        ]:
            writer.writerow([""])
            writer.writerow([section])
            for sub in subject_list:
                s = scores[sub]
                writer.writerow([sub, ASSIGNMENT_SCORE, ASSIGNMENT_SCORE, s["cat1"], s["assignment"], s["cat2"], s["total"], s["grade"], s["remark"]])
            section_avg = calculate_average([scores[sub]["total"] for sub in subject_list])
            writer.writerow(["", "", "", "", "", "CUM.A", section_avg])

        writer.writerow([""])
        writer.writerow([" ","Student's Overall Average(SOA):", f"{overall_avg:.2f}"])
        writer.writerow([""])
        writer.writerow(["Academic Remark", academic_remark])
        writer.writerow(["Behavioral Remark", behavioral_remark])
        writer.writerow(["Principal's Remark", principal_remark])

# ------------------ Stats and Admin ------------------ #
def rank_students(data):
    return sorted(data.items(), key=lambda x: x[1], reverse=True)

def show_histogram(data):
    scores = data.values()
    bins = {0:0, 50:0, 70:0, 90:0}
    for score in scores:
        if score >= 90: bins[90] += 1
        elif score >= 70: bins[70] += 1
        elif score >= 50: bins[50] += 1
        else: bins[0] += 1
    print("\nScore Distribution:")
    for threshold, count in sorted(bins.items()):
        print(f"{threshold}+: {'■' * count} ({count})")

def display_student_names(data):
    print("\nStudent Names:")
    for name in sorted(data):
        print(name)

def calculate_statistics(data):
    scores = data.values()
    print("\nClass Statistics:")
    print(f"Total: {len(data)}")
    print(f"Highest: {max(scores)}")
    print(f"Lowest: {min(scores)}")
    print(f"Average: {sum(scores)/len(scores):.2f}")

def is_admin():
    return input("Enter admin password: ") == ADMIN_PASSWORD

def student_performance_summary_graph(data):
    if not data:
        print("No student data to plot.")
        return

    names_scores = sorted(data.items(), key=lambda x: x[1])  # sort by score
    names = [ns[0].replace("_", " ") for ns in names_scores]
    scores = [ns[1] for ns in names_scores]

    # Define performance color bands
    colors = []
    for score in scores:
        if score >= 90:
            colors.append("green")     # Excellent
        elif score >= 70:
            colors.append("blue")      # Good
        elif score >= 50:
            colors.append("orange")    # Fair
        else:
            colors.append("red")       # Fail

    plt.figure(figsize=(12, max(6, len(scores) * 0.3)))
    bars = plt.barh(names, scores, color=colors)

    for bar, score in zip(bars, scores):
        plt.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                 f'{score:.1f}', va='center', fontsize=9)

    avg_score = sum(scores) / len(scores)
    plt.axvline(avg_score, color='purple', linestyle='--', linewidth=1.5, label=f'Class Avg: {avg_score:.2f}')

    plt.title('📊 Student Performance Summary', fontsize=16)
    plt.xlabel('Scores')
    plt.ylabel('Students')
    plt.grid(axis='x', linestyle=':', linewidth=0.5)
    plt.legend()
    plt.tight_layout()
    plt.show()

# ------------------ Menu ------------------ #
def main():
    students = load_students()
    while True:
        print("\n===== Student Management System =====")
        print("1. Enter new scores and generate report card")
        print("2. Check a student's score and ranking")
        print("3. View class statistics and histogram")
        print("4. View all student names")
        print("5. Add a new student manually")
        print("6. Delete all student records (Admin only)")
        print("7. Student's performance summary")
        print("8. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            name = input("Enter student name (First_Last): ")
            generate_report_card(name, students)
            save_students(students)
        elif choice == "2":
            first = input("Enter student's first name: ").capitalize()
            last = input("Enter student's last name: ").capitalize()
            name = first + "_"+ last
            name2 = last +"_"+ first
            if name in students or name2 in students:
                actual_name = name if name in students else name2
                print(f"{actual_name}'s score: {students[actual_name]}")
                for i, (student, _) in enumerate(rank_students(students), 1):
                    if student == actual_name:
                        print(f"Ranking: {i}")
                        break
            else:
                print("Student not found.")
        elif choice == "3":
            calculate_statistics(students)
            show_histogram(students)
        elif choice == "4":
            display_student_names(students)
        elif choice == "5":
            name = input("Enter new student's name (First_Last): ")
            try:
                score = int(input("Enter student's average score: "))
                students[name] = score
                save_students(students)
                print("Student added.")
            except ValueError:
                print("Invalid score.")
        elif choice == "6":
            if is_admin():
                students.clear()
                save_students(students)
                print("All records deleted.")
            else:
                print("Access denied.")
        elif choice == "7":
            print("Generating performance summary graph...")
            student_performance_summary_graph(students)
        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
# This code is a student management system that allows for entering scores, generating report cards,