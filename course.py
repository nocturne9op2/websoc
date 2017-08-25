class Course:
    def __init__(self, header):
        self.header = header
        self.schedules = []

    def add_schedule(self, info_list):
        info_dict = {}
        tags = ['CCode', 'Typ', 'Sec', 'Unt', 'Instructor',
                'Day', 'Time', 'Place', 'Final', 'Max',
                'Enr', 'WL', 'Req', 'Nor', 'Rstr', 'Status']

        for tag, info in zip(tags, info_list):
            if tag in ['Instructor', 'Day', 'Time', 'Place']:
                info_dict[tag] = [info.strip()]
            else:
                info_dict[tag] = info.strip()

        self.schedules.append(info_dict)

    def add_extra(self, info_list):
        if len(info_list) in [1, 4]:
            self.schedules[-1]['Instructor'].append(info_list[0])

        if len(info_list) in [3, 4]:
            tags = ['Day', 'Time', 'Place']
            for tag, info in zip(tags, info_list[len(info_list) - 3:]):
                self.schedules[-1][tag].append(info)
