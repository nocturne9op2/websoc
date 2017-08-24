def layout_instructors(instructors) -> str:
    result = ''
    for instructor in instructors[:-1]:
        result += '{}; '.format(instructor)
    else:
        result += '{}'.format(instructors[-1])
    return result


def layout_enr(enr) -> str:
    return enr.split('/')[0] if '/' in enr else enr
