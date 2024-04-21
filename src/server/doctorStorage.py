import psycopg

class doctorStorage():
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
            #create doctors table
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS doctors(
                id serial not null PRIMARY KEY,
                name varchar(50) not null,
                specialty varchar(100) not null,
                phone varchar(15);""", prepare=True)

            #create table for available times
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS doctor_times(
                id serial not null PRIMARY KEY,
                available timestamp not null);""", prepare=True)

            #join tables
            self.cursor.execute("""SELECT doctors.id
                                FROM doctors
                                JOIN doctor_times ON doctors.id = doctor_times.id;""", prepare=True)
        except:
            pass

    def addTime(self, doctor, new_time):


        #check if doctor exists
        check_doc = (f"""SELECT * FROM doctors 
                    WHERE doc_name = '{doctor}';""")
        result = self.cursor.execute(check_doc, prepare=True).fetchone()
        if result is None:
            return False

        add_timeslot = (f"""INSERT INTO doctor_times VALUES(
	                    id = (SELECT id FROM doctors WHERE name = '{name}'),
	                    available = '{new_time}');""")
        self.cursor.execute(add_timeslot, prepare=True)

    def getTimes(self, doctor):
        # check if doctor exists
        check_doc = (f"""SELECT * FROM doctors 
                            WHERE doc_name = '{doctor}';""")
        result = self.cursor.execute(check_doc, prepare=True ).fetchone()
        if result is None:
            return False

        get_sql = (f"""SELECT available FROM DOCTORS
                    WHERE doc_name = '{doctor}';""")
        free_times = self.cursor.execute(get_sql, prepare=True).fetchall()
        return free_times