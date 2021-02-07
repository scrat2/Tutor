import kronos
import datetime
from lesson.models import Profiles, Lessons, Groups


@kronos.register('0 22 * * *')
def update_hour():
    finds = Lessons.objects.filter(date=datetime.date.today() - datetime.timedelta(1))
    for lesson in finds:
        group = Groups.objects.filter(lessonID=lesson)
        if group.count() > 1:
            try:
                group = group.get(teacher=True)
                teacher = group.profileID
                teacher.nbr_heure += 1
                teacher.save()
            except:
                print("ERROR : plusieurs teacher sur une lesson")
