import os
import matplotlib.pyplot as plt


def load_students():
    students = {}
    file_path = 'students.txt'
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if len(line) >= 4:
                student_id = line[:3].strip()
                name = line[3:].strip()
                students[name] = student_id
    return students


def load_assignments():
    assignments = {}
    file_path = 'assignments.txt'
    with open(file_path, 'r') as file:
        lines = file.readlines()

        for i in range(0, len(lines), 3):
            name = lines[i].strip()
            assignment_id = lines[i + 1].strip()
            weight = float(lines[i + 2].strip())
            assignments[assignment_id] = (name, weight)
    return assignments


def load_submissions():
    submissions = []
    submissions_dir = os.path.join(os.path.dirname(__file__), 'submissions')
    for file_name in os.listdir(submissions_dir):
        file_path = os.path.join(submissions_dir, file_name)
        with open(file_path, 'r') as file:
            line = file.read().strip()
            assignment_id, student_id, score = line.split('|')
            submissions.append((student_id.strip(), assignment_id.strip(), float(score.strip())))
    return submissions




def calculate_student_grade(students, assignments, submissions, student_name):
    if student_name not in students:
        return "Student not found"
    student_id = students[student_name]
    total_score = 0
    max_score = 0


    for student_id_sub, assignment_id, score in submissions:
        if student_id_sub == student_id:
            if assignment_id in assignments:
                _, weight = assignments[assignment_id]
                total_score += score * weight
                max_score += weight


    if max_score == 0:
        return "No submissions found for this student"
    return f"Grade: {round((total_score / max_score) * 100)}%"


def assignment_statistics(assignments, submissions, assignment_name):

    assignment_id = None

    for aid, (name, _) in assignments.items():
        if name == assignment_name:
            assignment_id = aid
            break

    if not assignment_id:
        return "Assignment not found"

    scores = [score for _, aid, score in submissions if aid == assignment_id]

    if not scores:
        return "No submissions found for this assignment"

    return f"Min: {min(scores)}%\nAvg: {sum(scores) / len(scores):.2f}%\nMax: {max(scores)}%"


def plot_histogram(assignments, submissions, assignment_name):
    assignment_id = None

    for aid, (name, _) in assignments.items():
        if name == assignment_name:
            assignment_id = aid
            break

    if not assignment_id:
        return "Assignment not found"

    scores = [score for _, aid, score in submissions if aid == assignment_id]

    if not scores:

        return "No submissions found for this assignment"

    plt.hist(scores, bins=[0, 25, 50, 75, 100])
    plt.title(f"Histogram for {assignment_name}")
    plt.xlabel("Score Ranges")
    plt.ylabel("Frequency")
    plt.show()
    return "Histogram displayed."


def main():
    students = load_students()
    assignments = load_assignments()
    submissions = load_submissions()

    while True:
        print("\n1. Student grade")
        print("2. Assignment statistics")
        print("3. Assignment graph")


        choice = input("\nEnter your selection: ").strip()

        if choice == "1":
            student_name = input("What is the student's name: ").strip()
            print(calculate_student_grade(students, assignments, submissions, student_name))
        elif choice == "2":
            assignment_name = input("What is the assignment name: ").strip()
            print(assignment_statistics(assignments, submissions, assignment_name))
        elif choice == "3":
            assignment_name = input("What is the assignment name: ").strip()
            print(plot_histogram(assignments, submissions, assignment_name))
        else:
            print("Invalid selection!")


if __name__ == "__main__":
    main()
