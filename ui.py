from reprocess import ReProcess
from weblib import WebLib

from layout import layout_enr
from layout import layout_instructors
from lookup import lookup


class UI:
    def __init__(self):
        self.response = str
        self.courses = []

        self.main_loop()

    def main_loop(self):
        while True:
            args = input(">>> ").lower().split()
            if len(args) == 0:
                print("Invalid argument(s), type websoc for usage.")
                continue

            if args[0] == 'websoc':
                if len(args) > 3:
                    print("Invalid argument(s), type websoc for usage.")
                elif len(args) == 1:
                    print("Usage: websoc [department] [course number]")
                else:
                    args[1] = lookup(args[1])
                    if len(args) == 2:
                        self.send_request(args[1], '')
                    elif len(args) == 3:
                        self.send_request(args[1], args[2])

                    self.resolve_text(args[1])
                    self.display_courses(args)

            elif args[0] == 'quit':
                break
            else:
                print("Invalid argument(s), type websoc for usage.")

    def send_request(self, department, course_number):
        web_lib = WebLib(lookup(department), course_number)
        self.response = web_lib.response

    def resolve_text(self, department):
        text = open('web_content.txt', 'w')
        text.write(self.response)
        text.close()
        text = open('web_content.txt', 'r')
        re_process = ReProcess(text, department)
        self.courses = re_process.courses

    def display_courses(self, args):
        if len(self.courses) == 0:
            print("No course(s) found.")
        else:
            if len(args) == 2:
                print('')
                for course in self.courses:
                    print(course.header)
                print('')
            elif len(args) == 3:
                print('')
                for course in self.courses:
                    print(course.header)

                    for schedule in course.schedules:
                        print('     #{} {}  --  {} [{}/{}]+{}'.
                              format(schedule['CCode'],
                                     schedule['Typ'],
                                     layout_instructors(schedule['Instructor']),
                                     layout_enr(schedule['Enr']),
                                     schedule['Max'],
                                     schedule['WL']))

                        for i in range(len(schedule['Place'])):
                            print('                       {}, {} {}'
                                  .format(schedule['Place'][i],
                                          schedule['Day'][i],
                                          schedule['Time'][i]))

                        if schedule['Final'] == '':
                            print('')
                        else:
                            print('                         Final: {}\n'
                                  .format(schedule['Final']))


if __name__ == '__main__':
    UI()
