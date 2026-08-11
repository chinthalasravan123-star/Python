class Subjects:
    def __init__(self, marks):
        self.marks = marks

    def total_marks(self):
        return sum(self.marks)

    def percentage(self):
        if not self.marks:
            return 0
        total = self.total_marks()
        return total / len(self.marks)

    def grade(self):
        percent = self.percentage()
        if percent >= 90:
            return "A+"
        if percent >= 80:
            return "A"
        if percent >= 70:
            return "B"
        if percent >= 60:
            return "C"
        if percent >= 50:
            return "D"
        return "F"


def get_marks(subjects):
    marks = []
    for subject in subjects:
        while True:
            try:
                value = float(input(f"Enter marks for {subject}: ").strip())
                if value < 0 or value > 100:
                    raise ValueError("Marks must be between 0 and 100.")
                marks.append(value)
                break
            except ValueError as exc:
                print("Invalid input:", exc)
    return marks


def main():
    print("Student Grade Calculator")
    student_name = input("Enter student name: ").strip()
    subjects = ["CG", "CN", "DevOps", "DAA", "PPL"]
    marks = get_marks(subjects)
    student = Subjects(marks)

    total = student.total_marks()
    percent = student.percentage()
    grade = student.grade()

    print("\n--- Result ---")
    print(f"Student: {student_name}")
    for subject, mark in zip(subjects, marks):
        print(f"{subject}: {mark}")
    print(f"Total Marks: {total}/{len(subjects) * 100}")
    print(f"Percentage: {percent:.2f}%")
    print(f"Grade: {grade}")
  

if __name__ == "__main__":
    main()
