from experta import KnowledgeEngine,Fact,Rule,AS, MATCH
import sqlite3

db_file='flight_schedule.db'
# print("jay hanuman dada ")

class flight_time(Fact):
  pass


class Flight(Fact):
    pass

class Cargo(Fact):
    pass


class GARUDA(KnowledgeEngine):
  def __init__(self, db_file):
        super().__init__()
        self.db_file = db_file

        # Create flights table if not exists
        self.create_flights_table()

  def create_flights_table(self):
        try:
            connection = sqlite3.connect(self.db_file)
            cursor = connection.cursor()
              # Drop existing tables if they exist
            cursor.execute('DROP TABLE IF EXISTS flights;')
            cursor.execute('DROP TABLE IF EXISTS cargo;')
            # Create flights table if not exists
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS flights (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source TEXT NOT NULL,
                    destination TEXT NOT NULL,
                    time TEXT NOT NULL
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS cargo (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    source TEXT NOT NULL,
                    destination TEXT NOT NULL
                 
                )
            ''')

            connection.commit()

        except sqlite3.Error as err:
            print(f"Error: {err}")

        finally:
            if connection:
                connection.close()     
  @Rule(flight_time('on_time'))
  def ailine_ontime(self):
    print("flight goint to take of on time !")

  @Rule(flight_time('delay'))
  def airline_delay(self):
    print("flight is delay due to certain issues please take a note of it !")

  @Rule(AS.f << Flight(id=MATCH.id,source=MATCH.source, destination=MATCH.destination,time=MATCH.time))
  def schedule_flight(self, f,id, source, destination,time):
        self.store_flight_in_database(id,source,destination,time)

        print(f"Flight {id} is scheduled from {source} to {destination} at {time}")

  @Rule(Flight(id=int, source=str, destination=str, time=str),
          Cargo(name=str, id=int, source=str, destination=str))
  def schedule(self, flight, cargo):
        # Check if cargo matches the flight criteria (source, destination, and time)
        if cargo.source == flight.source and cargo.destination == flight.destination:
            print(f"Scheduled Cargo '{cargo.name}' (ID={cargo.id}) on Flight {flight.id}")
        else:
            print(f"No matching flight found for Cargo '{cargo.name}' (ID={cargo.id})")

  def store_flight_in_database(self,id,source, destination,time):
        try:
            connection = sqlite3.connect(self.db_file)
            cursor = connection.cursor()

            # Insert flight information into the database
            cursor.execute("INSERT INTO flights (id,source, destination,time) VALUES (?, ?, ?,?)", (id,source, destination,time))

            connection.commit()
            print("Flight information stored in the database.")

        except sqlite3.Error as err:
            print(f"Error: {err}")

        finally:
            if connection:
                connection.close()

if __name__ == "__main__":
  engine=GARUDA(db_file)
  engine.reset()
  print("Welcome to GARUDA ~ An expert system for airline scheduling ")
  # source_input = input("Enter the source: ")
  # destination_input = input("Enter the destination: ")

    # Declare a flight and cargo based on user input
  while True:
        user_input = input("Enter |1.Enter Flight details, |2.Enter Cargo DEtails, |3.Schedule Flight and Cargo |4.any other key to exit: ")

        if user_input == '1':
            id_input=input('Enter the id of flight :')
            source_input = input("Enter the source for the flight: ")
            destination_input = input("Enter the destination for the flight: ")
            time_input=input('Enter time of flight in 24 hr format :')
            engine.declare(Flight(id=id_input,source=source_input, destination=destination_input,time=time_input))
            
            engine.run()
        elif user_input == '2':
            id_input=input('Enter the id of cargo :')
            name_input=input('Enter the name of cargo :')
            source_input = input("Enter the source for the flight: ")
            destination_input = input("Enter the destination for the flight: ")
            
            engine.declare(Flight(id=id_input,source=source_input, destination=destination_input,time=time_input))
            
            engine.run()
            
    # engine.declare(Cargo(source=source_input, destination=destination_input))
        else :
           break 


  engine.run()





