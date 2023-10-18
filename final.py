from experta import KnowledgeEngine, Fact, Rule, AS, MATCH
import sqlite3

db_file = 'flight_schedule3.db'
connection = sqlite3.connect(db_file)
cursor = connection.cursor()

class Flight(Fact):
    pass

class Cargo(Fact):
    pass

class plane(Fact):
    pass

class runway(Fact):
    pass

class showflight(Fact):
    pass

class schedule_flight_cargo(Fact):
    pass

class assign_plane(Fact):
    pass

class assign_runway(Fact):
    pass

class fuel(Fact):
    pass

class GARUDA(KnowledgeEngine):
    def __init__(self, db_file):
        super().__init__()
        self.db_file = db_file

        # Create flights table if not exists
        self.create_flights_table()
        self.create_cargo_table()
        self.create_runway_table()
        self.create_plane_table()

    def create_runway_table(self):
        try:
            # Drop existing tables if they exist
            cursor.execute('DROP TABLE IF EXISTS runway;')

            # Create runway table if not exists
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS runway (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    runway_number INTEGER NOT NULL,
                    length INTEGER NOT NULL,
                    availability TEXT NOT NULL
                )
            ''')

            # Insert four runways with fixed length and availability
            for runway_number in range(1, 5):
                cursor.execute("INSERT INTO runway (runway_number, length, availability) VALUES (?, ?, ?)",
                               (runway_number, 2000, 'Available'))

            connection.commit()

            # print("Runway table created successfully with four runways.")

        except sqlite3.Error as err:
            print(f"Error: {err}")

    def create_plane_table(self):
        try:
            # Drop existing tables if they exist
            cursor.execute('DROP TABLE IF EXISTS plane;')

            # Create plane table if not exists
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS plane (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    plane_number INTEGER NOT NULL,
                    fuel_capacity INTEGER NOT NULL,
                    availability TEXT NOT NULL
                )
            ''')

            # Insert 10 planes with a fuel capacity of 1000
            for plane_number in range(1, 11):
                cursor.execute("INSERT INTO plane (plane_number, fuel_capacity, availability) VALUES (?, ?, ?)",
                               (plane_number, 1000, 'Available'))

            connection.commit()

            # print("Plane table created successfully with 10 planes.")

        except sqlite3.Error as err:
            print(f"Error: {err}")

    def create_flights_table(self):
        try:
            # Drop existing tables if they exist
            cursor.execute('DROP TABLE IF EXISTS flights;')

            # Create flights table if not exists
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS flights (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    destination TEXT NOT NULL,
                    time TEXT NOT NULL,
                    distance INTEGER,
                    plane_id INTEGER,
                    runway_id INTEGER
                )
            ''')

            connection.commit()

        except sqlite3.Error as err:
            print(f"Error: {err}")

    def create_cargo_table(self):
        try:
            # Drop existing tables if they exist
            cursor.execute('DROP TABLE IF EXISTS cargo;')

            # Create flights table if not exists
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS cargo (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    destination TEXT NOT NULL
                )
            ''')

            connection.commit()
            # print("Cargo table created successfully.")

        except sqlite3.Error as err:
            print(f"Error: {err}")
    @Rule(AS.f<<fuel(distance=MATCH.distance))
    def fuel_check(self,f,distance):
        print("fuell is invoke")
        if(distance>2000):
            print("insufficient fuel please add extra fuel to plane ")
        
    @Rule(AS.f << Flight(id=MATCH.id, destination=MATCH.destination, time=MATCH.time, distance=MATCH.distance))

    def schedule_flight(self, f, id, destination, time, distance):
        plane_id = self.assign_plane_to_flight()
        runway_id = self.assign_runway_to_flight()
        self.store_flight_in_database(id, destination, time, distance, plane_id, runway_id)
        print(f"Flight {id} is scheduled from PUNE to {destination} at {time} with Plane {plane_id} and Runway {runway_id}.")
        if(distance>2000):
            print("insufficient fuel please add extra fuel to plane ")
        

    @Rule(AS.f << Cargo(id=MATCH.id, name=MATCH.name, destination=MATCH.destination))
    def schedule_cargo(self, f, id, name, destination):
        self.store_cargo_in_database(id, name, destination)

    @Rule(AS.f << showflight())
    def display_flights(self, f):
        print("Upcoming flights details are :")
        cursor.execute("SELECT * FROM flights ORDER BY time desc ")
        flights = cursor.fetchall()
        if flights:
            for flight in flights:
                print(f"Flight ID: {flight[0]}, FROM: PUNE, Destination: {flight[1]}, Time: {flight[2]}, Plane ID: {flight[4]},Runway ID: {flight[5]}")
        else:
            print("No flights found.")
    @Rule(AS.f <<schedule_flight_cargo())
    def schedule_fc(self,f):
          print("schedule flight with cargo are as follows :")
          cursor.execute("SELECT * FROM flights t1 JOIN cargo t2 on t1.destination=t2.destination ")
          flights=cursor.fetchall()
          # Display the data
          if flights:
              for flight in flights:
                  print(f"Flight ID: {flight[0]}, Destination: {flight[1]}, Time: {flight[2]}, cargo id:{flight[6]},cargo name:{flight[7]}")
          else:
              print("No flights found.")

          # Remove the fact to avoid triggering the rule again
          # self.retract(f)       

    def get_plane_info(self, plane_id):
        cursor.execute("SELECT * FROM plane WHERE id = ?", (plane_id,))
        plane_info = cursor.fetchone()
        return f"Plane Number: {plane_info[1]}, Fuel Capacity: {plane_info[2]}"

    def get_runway_info(self, runway_id):
        cursor.execute("SELECT * FROM runway WHERE id = ?", (runway_id,))
        runway_info = cursor.fetchone()
        return f"Runway Number: {runway_info[1]}, Length: {runway_info[2]}"

    def assign_plane_to_flight(self):
        # Rule to assign a plane to a flight
        cursor.execute("SELECT * FROM plane WHERE availability = 'Available' LIMIT 1")
        plane_info = cursor.fetchone()
        if plane_info:
            plane_id = plane_info[0]
            cursor.execute("UPDATE plane SET availability = 'Not Available' WHERE id = ?", (plane_id,))
            connection.commit()
            return plane_id
        else:
            print("No available planes.")
            return None

    def assign_runway_to_flight(self):
        # Rule to assign a runway to a flight
        cursor.execute("SELECT * FROM runway WHERE availability = 'Available' LIMIT 1")
        runway_info = cursor.fetchone()
        if runway_info:
            runway_id = runway_info[0]
            cursor.execute("UPDATE runway SET availability = 'Not Available' WHERE id = ?", (runway_id,))
            connection.commit()
            return runway_id
        else:
            print("No available runways.")
            return None

    def store_flight_in_database(self, id, destination, time, distance, plane_id, runway_id):
        try:
            # Insert flight information into the database
            cursor.execute("INSERT INTO flights (id, destination, time, distance, plane_id, runway_id) VALUES (?, ?, ?, ?, ?, ?)",
                           (id, destination, time, distance, plane_id, runway_id))

            connection.commit()
            print("Flight information stored in the database.")

        except sqlite3.Error as err:
            print(f"Error: {err}")

    def store_cargo_in_database(self, id, name, destination):
        try:
            # Insert cargo information into the database
            cursor.execute("INSERT INTO cargo (id, name,destination) VALUES (?,  ?, ?)",
                           (id, name, destination))

            connection.commit()
            print("Cargo information stored in the database.")

        except sqlite3.Error as err:
            print(f"Error: {err}")



if __name__ == "__main__":
    engine = GARUDA(db_file)
    engine.reset()
    
    print(""" 
                             ,-.  ,.  ,-.  .  . ,-.   ,.  
                            /    /  \ |  ) |  | |  \ /  \ 
                            | -. |--| |-<  |  | |  | |--| 
                            \  | |  | |  \ |  | |  / |  | 
                             `-' '  ' '  ' `--` `-'  '  ' 
          
                         An expert system for airline scheduling 
                              PUNE INTERNATIONAL AIRPORT
        """)
    
   
    # Declare a flight and cargo based on user input
    while True:
        user_input = input("Enter |1.Enter Flight details, |2.Enter Cargo Details, |3.Schedule Flight and Cargo "
                           "|4.show available flights |5.any other key to exit: ")

        if user_input == '1':
            id_input = int(input('Enter the id of flight: '))
            destination_input = input("Enter the destination for the flight: ")
            time_input = int(input('Enter time of flight in 24 hr format: '))
            distance_input = int(input(f"Enter distance of {destination_input} from pune airport: "))
            engine.declare(fuel(distance_input))
            engine.run()
            engine.declare(Flight(id=id_input, destination=destination_input, time=time_input, distance=distance_input))
            print(f"flight {id_input} is stored in database from pune to {destination_input} at time {time_input} ")
            engine.run()

        elif user_input == '2':
            id_input = input('Enter the id of cargo: ')
            name_input = input('Enter the name of cargo: ')
            destination_input = input("Enter the destination for the cargo: ")
            engine.declare(Cargo(id=id_input, name=name_input, destination=destination_input))
            print(f"kargo {name_input} is store in database with destination {destination_input}")
            engine.run()

        elif user_input == '3':
            engine.declare(schedule_flight_cargo())
            engine.run()
        elif user_input == '4':
            engine.declare(showflight())
            engine.run()
        else:
            break
