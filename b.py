from experta import Fact, Rule, KnowledgeEngine

class Flight(Fact):
    pass

class Cargo(Fact):
    pass

class GarudaScheduler(KnowledgeEngine):
    @Rule(Flight(id=int, source=str, destination=str, time=str))
    def process_flight(self, id, source, destination, time):
        print(f"Received Flight Information: ID={id}, Source={source}, Destination={destination}, Time={time}")
        # You can add scheduling logic here based on the received information

    @Rule(Cargo(name=str, id=int, source=str, destination=str))
    def process_cargo(self, name, id, source, destination):
        print(f"Received Cargo Information: Name={name}, ID={id}, Source={source}, Destination={destination}")
        # You can add cargo processing logic here

# Example usage
if __name__ == "__main__":
    scheduler = GarudaScheduler()

    # Reset the engine
    scheduler.reset()

    # Simulate receiving flight information
    scheduler.declare(Flight(id=1, source="CityA", destination="CityB", time="10:00 AM"))

    # Simulate receiving cargo information
    scheduler.declare(Cargo(name="Cargo1", id=101, source="CityX", destination="CityY"))

    # Run the expert system
    scheduler.run()
