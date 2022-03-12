import json

with open("db.json") as db_file:
    db = json.loads(db_file.read())
db_users = db["usernames"]
db_roles = db["roles"]
db_info = db["info"]
db_courses = db["courses"]

class Student:
    def __init__(self, username):
        self.username = username
        self.main_menu()
        self.enrolled_courses = []

    def update_db(self):
        db["usernames"].update(db_users)
        db["roles"].update(db_roles)
        db["info"].update(db_info)
        db["courses"].update(db_courses)
        with open("db.json", "w") as file:
            json.dump(db, file, indent=4)

    def see_enrolled_courses(self):
        self.enrolled_courses = []
        cnt = 1
        for course_name in db_courses:
            if self.username in db_courses[course_name]["students_enrolled"]:
                print(f"{cnt}. {course_name}")
                cnt += 1
                self.enrolled_courses.append(course_name)
                continue
        if cnt == 1:
            print("You don't have any enrolled courses")

    def unenroll_from_course(self):
        while True:
            print(10 * "*" + "Unenrollment Menu" + 10 * "*")
            self.see_enrolled_courses()
            if not self.enrolled_courses:
                print("You don't have any courses")
                return
            print(f"{len(self.enrolled_courses)+1}. Go back")
            try:
                course_num = int(input(f"Enter number: "))
            except ValueError:
                print("You should input integer")
                continue
            if course_num < 1 or course_num > (len(self.enrolled_courses) + 1):
                print("Should input number within a range")
                continue
            if course_num == (len(self.enrolled_courses) + 1):
                break
            else:
                course_name = self.enrolled_courses[course_num-1]
                db_courses[course_name]["students_enrolled"].remove(self.username)
                if self.username in db_courses[course_name]["students_rating"]:
                    del db_courses[course_name]["students_rating"][self.username]
                if self.username in db_courses[course_name]["attendance_list"]:
                    del db_courses[course_name]["attendance_list"][self.username]
                if self.username in db_courses[course_name]["teachers_rating"]:
                    del db_courses[course_name]["teachers_rating"][self.username]
                db_courses[course_name]["places"] += 1
                self.update_db()

    def see_all_grades(self):
        print("All grades")
        for course_name in self.enrolled_courses:
            if self.username not in db_courses[course_name]["students_rating"]:
                print(f"{course_name}: No grade for this course")
            else:
                print(f'{course_name}: {db_courses[course_name]["students_rating"][self.username]}')
        print()

    def see_grades(self):
        while True:
            self.see_enrolled_courses()
            if not self.enrolled_courses:
                print("You don't have any assigned courses")
                return
            print(f"{len(self.enrolled_courses)+1}. See grade of all courses")
            print(f"{len(self.enrolled_courses)+2}. Go back")
            try:
                course_num = int(input(f"Enter number: "))
            except ValueError:
                print("You should input integer")
                continue
            if course_num < 1 or course_num > (len(self.enrolled_courses)+2):
                print("Should input number within a range")
                continue
            if course_num == (len(self.enrolled_courses)+1):
                self.see_all_grades()
            elif course_num == (len(self.enrolled_courses)+2):
                break
            else:
                if self.username not in db_courses[self.enrolled_courses[course_num-1]]["students_rating"]:
                    print(f"{self.enrolled_courses[course_num-1]}: No grade for this course")
                else:
                    print(f'{self.enrolled_courses[course_num-1]}: '
                          f'{db_courses[self.enrolled_courses[course_num-1]]["students_rating"][self.username]}')

    def see_all_subject_attendance(self):
        print("Attendance")
        for course_name in self.enrolled_courses:
            if db_courses[course_name]["number_of_lessons"] == 0:
                print(f"{course_name}: This course didn't have any lessons yet")
            elif self.username not in db_courses[course_name]["attendance_list"]:
                print(f"{course_name}: You didn't visit any lessons yet. Attendance is 0%")
            else:
                attendance_rate = round(100 / db_courses[course_name]['number_of_lessons'] *
                                        db_courses[course_name]['attendance_list'][
                                            self.username], 2)
                print(
                    f"{course_name}: You visited {db_courses[course_name]['attendance_list'][self.username]} "
                    f"from {db_courses[course_name]['number_of_lessons']}. Attendace is {attendance_rate}%")
        print()

    def see_attendance(self):
        while True:
            self.see_enrolled_courses()
            if not self.enrolled_courses:
                print("You don't have any assigned courses")
                return
            print(f"{len(self.enrolled_courses) + 1}. See attendance of all courses")
            print(f"{len(self.enrolled_courses) + 2}. Go back")
            try:
                course_num = int(input(f"Enter number: "))
            except ValueError:
                print("You should input integer")
                continue
            if course_num < 1 or course_num > (len(self.enrolled_courses) + 2):
                print("Should input number within a range")
                continue
            if course_num == (len(self.enrolled_courses) + 1):
                self.see_all_subject_attendance()
            elif course_num == (len(self.enrolled_courses) + 2):
                break
            else:
                if db_courses[self.enrolled_courses[course_num - 1]]["number_of_lessons"] == 0:
                    print("This course doesn't have any lessons yet")
                elif self.username not in db_courses[self.enrolled_courses[course_num-1]]["attendance_list"]:
                    print("You didn't visit any lessons yet. Attendance is 0%")
                else:
                    attendance_rate = round(100/db_courses[self.enrolled_courses[course_num - 1]]['number_of_lessons'] * db_courses[self.enrolled_courses[course_num-1]]['attendance_list'][self.username], 2)
                    print(f"You visited {db_courses[self.enrolled_courses[course_num-1]]['attendance_list'][self.username]} "
                          f"from {db_courses[self.enrolled_courses[course_num - 1]]['number_of_lessons']}. Attendace is {attendance_rate}%")


    def teacher_courses(self, teacher_username):
        courses_names = []
        cnt = 1
        for course_name in db_courses:
            if db_courses[course_name]["mentor"] == teacher_username:
                print(f"{cnt}. {course_name}, Available places: {db_courses[course_name]['places']}")
                cnt += 1
                courses_names.append(course_name)
        if cnt == 1:
            print("This teacher currently doesn't have any courses")
            return

        print(f"{cnt}. Go back")
        try:
            course_num = int(input(f"Enter number of course you want to enroll: "))
        except ValueError:
            print("You should input integer")
            return
        if course_num < 1 or course_num > cnt:
            print("Should input number within a range")
            return
        if course_num == cnt:
            return
        else:
            self.enroll_to_course(courses_names[course_num-1])

    def see_teachers(self):
        teachers_usernames = []
        cnt = 1
        for username in db_roles:
            if db_roles[username] == "teacher":
                print(f"{cnt}. {db_info[username]['fname']} {db_info[username]['lname']}")
                cnt += 1
                teachers_usernames.append(username)
        print(f"{len(teachers_usernames)+1}. Go back")
        try:
            teacher_num = int(input("Enter number to see teacher courses: "))
        except ValueError:
            print("Input should be integer!")
            return
        if teacher_num == len(teachers_usernames)+1:
            return
        if teacher_num < 1 or teacher_num > len(teachers_usernames)+1:
            print("Should input number within a range")
            return
        self.teacher_courses(teachers_usernames[teacher_num-1])

    def enroll_to_course(self, course_name):
        if self.username in db_courses[course_name]["students_enrolled"]:
            print("You already enrolled in this course")
            return
        if db_courses[course_name]["places"] == 0:
            print("No available places")
            return
        db_courses[course_name]["places"] -= 1
        db_courses[course_name]["students_enrolled"].append(self.username)
        self.update_db()

    def see_free_courses(self):
        while True:
            courses_names = []
            cnt = 1
            for course_name in db_courses:
                print(f"{cnt}. {course_name}, Available places: {db_courses[course_name]['places']} ")
                courses_names.append(course_name)
                cnt += 1
            print(f"{cnt}. Go back")
            try:
                decision = int(input("Enter number of course you want to enroll: "))
            except ValueError:
                print("Input should be integer")
                continue

            if decision == cnt:
                break
            elif decision > cnt or decision < 1:
                print("Number not within a range")
                continue
            self.enroll_to_course(courses_names[decision-1])

    def rate_teacher(self):
        while True:
            self.see_enrolled_courses()
            if not self.enrolled_courses:
                print("You don't have any courses")
                return
            print(f"{len(self.enrolled_courses) + 1}. Go back")
            try:
                course_num = int(input(f"Enter number of course you want ro rate: "))
            except ValueError:
                print("You should input integer")
                continue

            if course_num < 1 or course_num > (len(self.enrolled_courses) + 1):
                print("Should input number within a range")
                continue
            if course_num == (len(self.enrolled_courses) + 1):
                break
            else:
                course_name = self.enrolled_courses[course_num-1]
                if self.username in db_courses[course_name]["teachers_rating"]:
                    print("You already rate teacher of this course")
                else:
                    try:
                        rate = float(input("Enter teacher grade: "))
                    except ValueError:
                        print("You should enter number")
                        continue
                    if rate < 0 or rate > 100:
                        print("Grade should be in range between 0 and 100")
                        continue
                    db_courses[course_name]["teachers_rating"][self.username] = rate
                    self.update_db()

    def main_menu(self):
        while True:
            print(10 * "*" + "MAIN MENU" + 10 * "*")
            print("1. See courses you enrolled")
            print("2. See grades")
            print("3. See teachers")
            print("4. See courses to enroll")
            print("5. Unenroll from course")
            print("6. Rate teacher")
            print("7. See attendance")
            print("8. Log out")
            decision = input("Enter number: ")
            if decision == "1":
                self.see_enrolled_courses()
            elif decision == "2":
                self.see_grades()
            elif decision == "3":
                self.see_teachers()
            elif decision == "4":
                self.see_free_courses()
            elif decision == "5":
                self.unenroll_from_course()
            elif decision == "6":
                self.rate_teacher()
            elif decision == "7":
                self.see_attendance()
            elif decision == "8":
                break
            else:
                print("Incorrect input")
