import json

with open("db.json") as db_file:
    db = json.loads(db_file.read())
db_users = db["usernames"]
db_roles = db["roles"]
db_info = db["info"]
db_courses = db["courses"]


class Teacher:
    def __init__(self, username):
        self.username = username
        self.main_menu()
        self.lead_subject = []

    def update_db(self):
        db["usernames"].update(db_users)
        db["roles"].update(db_roles)
        db["info"].update(db_info)
        db["courses"].update(db_courses)
        with open("db.json", "w") as file:
            json.dump(db, file, indent=4)

    def add_students(self, course_name):
        student_username = input("Enter student username: ")
        if student_username not in db_users:
            print("Such username doesn't exist")
            return

        if student_username in db_courses[course_name]["students_enrolled"]:
            print("This user already enrolled in this course")
            return

        if db_roles[student_username] != "student":
            print("This username role is not student")
            return

        if db_courses[course_name]["places"] == 0:
            print("No available places. Update course info to update number of places")
            return

        db_courses[course_name]["students_enrolled"].append(student_username)
        db_courses[course_name]["places"] -= 1
        self.update_db()

    def delete_student(self, course_name):
        student_username = input("Enter student username: ")
        if student_username not in db_courses[course_name]["students_enrolled"]:
            print("Such user not enrolled to this course")
            return
        db_courses[course_name]["students_enrolled"].remove(student_username)
        if student_username in db_courses[course_name]["students_rating"]:
            del db_courses[course_name]["students_rating"][student_username]
        if student_username in db_courses[course_name]["attendance_list"]:
            del db_courses[course_name]["attendance_list"][student_username]
        if student_username in db_courses[course_name]["teachers_rating"]:
            del db_courses[course_name]["teachers_rating"][student_username]

        db_courses[course_name]["places"] += 1
        self.update_db()

    def rate_student(self, course_name):
        student_username = input("Enter student username: ")
        if student_username not in db_courses[course_name]["students_enrolled"]:
            print("Such user not enrolled to this course")
            return
        if student_username in db_courses[course_name]["students_rating"]:
            print("This student already evaluated. You can't evaluate student more than once!")
            return
        try:
            grade = float(input("Enter student grade: "))
        except ValueError:
            print("You should enter number")
            return
        if grade < 0 or grade > 100:
            print("Grade should be in range between 0 and 100")
            return
        db_courses[course_name]["students_rating"][student_username] = grade
        self.update_db()

    def see_students_in_course(self, course_name):
        if not db_courses[course_name]["students_enrolled"]:
            print("No such students enrolled")
            return
        cnt = 1
        print("Students list")
        for student_username in db_courses[course_name]["students_enrolled"]:
            print(f"{cnt}. {db_info[student_username]['fname']} {db_info[student_username]['lname']}")
            cnt += 1
        print()

    def take_attendance(self, course_name):
        if not db_courses[course_name]["students_enrolled"]:
            print("This course doesn't have students")
            return
        db_courses[course_name]["number_of_lessons"] += 1
        cnt = 1
        for student_username in db_courses[course_name]["students_enrolled"]:
            while True:
                attendance_value = input(f"{cnt}. {db_info[student_username]['fname']} "
                                         f"{db_info[student_username]['lname']}: present(p) or absent(a): ")
                if attendance_value == "p":
                    if student_username in db_courses[course_name]["attendance_list"]:
                        db_courses[course_name]["attendance_list"][student_username] += 1
                    else:
                        db_courses[course_name]["attendance_list"][student_username] = 1
                    break
                elif attendance_value == "a":
                    if student_username not in db_courses[course_name]["attendance_list"]:
                        db_courses[course_name]["attendance_list"][student_username] = 0
                    break
                else:
                    print("Incorrect syntax")
            cnt += 1
        self.update_db()

    def adjust_course(self):
        print("Your current lead subjects:")
        self.subject_lead()
        if not self.lead_subject:
            return
        try:
            course_num = int(input("Enter number of course you want to configure: "))
        except ValueError:
            print("You should input number")
            return
        if course_num < 1 or course_num > len(self.lead_subject):
            print("Number not within a range")
            return
        course_name = self.lead_subject[course_num-1]
        if course_name not in db_courses:
            print("Incorrect input")
            return
        while True:
            print("What do you want to do in this course?")
            print("1. Take attendance")
            print("2. Add student to this course")
            print("3. Delete student from this course")
            print("4. Rate student in this course")
            print("5. See students in this course")
            print("6. Go back")
            decision = input("Enter number: ")
            if decision == "1":
                self.take_attendance(course_name)
            elif decision == "2":
                self.add_students(course_name)
            elif decision == "3":
                self.delete_student(course_name)
            elif decision == "4":
                self.rate_student(course_name)
            elif decision == "5":
                self.see_students_in_course(course_name)
            elif decision == "6":
                return
            else:
                print("Incorrect input")

    def find_student(self):
        student_username = input("Enter student username: ")
        if student_username not in db_users:
            print("Such username doesn't exist")
            return

        if db_roles[student_username] != "student":
            print("This username role is not student")
            return
        for course_name in db_courses:
            if db_courses[course_name]["mentor"] == self.username:

                if student_username in db_courses[course_name]["students_enrolled"]:
                    print(course_name)




    def subject_lead(self):
        cnt = 1
        self.lead_subject = []
        for course_name in db_courses:
            if db_courses[course_name]["mentor"] == self.username:
                print(f"{cnt}. {course_name}")
                cnt += 1
                self.lead_subject.append(course_name)
        if cnt == 1:
            print("You don't lead any subjects")
            print()


    def main_menu(self):
        while True:
            print(10 * "*" + "MAIN MENU" + 10 * "*")
            print("1. See subject I lead")
            print("2. Adjust course")
            print("3. Find student")
            print("4. Log out")

            decision = input("Enter number: ")
            if decision == "1":
                self.subject_lead()
            elif decision == "2":
                self.adjust_course()
            elif decision == "3":
                self.find_student()
            elif decision == "4":
                break
            else:
                print("Incorrect input")
