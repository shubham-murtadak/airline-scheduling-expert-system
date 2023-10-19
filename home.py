<<<<<<< HEAD
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

            print("Runway table created successfully with four runways.")

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
                    fuel_capacity INTEGER NOT NULL
                )
            ''')

            # Insert 10 planes with a fuel capacity of 1000
            for plane_number in range(1, 11):
                cursor.execute("INSERT INTO plane (plane_number, fuel_capacity) VALUES (?, ?)",
                            (plane_number, 1000))

            connection.commit()

            print("Plane table created successfully with 10 planes.")

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
                    distance INTEGER ,
                    plane_id INTEGER ,
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
                print("cargo table created succesfully ")


            except sqlite3.Error as err:
                print(f"Error: {err}")



    @Rule(AS.f << Flight(id=MATCH.id, destination=MATCH.destination, time=MATCH.time, distance=MATCH.distance))
    def schedule_flight(self, f, id, destination, time, distance):
        self.store_flight_in_database(id, destination, time, distance)
        # print(f"Flight {id} is scheduled from pune to {destination} at {time}")

    @Rule(AS.f << Cargo(id=MATCH.id, name=MATCH.name, destination=MATCH.destination))
    def schedule_cargo(self, f, id, name, destination):
        self.store_cargo_in_database(id,name,destination)
      
    @Rule(AS.f << showflight())
    def display_flights(self, f):
        print("Upcoming flights details are :")
        cursor.execute("SELECT * FROM flights ORDER BY time desc ")
        flights = cursor.fetchall()
        if flights:
            for flight in flights:
                print(f"Flight ID: {flight[0]},FROM :PUNE, Destination: {flight[1]}, Time: {flight[2]}")
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
                print(f"Flight ID: {flight[0]}, Destination: {flight[1]}, Time: {flight[2]}, cargo id:{flight[4]},cargo name:{flight[5]}")
        else:
            print("No flights found.")

        # Remove the fact to avoid triggering the rule again
        self.retract(f)
    @Rule(AS.f << assign_plane(plane_id=MATCH.plane_id, flight_id=MATCH.flight_id),
          plane('Available', plane_id=MATCH.plane_id, fuel_capacity=MATCH.fuel_capacity),
          Flight(id=MATCH.flight_id, time=MATCH.time))
    def assign_plane_to_flight(self, f, plane_id, flight_id, fuel_capacity, time):
        print(f"Flight {flight_id} is assigned Plane {plane_id} with fuel capacity {fuel_capacity}.")
        cursor.execute("UPDATE plane SET availability = 'Not Available' WHERE id = ?", (plane_id,))
        connection.commit()
        cursor.execute("UPDATE flights SET time = ? WHERE id = ?", ('Delayed', flight_id,))
        connection.commit()

    @Rule(AS.f << assign_runway(runway_id=MATCH.runway_id, flight_id=MATCH.flight_id),
          runway('Available', runway_id=MATCH.runway_id, length=MATCH.length),
          Flight(id=MATCH.flight_id, time=MATCH.time))
    def assign_runway_to_flight(self, f, runway_id, flight_id, length, time):
        print(f"Flight {flight_id} is assigned Runway {runway_id} with length {length}.")
        cursor.execute("UPDATE runway SET availability = 'Not Available' WHERE id = ?", (runway_id,))
        connection.commit()
        cursor.execute("UPDATE flights SET time = ? WHERE id = ?", ('Delayed', flight_id,))
        connection.commit()
    @Rule(AS.f << Flight(id=MATCH.id, destination=MATCH.destination, time=MATCH.time, distance=MATCH.distance),
      plane('Available', plane_id=MATCH.plane_id, fuel_capacity=MATCH.fuel_capacity),
      runway('Available', runway_id=MATCH.runway_id, length=MATCH.length))
    def schedule_flight(self, f, id, destination, time, distance, plane_id, fuel_capacity, runway_id, length):
        self.store_flight_in_database(id, destination, time, distance, plane_id, runway_id)
        print(f"Flight {id} is scheduled from PUNE to {destination} at {time} with Plane {plane_id} and Runway {runway_id}.")
        self.assign_plane_to_flight(id)
        self.assign_runway_to_flight(id)

        
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
                           (id, name,destination))

            connection.commit()
            print("Cargo information stored in the database.")

        except sqlite3.Error as err:
            print(f"Error: {err}")
    def assign_plane_to_flight(self, flight_id):
        # Rule to assign a plane to a flight
        self.declare(assign_plane(flight_id=flight_id))

    def assign_runway_to_flight(self, flight_id):
        # Rule to assign a runway to a flight
        self.declare(assign_runway(flight_id=flight_id))

if __name__ == "__main__":
    engine = GARUDA(db_file)
    engine.reset()
    print("Welcome to GARUDA ~ An expert system for airline scheduling ")
    print("Welcome to PUNE INTERNATIONAL AIRPORT")

    # Declare a flight and cargo based on user input
    while True:
        user_input = input("Enter |1.Enter Flight details, |2.Enter Cargo Details, |3.Schedule Flight and Cargo |4.show available flights |5.any other key to exit: ")

        if user_input == '1':
            id_input = input('Enter the id of flight: ')
            destination_input = input("Enter the destination for the flight: ")
            time_input = input('Enter time of flight in 24 hr format: ')
            distance_input = input(f"Enter distance of {destination_input} from pune airport: ")
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
         
        elif user_input=='3':
            engine.declare(schedule_flight_cargo())
            engine.run()
        elif user_input=='4':
            engine.declare(showflight())
            engine.run()
        else:
            break


=======
-- gui coming soon -----
>>>>>>> e667905b6b0fdb48efaef0bfb5bbef9948970724
