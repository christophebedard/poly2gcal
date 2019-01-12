## Input data

from classes import TimeStringUtils, SemesterInfo, Timeslot, AltTimeslot, Course, Courses

semester_info = SemesterInfo(firstweek_day='7/Jan/2019',
                             lastweek_day='29/Apr/2019',
                             last_day='4/May/2019',
                             breakweek_day='4/Mar/2019')

courses = Courses()

inf3610 = Course(name='Systemes embarques',
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

inf4420a = Course(name='Securite informatique',
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

inf8480 = Course(name='Syst repartis et infonuagique',
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

inf8770 = Course(name='Technologies multimedias',
                 cid='INF8770',
                 lectures=[Timeslot(day='Monday',
                                    start='0830',
                                    duration=3,
                                    room='M-1420')],
                 lab=AltTimeslot(day='Thursday',
                                 start='1445',
                                 duration=3,
                                 room='L-3712',
                                 week='B2'))

phs1102 = Course(name='Champs electromagnetiques',
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

courses.add(inf3610)
courses.add(inf4420a)
courses.add(inf8480)
courses.add(inf8770)
courses.add(phs1102)

# tests
print(semester_info.firstweek_day + inf4420a.lectures[0].start)
print(TimeStringUtils.weekday('Friday'))
