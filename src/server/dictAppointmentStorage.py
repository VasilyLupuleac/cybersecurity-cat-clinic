class Appointment:
    def __init__(self, user, doctor, date, slot):
        self.user = user
        self.doctor = doctor
        self.date = date
        self.slot = slot


class DictAppointmentStorage:
    def __init__(self):
        self.appointments = []
        self.doctors = ['Vasilii Lupuliak', 'Melinda Pozna', 'Miruna Gherasim', 'Anuj Rathee']
        times = list(map(str, range(11, 17)))
        self.slots = [f'{x}:{y}' for x in times for y in ['00', '30']]
        self.slot_by_time = {}
        for slot, time in enumerate(self.slots):
            self.slot_by_time[time] = slot

    def check_doctor(self, doctor):
        return doctor in self.doctors

    def select(self, filter_func, map_func):
        return sorted(list(map(map_func, filter(filter_func, self.appointments))))

    def reserve_time(self, doctor, user, date, time):
        slot = self.slot_by_time[time]
        if list(filter(lambda a: a.doctor == doctor and
                                 str(a.date) == str(date) and
                                 a.slot == slot,
                       self.appointments)):
            return False
        self.appointments.append(Appointment(user=user, doctor=doctor, date=date, slot=slot))
        return True

    def date_is_available(self, doctor, date):
        apts = self.select(lambda a: (a.doctor == doctor and
                                      str(a.date) == str(date)),
                           lambda a: a.slot)
        return len(apts) < len(self.slots)

    def get_user_appointments(self, user):
        return self.select(lambda a: a.user == user,
                           lambda a: (a.date, self.slots[a.slot], a.doctor))

    def get_appointments_day(self, doctor, day):
        for apt in self.appointments:
            print(apt.date, day, apt.date == day)
            print(apt.doctor, doctor, apt.doctor == doctor)
        day_appointments = self.select(lambda a: str(a.date) == str(day) and a.doctor == doctor,
                                       lambda a: a.slot)

        return [t for i, t in enumerate(self.slots) if i not in day_appointments]
