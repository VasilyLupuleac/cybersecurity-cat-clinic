import psycopg


class AppointmentStorage:
    def __init__(self, dbname, db_user, db_password):
        self.connection = psycopg.connect (
            dbname=dbname,
            user=db_user,
            password=db_password,
            host="127.0.0.1",
            autocommit=True
        )
        self.cursor = self.connection.cursor ()
        try:
            self.cursor.execute ( "CREATE DATABASE cat_clinic;", prepare=True )
        except psycopg.errors.DuplicateDatabase:
            pass

        # create table for taken times
        self.cursor.execute ( """CREATE TABLE IF NOT EXISTS reserved_times(
                id serial not null PRIMARY KEY,
                appointment_date date not null,
                slot_id int not null,
                username varchar(50) not null,
                doctor varchar(50) not null);""", prepare=True )

        self.cursor.execute ( """DROP TABLE IF EXISTS doctors;""" )
        self.cursor.execute ( """CREATE TABLE doctors(
                            id serial not null PRIMARY KEY,
                            name varchar(50) not null);""", prepare=True )

        self.cursor.execute ( """INSERT INTO doctors(name) VALUES(
                                'Vasilii Lupuliak'), ('Melinda Pozna'), ('Miruna Gherasim'), ('Anuj Rathee');""" )

        # create table for slots and times
        self.cursor.execute("""DROP TABLE IF EXISTS slots;""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS slots(
                                id serial not null PRIMARY KEY,
                                slottime varchar(5) not null);""", prepare=True)

        # fill slots with values from 9 to 17
        times = ['09'] + list ( map ( str, range ( 10, 17 ) ) )
        slots_to_insert = [f'{x}:{y}' for x in times for y in ['00', '30']]

        for slot in slots_to_insert:
            self.cursor.execute ( f"""INSERT INTO slots(slottime) VALUES(
                                    '{slot}');""", prepare=True)


    def check_doctor(self, doctor):
        check_doc = (f"""SELECT name FROM doctors 
                            WHERE name = '{doctor}';""")
        doc = self.cursor.execute(check_doc, prepare=True).fetchone()
        return doc
    def silly(self, new_slot):
        #print(self.cursor.execute ( f"""SELECT id FROM slots;""" ).fetchall ())

        return str(self.cursor.execute(f"""SELECT slots.id FROM slots WHERE slottime = '{new_slot[2:-2]}';""").fetchone())[1:-2]

    def reserve_time(self, username, doctor, new_date, new_slot):

        check_availability = (f"""SELECT COUNT(*) FROM reserved_times
                                    JOIN slots ON slots.id = reserved_times.slot_id
                                    WHERE appointment_date = '{new_date}' AND slottime = '{new_slot[2:-2]}' AND doctor = '{doctor}';""")
        if (self.cursor.execute(check_availability, prepare=True).fetchone () == 1):
            return False

        id = str(self.cursor.execute(f"""SELECT slots.id FROM slots WHERE slottime = '{new_slot[2:-2]}';""").fetchone())[1:-2]
        add_timeslot = (f"""INSERT INTO reserved_times(appointment_date, slot_id, username, doctor) VALUES(
                            '{new_date}',
                            {id},
                            '{username}',
                            '{doctor}');""")
        print(id)
        self.cursor.execute(add_timeslot, prepare=True)



    def getReservedTimes(self, doctor):
        get_sql = (f"""SELECT reserved_times.appointment_date, slots.slottime FROM reserved_times
                        JOIN slots ON reserved_times.slot_id = slots.id
                        WHERE doctor = '{doctor}';""")
        reserved_times = self.cursor.execute ( get_sql, prepare=True ).fetchall ()
        return reserved_times


    # get all appointments for one user
    def get_user_appointments(self, username):
        result = self.cursor.execute ( f"""SELECT reserved_times.appointment_date, slots.slottime FROM reserved_times
                                    JOIN slots ON reserved_times.slot_id = slots.id
                                    WHERE reserved_times.username = '{username}';""", prepare=True )
        return result.fetchall()


    # all available appointments in one day for one doctor
    def get_appointments_day(self, doctor, date):
        result = self.cursor.execute(f"""SELECT slottime FROM slots
                                EXCEPT (
                                SELECT slots.slottime FROM reserved_times
                                JOIN slots ON reserved_times.slot_id = slots.id
                                WHERE doctor = '{doctor}'
                                AND appointment_date = '{date}');""", prepare=True).fetchall()

        return sorted(result)


    # days in one month for one doctor that have available slots
    def date_is_available(self, doctor, day):
        result = self.cursor.execute ( f"""SELECT COUNT(*) from reserved_times
                                WHERE doctor = '{doctor}' AND appointment_date = '{day}';""" ).fetchone ()
        return result < 16


if __name__ == '__main__':
    appointments = AppointmentStorage ( 'cat_clinic', 'postgres', 'nghtwsh12')
    print(appointments.get_appointments_day('Miruna Gherasim', '2022-01-01'))
    print(appointments.silly("['10:00']"))
    appointments.reserve_time("cat3", "Miruna Gherasim", "2000-01-01", "['10:00']")