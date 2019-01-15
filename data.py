## Input data

from classes import TimeStringUtils, SemesterInfo, Timeslot, AltTimeslot, Course

semester_info = SemesterInfo(firstweek_day='7/Jan/2019',
                             lastweek_day='8/Apr/2019',
                             last_day='12/Apr/2019',
                             breakweek_day='4/Mar/2019',
                             holidays=[])

courses = []

inf3610 = Course(name='Systèmes embarqués',
                 cid='INF3610',
                 lectures=[Timeslot(day='Monday',
                                    start='0830',
                                    duration=3,
                                    room='M-2203')],
                 lab=AltTimeslot(day='Friday',
                                 start='0830',
                                 duration=3,
                                 room='L-3712',
                                 week='B1'))

inf4420a = Course(name='Sécurité informatique',
                  cid='INF4420A',
                  lectures=[Timeslot(day='Wednesday',
                                     start='1445',
                                     duration=3,
                                     room='M-1510')],
                  lab=AltTimeslot(day='Thursday',
                                  start='1345',
                                  duration=3,
                                  room='L-4712',
                                  week='B1'))

inf8480 = Course(name='Syst répartis et infonuagique',
                 cid='INF8480',
                 lectures=[Timeslot(day='Friday',
                                    start='0830',
                                    duration=3,
                                    room='M-1010')],
                 lab=AltTimeslot(day='Tuesday',
                                 start='1545',
                                 duration=3,
                                 room='L-4712',
                                 week='B1'))

phs1102 = Course(name='Champs électromagnétiques',
                 cid='PHS1102',
                 lectures=[Timeslot(day='Monday',
                                    start='1130',
                                    duration=1,
                                    room='B-316.1'),
                           Timeslot(day='Wednesday',
                                    start='1245',
                                    duration=2,
                                    room='B-316.1')],
                 lab=Timeslot(day='Friday',
                              start='1245',
                              duration=3,
                              room='C-539.6'))

courses.append(inf3610)
courses.append(inf4420a)
courses.append(inf8480)
courses.append(phs1102)

if __name__ == '__main__':
    # tests
    print(semester_info.firstweek_day + inf4420a.lectures[0].start)
    print(TimeStringUtils.weekday('Friday'))
