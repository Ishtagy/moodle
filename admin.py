import json
from teacher import Teacher
from student import Student
import sys
try:
    with open("db.json") as db_file:
        db = json.loads(db_file.read())
except FileNotFoundError:
    print("Not found file")
    sys.exit()
db_users = db["usernames"]
db_roles = db["roles"]
db_info = db["info"]
db_courses = db["courses"]


class Admin:
    def __init__(self, username):
        self.username = username
        self.main_menu()

    def update_db(self):
        db["usernames"].update(db_users)
        db["roles"].update(db_roles)
        db["info"].update(db_info)
        db["courses"].update(db_courses)
        with open("db.json", "w") as file:
            json.dump(db, file, indent=4)

    def create_account(self):
        role = input("Enter account type: teacher(t) or student(s): ")
        if role != 's' and role != 't':
            print("Incorrect syntax")
            return self.create_account()
        if role == 's':
            role_type = "student"
        else:
            role_type = "teacher"

        fname = input("Enter first name: ")
        lname = input("Enter second name: ")

        while True:
            username = input("Enter username: ")
            if username in db_users:
                print("Such username already exist")
            else:
                break
        password = input("Enter password: ")
        db_users[username] = password
        db_roles[username] = role_type
        db_info[username] = {"fname": fname, "lname": lname}
        self.update_db()

    def update_account(self):
        username = input("Enter username of account: ")
        if username not in db_users:
            print("Such user don't exist")
            return
        while True:
            print("1. Change first name")
            print("2. Change last name")
            print("3. Change password")
            print("4. Change role of account")
            print("5. Go back")
            decision = input("Enter number: ")
            if decision == "1":
                fname = input("Enter new first name: ")
                db_info[username]["fname"] = fname
            elif decision == "2":
                lname = input("Enter new last name: ")
                db_info[username]["lname"] = lname
            elif decision == "3":
                password = input("Enter new password: ")
                db_users[username] = password
            elif decision == "4":
                role = input("Enter new role: teacher(t) or student(s): ")
                if role != 's' and role != 't':
                    print("Incorrect syntax")
                    continue
                if role == 's':
                    role_type = "student"
                else:
                    role_type = "teacher"
                db_roles[username] = role_type
            elif decision == "5":
                break
            else:
                print("Incorrect input ")
                continue
            self.update_db()

    def delete_account(self):
        username = input("Enter username of account you want to delete: ")
        if username not in db_users:
            print("Such user doesn't exist")
            return

        if username == self.username:
            print("Can't delete yourself")
            return

        if db_roles[username] == "student":
            for course_name in db_courses:

                if username in db_courses[course_name]["students_enrolled"]:
                    db_courses[course_name]["students_enrolled"].remove(username)
                    db_courses[course_name]["places"] += 1
                if username in db_courses[course_name]["students_rating"]:
                    del db_courses[course_name]["students_rating"][username]

                if username in db_courses[course_name]["teachers_rating"]:
                    del db_courses[course_name]["teachers_rating"][username]

                if username in db_courses[course_name]["attendance_list"]:
                    del db_courses[course_name]["attendance_list"][username]


        if db_roles[username] == "teacher":
            for course_name in db_courses:
                if username == db_courses[course_name]["mentor"]:
                    db_courses[course_name]["mentor"] = ""

        del db_users[username]
        del db_roles[username]
        del db_info[username]

        self.update_db()

    def adjust_account(self):
        while True:
            print("1. Create account")
            print("2. Update account")
            print("3. Delete account")
            print("4. Go back")
            decision = input("Enter number: ")
            if decision == "1":
                self.create_account()
            elif decision == "2":
                self.update_account()
            elif decision == "3":
                self.delete_account()
            elif decision == "4":
                break
            else:
                print("Incorrect input")

    def create_course(self):
        course_name = input("Enter course name: ")
        if course_name in db_courses:
            print("Course with this name already exist")
            return
        try:
            places = int(input("Enter number of places: "))
        except ValueError:
            print("You should input number")
            return
        if places < 0:
            print("Number of places shouldn't be negative number")
            return
        assigned_teacher = input("Enter username of assigned teacher to these course: ")
        if assigned_teacher not in db_users:
            print("Such users not exist")
            return
        if db_roles[assigned_teacher] != "teacher":
            print("This user is not teacher")
            return
        db_courses[course_name] = {"places": places, "mentor": assigned_teacher,
                                   "students_enrolled": [], "students_rating": {}, "teachers_rating": {},
                                   "number_of_lessons": 0, "attendance_list": {}}
        self.update_db()

    def update_course(self):
        course_name = input("Enter course name: ")
        if course_name not in db_courses:
            print("Such course doesn't exist")
            return
        while True:

            print("1. Change course name")
            print("2. Change number of free places")
            print("3. Change assigned teacher")
            print("4. Add student to this course")
            print("5. Go back")

            decision = input("Enter number: ")

            if decision == "1":
                new_course_name = input("Enter new course name: ")
                db_courses[new_course_name] = db_courses.pop(course_name)
                course_name = new_course_name
            elif decision == "2":
                try:
                    numbers_of_places = int(input("Enter new number of places: "))
                except ValueError:
                    print("Input should be number")
                    continue
                db_courses[course_name]["places"] = numbers_of_places
            elif decision == "3":
                new_teacher = input("Enter username of new teacher: ")
                if new_teacher not in db_users:
                    print("Such users not exist")
                    continue
                if db_roles[new_teacher] != "teacher":
                    print("This user is not teacher")
                    continue
                db_courses[course_name]["mentor"] = new_teacher
            elif decision == "4":
                student_username = input("Enter student username: ")
                if student_username in db_courses[course_name]["students_enrolled"]:
                    print("This user already enrolled in this course")
                    continue
                if student_username not in db_users:
                    print("Such username doesn't exist")
                    continue
                if db_roles[student_username] != "student":
                    print("This username role is not student")
                    continue
                if db_courses[course_name]["places"] == 0:
                    print("No available places. Update course info to increase number of places")
                    continue
                db_courses[course_name]["students_enrolled"].append(student_username)
                db_courses[course_name]["places"] -= 1
            elif decision == "5":
                break
            else:
                print("Incorrect input")
                continue
            self.update_db()

    def delete_course(self):
        course_name = input("Enter course name: ")
        if course_name not in db_courses:
            print("Such course doesn't exist")
            return
        del db_courses[course_name]
        self.update_db()


    def adjust_course(self):
        while True:
            print("1. Create course")
            print("2. Update course")
            print("3. Delete course")
            print("4. Return to main menu")
            decision = input("Enter number: ")
            if decision == "1":
                self.create_course()
            elif decision == "2":
                self.update_course()
            elif decision == "3":
                self.delete_course()
            elif decision == "4":
                return
            else:
                print("Incorrect input")

    def database_statistic(self):
        num_of_teachers = 0
        num_of_students = 0
        num_of_courses = len(db_courses)
        for username in db_roles:
            if db_roles[username] == "teacher":
                num_of_teachers += 1
            else:
                num_of_students += 1
        print("Database statistic")
        print(f"Number of students: {num_of_students}")
        print(f"Number of teachers: {num_of_teachers}")
        print(f"Number of courses: {num_of_courses}")

    def seeCourseAverage(self):
        for course in db_courses:
            cnt = 1
            sum = 0
            for num in db_courses[course]["teachers_rating"]:
                sum += db_courses[course]["teachers_rating"][num]
                cnt += 1
            if cnt == 1:
                print(f"The course {course} currently didn't evaluated")
            else:
                print(f"Course name: {course}, Assigned teacher: {db_courses[course]['mentor']}, Average rating: {sum/(cnt-1)}")

    def main_menu(self):
        while True:
            print(10 * "*" + "MAIN MENU" + 10 * "*")
            print("1. Adjust account")
            print("2. Adjust courses")
            print("3. See statistic of database")
            print("4. See course average rating")
            print("5. Log out")
            decision = input("Enter number: ")
            if decision == "1":
                self.adjust_account()
            elif decision == "2":
                self.adjust_course()
            elif decision == "3":
                self.database_statistic()
            elif decision == "4":
                self.seeCourseAverage()
            elif decision == "5":
                break
            else:
                print("Incorrect input")


def authentication():
    with open("db.json") as db_file:
        db_data = json.loads(db_file.read())

    user = input("Enter a username: ")
    if user == "exit":
        return
    password = input("Enter your password: ")
    users_data = db_data["usernames"]
    if user not in users_data:
        print("Incorrect login or password")
        return authentication()
    if users_data[user] != password:
        print("Incorrect login or password")
        return authentication()

    roles_data = db_data["roles"]

    if roles_data[user] == "student":
        Student(user)
    elif roles_data[user] == "teacher":
        Teacher(user)
    elif roles_data[user] == "admin":
        Admin(user)
    return authentication()


authentication()

# Task for the 20%
# Class admin have additional feature that provide see statistic of number of courses, teacher and student in database
# Also it have unique feature See course average rating. It provides course name it's assigned teacher and it's average rating
# Class teacher have feature so that he can enter in """modemode""" of specific course for user convenience.
# There he have additional feature see list of students enrolled in this course. Also it has method to search student
# between teacher lead courses. It will provide all courses in which this student enrolled. (only in courses in which teacher lead)
# Class student have feature to see attendance. In this section as well as in grades section student can see statistic
# of attendance in specific subject or attendance in all courses. Also in section see teachers there have unique feature
# to see teacher course and then if student desire in the same section it can enroll to them.




