import requests


class WebLib:
    def __init__(self, department, course_number):
        url = 'https://www.reg.uci.edu/perl/WebSoc'
        form = {
            'YearTerm': '2017-92',
            'ShowComments': '',
            'ShowFinals': 'on',
            'Breadth': 'ANY',
            'Dept': department,
            'CourseNum': course_number,
            'Division': 'ANY',
            'CourseCodes': '',
            'InstrName': '',
            'CourseTitle': '',
            'ClassType': 'ALL',
            'Units': '',
            'Days': '',
            'StartTime': '',
            'EndTime': '',
            'MaxCap': '',
            'FullCourses': 'ANY',
            'CancelledCourses': 'Exclude',
            'Bldg': '',
            'Room': '',
            'Submit': 'Display Text Results',
        }
        self.response = requests.post(url, form).text
