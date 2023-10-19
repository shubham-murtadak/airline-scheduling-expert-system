import tkinter as tk

class GarudaGUI:
    def __init__(self, master):
        self.master = master
        master.title("Garuda - Flight Scheduler")

        self.id_label = tk.Label(master, text="Flight ID:")
        self.id_entry = tk.Entry(master)

        self.destination_label = tk.Label(master, text="Destination:")
        self.destination_entry = tk.Entry(master)

        self.time_label = tk.Label(master, text="Time (24 hr format):")
        self.time_entry = tk.Entry(master)

        self.distance_label = tk.Label(master, text="Distance from Pune:")
        self.distance_entry = tk.Entry(master)

        self.submit_button = tk.Button(master, text="Submit", command=self.submit)

        # Layout
        self.id_label.grid(row=0, column=0, sticky=tk.E)
        self.id_entry.grid(row=0, column=1)

        self.destination_label.grid(row=1, column=0, sticky=tk.E)
        self.destination_entry.grid(row=1, column=1)

        self.time_label.grid(row=2, column=0, sticky=tk.E)
        self.time_entry.grid(row=2, column=1)

        self.distance_label.grid(row=3, column=0, sticky=tk.E)
        self.distance_entry.grid(row=3, column=1)

        self.submit_button.grid(row=4, column=1, pady=10)

    def submit(self):
        # Add your logic here to handle the submission
        flight_id = self.id_entry.get()
        destination = self.destination_entry.get()
        time = self.time_entry.get()
        distance = self.distance_entry.get()

        # Display the entered values (replace this with your logic)
        print(f"Flight ID: {flight_id}, Destination: {destination}, Time: {time}, Distance: {distance}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GarudaGUI(root)
    root.mainloop()
print("""
    ╔════════════════════════════════════════════════════════════╗


  .oooooo.          .o.       ooooooooo.   ooooo     ooo oooooooooo.         .o.            
 d8P'  `Y8b        .888.      `888   `Y88. `888'     `8' `888'   `Y8b       .888.           
888               .8"888.      888   .d88'  888       8   888      888     .8"888.          
888              .8' `888.     888ooo88P'   888       8   888      888    .8' `888.         
888     ooooo   .88ooo8888.    888`88b.     888       8   888      888   .88ooo8888.        
`88.    .88'   .8'     `888.   888  `88b.   `88.    .8'   888     d88'  .8'     `888.       
 `Y8bood8P'   o88o     o8888o o888o  o888o    `YbodP'    o888bood8P'   o88o     o8888o      
                                                                                            
                                                                                            
                                                                                                                              
    ║                                                                                    ║
    ║                 An Expert System for Airline                                       ║
    ║                  Scheduling - Welcome to                                           ║
    ║                 PUNE INTERNATIONAL AIRPORT                                         ║
    ║                                                                                 
    ╚════════════════════════════════════════════════════════════╝
    """)