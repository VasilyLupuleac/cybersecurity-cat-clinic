import psycopg

class appointmentStorage():
    def __init__(self):
        db_user = input("username for postgres: ")
        db_password = input("password for database: ")
        self.connection = psycopg.connect(
            dbname="postgres",
            user=db_user,
            password=db_password,
            host="localhost",
            autocommit=True
        )
        self.cursor = self.connection.cursor()
        try:
            self.cursor.execute("CREATE DATABASE cat_clinic;", prepare=True)
        except psycopg.errors.DuplicateDatabase:
            pass
        try:
            #create table for taken times
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS reserved_times(
                id serial not null PRIMARY KEY,
                appointment_date date not null,
                slot_id int not null,
                username varchar(50) not null,
                doctor varchar(50) not null);""", prepare=True)

            #create table for slots and times
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS slots(
                                id serial not null PRIMARY KEY,
                                slottime varchar(5) not null);""", prepare=True)

            #fill slots with values from 9 to 17
            times = ['09'] + list(map(str, range(10, 17)))
            slots_to_insert = [f'{x}:{y}' for x in times for y in ['00', '30']]
            for slot in slots_to_insert:
                self.cursor.execute(f"""INSERT INTO slots(slottime) VALUES(
                                    '{slot}');""", prepare=True)
        except:
            print("died")
            pass

    def reserveTime(self, username, doctor, new_date, new_slot):
        #TODO change
        check_availability = (f"""SELECT COUNT(*) FROM reserved_times
                                WHERE appointment_date = '{new_date}' AND slot_id = {new_slot} AND doctor = '{doctor}';""")
        if (self.cursor.execute(check_availability, prepare=True).fetchone() == 1):
            return False

        add_timeslot = (f"""INSERT INTO reserved_times(appointment_date, slot_id, username, doctor) VALUES(
	                    '{new_date}',
	                    {new_slot},
	                    '{username}',
	                    '{doctor}');""")
        self.cursor.execute(add_timeslot, prepare=True)



    def getReservedTimes(self, doctor):
        get_sql = (f"""SELECT reserved_times.appointment_date, slots.slottime FROM reserved_times
                    JOIN slots ON reserved_times.slot_id = slots.id
                    WHERE doctor = '{doctor}';""")
        reserved_times = self.cursor.execute(get_sql, prepare=True).fetchall()
        return reserved_times


    # get all appointments for one user
    def getUsersAppointments(self, username):
        result = self.cursor.execute(f"""SELECT reserved_times.appointment_date, slots.slottime FROM reserved_times
                                JOIN slots ON reserved_times.slot_id = slots.id
                                WHERE reserved_times.username = '{username}';""", prepare=True)
        return result.fetchall()


    #all available appointments in one day for one doctor
    def doctorAvailability(self, doctor):
        result = self.cursor.execute(f"""SELECT slottimes FROM slots
                            EXCEPT (
                            SELECT reserved_times.appointment_date, slots.slottime FROM reserved_times
                            JOIN slots ON reserved_times.slot_id = slots.id
                            WHERE doctor = '{doctor}');""", prepare=True)
        return result

    #days in one month for one doctor that have available slots
    def isDoctorAvailable(self, doctor, day):
        result = self.cursor.execute(f"""SELECT COUNT(*) from reserved_times
                            WHERE doctor = '{doctor}' AND appointment_date = '{day}';""").fetchone()
        return result < 16


if __name__ == '__main__':
    appointments = appointmentStorage()

