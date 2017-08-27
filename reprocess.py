import logging
import re

from course import Course


class ReProcess:
    def __init__(self, text, department):
        self.rough_courses = {}
        self.courses = []

        self.rough_process(text, department)
        self.re_match()

    def rough_process(self, text, department):
        inner_text = []
        count = 0

        for line in text:
            line = line.strip()
            if '_________________________________________________________________' in line:
                count += 1
            elif 'CCode' in line or '~' in line:
                continue
            elif 'Total Classes Displayed:' in line:
                break
            elif count == 2:
                inner_text.append(line)

        inner_text_iter = iter(inner_text)
        header = ''
        write_schedules = False

        while True:
            try:
                line = next(inner_text_iter)
            except StopIteration:
                break

            if write_schedules:
                if line == '':
                    write_schedules = False
                else:
                    schedule = line
                    self.rough_courses[header].append(schedule)
            elif department in line.lower():
                header = line
                self.rough_courses[header] = []
                write_schedules = True

    def re_match(self):
        patterns = {
            'full_schedule': re.compile(
                r'(\d*) *'
                r'(\w*) *'
                r'(\w*) *'
                r'([\d\-.]*) *'
                r'(STAFF|[^\d]*\.) *'
                r'(\w*) *'
                r'(\*TBA\*|[\d:]*- *[\d:]*\w*) *'
                r'(\*TBA\*|\w* \w*) {1,10}'
                r'(TBA|[\w,]* \w* [\d,]* [\d\-:]*\w*) *'
                r'(\d*) *'
                r'([\d/]*) *'
                r'([\w/()]*) *'
                r'(\d*) *'
                r'(\d*) {1,5}'
                r'([\w&]*) *'
                r'(\w*)'),
            'instructor_day_time_place': re.compile(
                r'(STAFF|[^\d]*\.) *'
                r'(\w*) *'
                r'(\*TBA\*|[\d:]*- *[\d:]*\w*) *'
                r'(\*TBA\*|\w* \w*)'),
            'day_time_place': re.compile(
                r'(\w*) *'
                r'(\*TBA\*|[\d:]*- *[\d:]*\w*) *'
                r'(\*TBA\*|\w* \w*)'),
            'instructor': re.compile(
                r'(STAFF|[^\d]*\.)')
        }

        for header, schedules in self.rough_courses.items():
            course = Course(header)

            for schedule in schedules:
                for name, pattern in patterns.items():
                    re_schedule = pattern.match(schedule)
                    if re_schedule:
                        if 'full_schedule' == name:
                            course.add_schedule(re_schedule.groups())
                        else:
                            course.add_extra(re_schedule.groups())
                        break
                else:
                    logging.error("Pattern not found for: {}".format(schedule))

            self.courses.append(course)
