import customtkinter as ctk
import classes as c
class HomePage(ctk.CTk):
    #class init
    def __init__(self):
        #super from original class
        super().__init__()
        #title and the shape of the window
        self.title("FairShare")
        self.geometry("400*400")

        #create a big ahh label called "FairShare" and also a subheading, pack with a bit of padding, otherwise it does look a bit ugly
        ctk.CTkLabel(self, text="FairShare", font=ctk.CTkFont(size=60, weight="bold")).pack()
        ctk.CTkLabel(self, text="Track Your Group Work Contributions", font=ctk.CTkFont(size=20)).pack()
        #create a button to go to the login page and also a place where you put your name cus we dont need a password right yeah!
        self.name_entry = ctk.CTkEntry(self, placeholder_text="Enter your name", width=180)
        self.name_entry.pack(pady=10)
        ctk.CTkButton(self, text="Login", width=100).pack(pady=10)
        #thing that is called when loging in 
        
app = HomePage()
app.mainloop()