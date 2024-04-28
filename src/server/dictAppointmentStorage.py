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
        times = ['09'] + list(map(str, range(10, 17)))
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
        filter(lambda a: a.doctor == doctor and a.date == date and a.slot == slot,
               self.appointments)  # TODO
        self.appointments.append(Appointment(user=user, doctor=doctor, date=date, slot=slot))

    def date_is_available(self, doctor, date):
        apts = self.select(lambda a: (a.doctor == doctor and
                                      a.date == date),
                           lambda a: a.slot)
        return len(apts) < len(self.times)

    def get_user_appointments(self, user):
        return self.select(lambda a: a.user == user, self.appointments,
                           lambda a: (a.date, self.times[a.slot]))

    def get_appointments_day(self, doctor, day):
        day_appointments = self.select(lambda a: a.date == day and a.doctor == doctor,
                                       lambda a: a.slot)
        return [t for i, t in enumerate(self.times) if i not in day_appointments]
