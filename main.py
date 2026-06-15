#import stuff yeah 

import customtkinter as ctk
import json
import os
from datetime import datetime
import classes as cl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import uuid as uuid


#set custom tk (im just gonna call it ctk for now) themes, so the main colours are like blue 
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

#name of the json file we r gon resue cus its like public variable 
DATA_FILE = "items.json"

#load users from json file ok now im thinking why not use Django tbh
def load_users():
    #if the file doesn't exist, create it
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            #dump is like put puh in json indent is like ohhhh im gonna make it look nice yay
            json.dump({}, file, indent=4)
            #return empty dict
        return {}
    #try and cathc errors
    try:
        #try and open the file
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
        #if sum go wrong return empty dict
    except Exception as e:
        print(f"urm theres an error {e}")
        #print("Uh oh i think sum wrong")
        #return empty dict
        return {}
    #if the data is not a dict data struct
    if not isinstance(data, dict):
        #return empty dict
        print("Not a dict")
        return {}
    #loop through the data
    for username, user in data.items():
        #set default values using .setdefault, just incase there is already data
        user.setdefault("name", username)
        user.setdefault("hours", 0)
        user.setdefault("lastLogin", datetime.now().isoformat())
        user.setdefault("isAdmin", False)
        #set default values with empty lists
        user.setdefault("contributions", [])
        user.setdefault("tasks", [])
        #loop through the tasks
        for task in user["tasks"]:
            task.setdefault("name", "")
            task.setdefault("submittedtime", "")
            task.setdefault("hours", 0)
            task.setdefault("difficulty", "e")
            task.setdefault("comment", "")
            task.setdefault("uid", str(uuid.uuid4()))  #backfill uid for old tasks
        #loop through the contributions uh i think this nested loop is okay
        for contribution in user["contributions"]:
            contribution.setdefault("name", "")
            contribution.setdefault("submittedtime", "")
            contribution.setdefault("hours", 0)
            contribution.setdefault("difficulty", "e")
            contribution.setdefault("comment", "")
    #return the data
    return data

#save information
def save_users(data):
    #save the data by opening the file and jumping info as in function 
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

#build user object from the json data
def build_user_object(username, data):
    #lowk why do i need this, i can just merge -- ok jason in the future, you have the stupid override thing
    if data.get("isAdmin", False):
        #return admin class with the attributes filled
        return cl.admin(
            #.get means like get the value of the key from teh dict cus dicts are the best form of data ew linked list ew hash table ew
            name=data.get("name", username),
            hours=data.get("hours", 0),
            lastLogin=data.get("lastLogin"),
            isadmin=True,
            contributions=data.get("contributions", []),
            tasks=data.get("tasks", [])
        )
    else:
        #else if not admin return member class with the attributes from json 
        return cl.member(
            name=data.get("name", username),
            hours=data.get("hours", 0),
            lastLogin=data.get("lastLogin"),
            contributions=data.get("contributions", []),
            tasks=data.get("tasks", [])
        )

#def change(member):
    #if data == isadmin:
        #member.__overide


#HOME PAGE: using ctk class and inheriting from ctk
class HomePage(ctk.CTk):
    #class init
    def __init__(self):
        #super from original class
        super().__init__()
        #title and the shape of the window
        self.title("FairShare")
        self.geometry("350x320")
        self.grab_set()

        #create a big ahh label called "FairShare" and also a subheading, pack with a bit of padding, otherwise it does look a bit ugly
        ctk.CTkLabel(self, text="FairShare", font=ctk.CTkFont(size=28, weight="bold")).pack(pady=(30, 10))
        ctk.CTkLabel(self, text="Track Your Group Work Contributions", font=ctk.CTkFont(size=14)).pack(pady=(5, 20))
        #create a button to go to the login page and also a place where you put your name cus we dont need a password right yeah!
        self.name_entry = ctk.CTkEntry(self, placeholder_text="Enter your name", width=180)
        self.name_entry.pack(pady=10)
        ctk.CTkButton(self, text="Login", command=self.login_user, width=100).pack(pady=10)
        #thing that is called when loging in 
    def login_user(self):
        #get the name from teh entry box, strip of empty spaces n stuff
        name = self.name_entry.get().strip().capitalize()
        #if theres jack in the entry box, show error message
        if not name:
            #self.status_label.configure(text="Please enter a name.")
            print("bro type sum")
            return
        #load the user wiht the name
        users = load_users()
        #if the name is not in the users dict, create a new user
        if name not in users:
            #make it empty cus they havent done anthig
            new_user = cl.member(name=name, hours=0, lastLogin=datetime.now().isoformat(),isAdmin=False, contributions=[], tasks=[])
            users[name] = new_user.dictafy()
            save_users(users)
        else:
            #if the name is in the users dict, update the last login
            obj = build_user_object(name, users[name])
            # get time and date now
            obj.lastLogin = datetime.now().isoformat()
            users[name] = obj.dictafy()
            save_users(users)
        #kill yourself
        self.destroy()
        #go to dashboard
        Dashboard(name).mainloop()

#dashboard
class Dashboard(ctk.CTk): #inherit from ctk main class
    def __init__(self, username):#init
        #super from original class from ctk
        super().__init__()
        #title and the shape of the window
        self.username = username
        self.title(f"FairShare — {username}")
        self.geometry("950x600")

        #lq layout of the window ig lmao
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        #creaate the taskbar frame that we will put stuff in like out buttons or sum
        self.taskbar = ctk.CTkFrame(self, width=220, corner_radius=0)
        #grid the taskbar frame (put it in the top left)   #and make it sticky whihc means it scrolls with us!
        self.taskbar.grid(row=0, column=0, sticky="nsew")
        self.taskbar.grid_rowconfigure(20, weight=1)

        #create a label called "FairShare" title lmao, bold, size 22 and also lil bit of padding
        #all of these buttons are visible for everyone but also have different commands
        ctk.CTkLabel(self.taskbar, text="FairShare",font=ctk.CTkFont(size=22, weight="bold")).grid(row=0, column=0, padx=20, pady=(20, 10))
        #create a button called "add task" that will go to the add task window
        ctk.CTkButton(self.taskbar, text="Add Task",         command=self.add_task).grid(row=1, column=0, padx=20, pady=5)
        #create a button called "add contribution" that will go to the add contribution window
        ctk.CTkButton(self.taskbar, text="Add Contribution", command=self.add_contribution).grid(row=2, column=0, padx=20, pady=5)
        #create a button called "refresh" that will refresh the dashboard
        ctk.CTkButton(self.taskbar, text="Refresh",          command=self.refresh_dashboard).grid(row=3, column=0, padx=20, pady=5)

        #if the user is an admin
        users = load_users()
        if users.get(username, {}).get("isAdmin", False):
            #create a label called "Admin"
            ctk.CTkLabel(self.taskbar, text="== Admin ==", font=ctk.CTkFont(size=11), text_color="gray").grid(row=4, column=0, padx=20, pady=(15, 5))
            #create a button called "view logs" that will go to the view logs window
            ctk.CTkButton(self.taskbar, text="View Logs",command=self.view_logs).grid(row=5, column=0, padx=20, pady=5)
            #create a button called "view all tasks" that will go to the view all tasks window
            ctk.CTkButton(self.taskbar, text="View All Tasks",command=self.view_all_tasks).grid(row=6, column=0, padx=20, pady=5)
            #create a button called "view all contributions" that will go to the view all contributions window
            ctk.CTkButton(self.taskbar, text="View All Contributions",command=self.view_all_contributions).grid(row=7, column=0, padx=20, pady=5)
            #create a button called "view all users" that will go to the view all users window
            ctk.CTkButton(self.taskbar, text="View All Users",command=self.view_all_users).grid(row=8, column=0, padx=20, pady=5)
            #create a button called "delete entry" that will go to the delete entry window
            ctk.CTkButton(self.taskbar, text="Delete Entry",command=self.delete_entry).grid(row=9, column=0, padx=20, pady=5)
        #create a button called "logout" that will logout the user this one is sticky so it goes to the bottom when we scroll
        ctk.CTkButton(self.taskbar, text="Logout", fg_color="gray",command=self.logout).grid(row=21, column=0, padx=20, pady=20, sticky="s")

        # main content and layout
        # create a frame for the main content and put it in the middle and make the colour transparent
        self.main_content = ctk.CTkFrame(self, fg_color="transparent")
        self.main_content.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        #configure the grid
        self.main_content.grid_columnconfigure(0, weight=1)
        self.main_content.grid_columnconfigure(1, weight=1)
        self.main_content.grid_rowconfigure(2, weight=1)
        #create a label called "Welcome back, {username}!"
        self.welcome_label = ctk.CTkLabel(self.main_content, text=f"Welcome back, {username}!",font=ctk.CTkFont(size=24, weight="bold"))
        #grid the label to the frame
        self.welcome_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))
        #create a label called "Summary"
        self.summary_label = ctk.CTkLabel(self.main_content, text="")
        #grid the label to the frame
        self.summary_label.grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 15))

        #this is where the tasks will go
        self.task_list = ctk.CTkScrollableFrame(self.main_content, label_text="My Tasks")
        self.task_list.grid(row=2, column=0, sticky="nsew", padx=(0, 10))
        self.task_list.grid_columnconfigure(0, weight=1)

        #this is where the leaderboard will go where we will put the top users
        self.leaderboard_frame = ctk.CTkFrame(self.main_content)
        self.leaderboard_frame.grid(row=2, column=1, sticky="nsew", padx=(10, 0))
        #call refresh emthod
        self.refresh_dashboard()

    # refresh the dashboard
    def refresh_dashboard(self):
        #load the users
        users = load_users()
        #if the user is not in the users dict, return
        if self.username not in users:
            return
        #build the user object
        self.user_obj = build_user_object(self.username, users[self.username])
        #destroy all the children of the widgets
        for w in self.task_list.winfo_children():
            #destroy the widget and all its children
            w.destroy()
        #destroy all the children of the widgets
        for w in self.leaderboard_frame.winfo_children():
            #destroy the widget and all its children
            w.destroy()

        # Summary bar
        pts = sum(
            #calculate the points for each contribution and add it to the total points
            cl.contributions(
                name=c.get("name", ""), user=self.username,
                submittedtime=c.get("submittedtime", ""),
                hours=c.get("hours", 0), difficulty=c.get("difficulty", "e"),
                comment=c.get("comment", "")
            )._pointcalc()
            #for each contribution
            for c in self.user_obj.contributions
        )
        #update the summary label
        self.summary_label.configure(
            text=f"Hours: {self.user_obj.hours}  |  Tasks: {len(self.user_obj.tasks)}  |  Contributions: {len(self.user_obj.contributions)}  |  My Points: {pts}"
        )

        # Task cards
        if self.user_obj.tasks:
            #for each task, get the name, submitted time, difficulty, and comment and list num
            for i, td in enumerate(self.user_obj.tasks):
                #create a card in the task frane
                card = ctk.CTkFrame(self.task_list)
                #attach the card to the frame
                card.grid(row=i, column=0, sticky="ew", padx=5, pady=5)
                #configure the column
                card.grid_columnconfigure(0, weight=1)
                #create a label in the card
                obj = cl.item.from_dict(td, self.username)
                #attach the label to the card
                ctk.CTkLabel(card,#create a label
                             text=f"{obj.name}  |  {obj.submittedtime}  |  Difficulty: {obj.difficulty.upper()}",
                             font=ctk.CTkFont(weight="bold"), wraplength=280, anchor="w", justify="left"
                             ).grid(row=0, column=0, sticky="ew", padx=10, pady=(8, 2))
                ctk.CTkLabel(card, text=f"Comment: {obj.comment}",
                             wraplength=280, anchor="w", justify="left"
                             ).grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 8))
        else:
            #if there are no tasks yet create a label
            ctk.CTkLabel(self.task_list, text="No tasks yet.").grid(row=0, column=0, pady=10)

        # Leaderboard only users with points
        leaderboard = []
        #for each user in the users dict
        for uname, udata in users.items():
            p = sum(
                cl.contributions(
                    name=c.get("name", ""), user=uname,
                    submittedtime=c.get("submittedtime", ""),
                    hours=c.get("hours", 0), difficulty=c.get("difficulty", "e"),
                    comment=c.get("comment", "")
                )._pointcalc()
                for c in udata.get("contributions", [])
            )
            if p > 0:
                leaderboard.append((uname, p))
        #sorts learderboard by points, and not name, lambda is used as a one off function
        leaderboard.sort(key=lambda x: x[1], reverse=True)

        ctk.CTkLabel(self.leaderboard_frame, text="Leaderboard",
                     font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(10, 4))

        if not leaderboard:
            ctk.CTkLabel(self.leaderboard_frame,
                         text="No contributions yet.\nChart appears once points are logged.",
                         text_color="gray").pack(pady=20)
            return

        #medals for top 3, just numbers after that
        medals = ["🥇", "🥈", "🥉"]
        #for each leaderboard entry create a label 
        for i, (uname, p) in enumerate(leaderboard):
            medal = medals[i] if i < 3 else f"{i+1}"
            #highlight the current user in blue so they know its them
            if i < 5:
                ctk.CTkLabel(self.leaderboard_frame,text=f"{medal}  {uname}  —  {p} pts",font=ctk.CTkFont(weight="bold") if uname == self.username else ctk.CTkFont(),
                            text_color="#4e9af1" if uname == self.username else "white"
                            ).pack(anchor="w", padx=16, pady=2)

        # Pie chart using matplotlib embedded in ctk cus why not
        names   = [n for n, _ in leaderboard]
        values  = [p for _, p in leaderboard]
        #colours for the pie chart slices, just a list of hex colours
        colours = ["#4e9af1", "#f1c94e", "#f17c4e", "#6ef14e",
                   "#c44ef1", "#4ef1c4", "#f14e7c", "#a0a0a0"][:len(names)]

        #make the figure dark so it matches the ctk theme
        fig, ax = plt.subplots(figsize=(3, 3), facecolor="#2b2b2b")
        ax.pie(values, labels=names, colors=colours, startangle=90,
               autopct="%1.0f%%", pctdistance=0.75,
               textprops={"color": "white", "fontsize": 7},
               wedgeprops={"linewidth": 1, "edgecolor": "#2b2b2b"})
        ax.set_facecolor("#2b2b2b")
        fig.tight_layout()

        #embed the matplotlib figure into the ctk frame using FigureCanvasTkAgg
        canvas = FigureCanvasTkAgg(fig, master=self.leaderboard_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=(6, 10))
        #close the figure so we dont leak memory haha
        plt.close(fig)

    # buttons 
    def add_task(self):
        AddTaskWindow(self, self.username)

    def add_contribution(self):
        AddContributionWindow(self, self.username)

    def view_logs(self):
        AdminLogsWindow(self)

    def view_all_tasks(self):
        AdminAllTasksWindow(self)

    def view_all_contributions(self):
        AdminAllContributionsWindow(self)

    def view_all_users(self):
        AdminAllUsersWindow(self)

    def delete_entry(self):
        AdminDeleteWindow(self)

    #logout: kill the dashboard and go back to home page
    def logout(self):
        self.destroy()
        HomePage().mainloop()


#ts window adds tasks
class AddTaskWindow(ctk.CTkToplevel):
    #init with parent and username
    def __init__(self, parent, username):
        super().__init__(parent)
        self.parent = parent
        self.username = username
        self.title("Add Task")
        self.geometry("320x350")
        #grab_set so u cant click on the dashboard while this is open
        self.grab_set()

        ctk.CTkLabel(self, text="Add a Task", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)

        #check if the user is an admin so we can show the assignee field
        users = load_users()
        self.is_admin = users.get(username, {}).get("isAdmin", False)

        #task name entry
        ctk.CTkLabel(self, text="Task Name:").pack()
        self.name_entry = ctk.CTkEntry(self, width=220)
        self.name_entry.pack(pady=4)

        #only show assignee field if admin cus normal users cant assign to others
        if self.is_admin:
            ctk.CTkLabel(self, text="Assignee:").pack()
            all_names = list(users.keys())
            self.assignee_menu = ctk.CTkOptionMenu(self, values=all_names, width=220)
            self.assignee_menu.pack(pady=4)
            self._target = all_names[0] if all_names else username
        else:
            #normal user can only log against their own tasks
            self._target = username

        #difficulty dropdown e = easy m = medium h = hard
        ctk.CTkLabel(self, text="Difficulty (e = easy m = medium h = hard):").pack()
        self.difficulty_menu = ctk.CTkOptionMenu(self, values=["e", "m", "h"], width=220)
        self.difficulty_menu.pack(pady=4)

        #comment entry
        ctk.CTkLabel(self, text="Comment:").pack()
        self.comment_entry = ctk.CTkEntry(self, width=220)
        self.comment_entry.pack(pady=4)

        #submit button and status label for errors
        ctk.CTkButton(self, text="Submit", command=self.submit).pack(pady=14)
        self.status_label = ctk.CTkLabel(self, text="", text_color="red")
        self.status_label.pack()

    #submit the task to the json file
    def submit(self):
        users = load_users()
        #if admin use the assignee entry, otherwise just use the logged in user
        assignee = self.assignee_menu.get() if self.is_admin else self.username
        name = self.name_entry.get().strip()
        difficulty = self.difficulty_menu.get().strip().lower()
        comment = self.comment_entry.get().strip()

        #validate that name isnt empty
        if not name:
            self.status_label.configure(text="Task name is required.")
            return
        #validate that the assignee actually exists
        if assignee not in users:
            self.status_label.configure(text="Assignee does not exist.")
            return

        #build the user object and add the task then save
        obj = build_user_object(assignee, users[assignee])
        obj.add_task(cl.item(name=name, user=assignee, submittedtime=datetime.now().strftime("%Y-%m-%d %H:%M"), hours=0, difficulty=difficulty, comment=comment))
        users[assignee] = obj.dictafy()
        save_users(users)
        #refresh the dashboard so the new task shows up
        self.parent.refresh_dashboard()
        self.destroy()


#ts window adds contributions and links them to tasks
class AddContributionWindow(ctk.CTkToplevel):
    def __init__(self, parent, username):
        super().__init__(parent)
        self.parent = parent
        self.username = username
        self.title("Add Contribution")
        self.geometry("340x420")
        self.grab_set()

        ctk.CTkLabel(self, text="Add a Contribution",font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)

        users = load_users()
        self.is_admin = users.get(username, {}).get("isAdmin", False)

        # If admin, let them pick whose tasks to log against
        if self.is_admin:
            ctk.CTkLabel(self, text="Assignee:").pack()
            all_names = list(users.keys())
            #when admin changes assignee, reload the task dropdown
            self.assignee_menu = ctk.CTkOptionMenu(self, values=all_names, width=220,
                                                   command=self._load_tasks)
            self.assignee_menu.pack(pady=4)
            self._target = all_names[0] if all_names else username
        else:
            #normal user can only log against their own tasks
            self._target = username

        # Task selector
        ctk.CTkLabel(self, text="Select Task:").pack()
        self._task_map = {}   # display label -> task dict
        self._build_task_map(users)
        task_labels = list(self._task_map.keys()) or ["— no tasks —"]
        self.task_menu = ctk.CTkOptionMenu(self, values=task_labels, width=220,)
        self.task_menu.pack(pady=4)

        #hours entry
        ctk.CTkLabel(self, text="Hours spent:").pack()
        self.hours_entry = ctk.CTkEntry(self, width=220)
        self.hours_entry.pack(pady=4)

        #comment entry
        ctk.CTkLabel(self, text="Comment:").pack()
        self.comment_entry = ctk.CTkEntry(self, width=220)
        self.comment_entry.pack(pady=4)

        ctk.CTkButton(self, text="Submit", command=self.submit).pack(pady=14)
        self.status_label = ctk.CTkLabel(self, text="", text_color="red")
        self.status_label.pack()

        # Pre-select first task if available
        if self._task_map:
            self._on_task_select(task_labels[0])

    #build the task map dict so we can look up task data from the display label
    def _build_task_map(self, users):
        self._task_map = {}
        tasks = users.get(self._target, {}).get("tasks", [])
        for t in tasks:
            label = f"{t.get('name','?')}  [{t.get('difficulty','e').upper()}]"
            self._task_map[label] = t

    def _load_tasks(self, assignee):
        self._target = assignee
        users = load_users()
        self._build_task_map(users)
        labels = list(self._task_map.keys()) or ["— no tasks —"]
        self.task_menu.configure(values=labels)
        self.task_menu.set(labels[0])
        if self._task_map:
            self._on_task_select(labels[0])

    #def _on_task_select(self, label):
     #   pass  # could pre-fill difficulty info here if desired

    #submit the contribution and link it to the selected task uid
    def submit(self):
        users = load_users()
        selected_label = self.task_menu.get()

        #make sure a valid task is selected
        if selected_label not in self._task_map:
            self.status_label.configure(text="Please select a valid task.")
            return

        task_data = self._task_map[selected_label]
        hours_text = self.hours_entry.get().strip()
        comment = self.comment_entry.get().strip()

        #validate hours is a positive number
        try:
            hours = float(hours_text)
            if hours < 0:
                raise ValueError
        except ValueError:
            self.status_label.configure(text="Hours must be a valid positive number.")
            return

        if self._target not in users:
            self.status_label.configure(text="User not found.")
            return

        #build the contribution object and add it to the user
        obj = build_user_object(self._target, users[self._target])
        contrib = cl.contributions(
            name=task_data.get("name", ""),
            user=self._target,
            submittedtime=datetime.now().strftime("%Y-%m-%d %H:%M"),
            hours=hours,
            difficulty=task_data.get("difficulty", "e"),
            comment=comment
        )
        #pass the task uid so it links to the right task
        obj.add_contribution(contrib, task_uid=task_data.get("uid"))

        users[self._target] = obj.dictafy()
        save_users(users)
        self.parent.refresh_dashboard()
        self.destroy()


#base class for all admin windows so we dont repeat ourselves lol
class _AdminBaseWindow(ctk.CTkToplevel):
    def __init__(self, parent, title, size="600x500"):
        super().__init__(parent)
        self.title(title)
        self.geometry(size)
        self.grab_set()
        #title label at the top
        ctk.CTkLabel(self, text=title, font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        #scrollable body frame where all the cards go
        self.body = ctk.CTkScrollableFrame(self)
        self.body.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.body.grid_columnconfigure(0, weight=1)


#admin window: shows last login times for all users
class AdminLogsWindow(_AdminBaseWindow):
    def __init__(self, parent):
        super().__init__(parent, "Login Logs")
        users = load_users()
        if not users:
            ctk.CTkLabel(self.body, text="No users found.").grid(row=0, column=0, pady=10)
            return
        #loop through users and make a card for each one
        for i, (uname, udata) in enumerate(users.items()):
            card = ctk.CTkFrame(self.body)
            card.grid(row=i, column=0, sticky="ew", padx=5, pady=4)
            card.grid_columnconfigure(0, weight=1)
            role = "Admin" if udata.get("isAdmin") else "Member"
            ctk.CTkLabel(card, text=f"{uname}  [{role}]",
                         font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w", padx=10, pady=(6, 2))
            #show last login in gray cus its like secondary info
            ctk.CTkLabel(card, text=f"Last login: {udata.get('lastLogin','—')}",
                         text_color="gray").grid(row=1, column=0, sticky="w", padx=10, pady=(0, 6))


#admin window: shows every task across all users
class AdminAllTasksWindow(_AdminBaseWindow):
    def __init__(self, parent):
        super().__init__(parent, "All Tasks")
        users = load_users()
        row = 0
        #loop through each user and show their tasks grouped under their name
        for uname, udata in users.items():
            tasks = udata.get("tasks", [])
            if not tasks:
                continue
            #user header label in blue
            ctk.CTkLabel(self.body, text=f"── {uname} ──",
                         font=ctk.CTkFont(weight="bold"), text_color="#4e9af1"
                         ).grid(row=row, column=0, sticky="w", padx=8, pady=(10, 2))
            row += 1
            #card for each task
            for td in tasks:
                card = ctk.CTkFrame(self.body)
                card.grid(row=row, column=0, sticky="ew", padx=5, pady=3)
                card.grid_columnconfigure(0, weight=1)
                ctk.CTkLabel(card,
                             text=f"{td.get('name','?')}  |  {td.get('submittedtime','')}  |  Diff: {td.get('difficulty','?').upper()}",
                             font=ctk.CTkFont(weight="bold"), wraplength=500, anchor="w"
                             ).grid(row=0, column=0, sticky="ew", padx=10, pady=(6, 2))
                ctk.CTkLabel(card, text=f"Comment: {td.get('comment','')}",
                             wraplength=500, anchor="w"
                             ).grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 6))
                row += 1
        if row == 0:
            ctk.CTkLabel(self.body, text="No tasks found.").grid(row=0, column=0, pady=10)


#admin window: shows every contribution across all users with points
class AdminAllContributionsWindow(_AdminBaseWindow):
    def __init__(self, parent):
        super().__init__(parent, "All Contributions")
        users = load_users()
        row = 0
        #loop through each user and show their contributions grouped under their name
        for uname, udata in users.items():
            contribs = udata.get("contributions", [])
            if not contribs:
                continue
            #user header label in blue
            ctk.CTkLabel(self.body, text=f"── {uname} ──",
                         font=ctk.CTkFont(weight="bold"), text_color="#4e9af1"
                         ).grid(row=row, column=0, sticky="w", padx=8, pady=(10, 2))
            row += 1
            for cd in contribs:
                #build contribution object so we can call _pointcalc on it
                c_obj = cl.contributions(
                    name=cd.get("name", ""), user=uname,
                    submittedtime=cd.get("submittedtime", ""),
                    hours=cd.get("hours", 0), difficulty=cd.get("difficulty", "e"),
                    comment=cd.get("comment", "")
                )
                card = ctk.CTkFrame(self.body)
                card.grid(row=row, column=0, sticky="ew", padx=5, pady=3)
                card.grid_columnconfigure(0, weight=1)
                ctk.CTkLabel(card,
                             text=f"{c_obj.name}  |  {c_obj.submittedtime}  |  {c_obj.hours}h  |  Diff: {c_obj.difficulty.upper()}  |  Pts: {c_obj._pointcalc()}",
                             font=ctk.CTkFont(weight="bold"), wraplength=500, anchor="w"
                             ).grid(row=0, column=0, sticky="ew", padx=10, pady=(6, 2))
                ctk.CTkLabel(card, text=f"Comment: {c_obj.comment}",
                             wraplength=500, anchor="w"
                             ).grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 6))
                row += 1
        if row == 0:
            ctk.CTkLabel(self.body, text="No contributions found.").grid(row=0, column=0, pady=10)


#admin window: shows all users with their stats
class AdminAllUsersWindow(_AdminBaseWindow):
    def __init__(self, parent):
        super().__init__(parent, "All Users")
        users = load_users()
        if not users:
            ctk.CTkLabel(self.body, text="No users found.").grid(row=0, column=0, pady=10)
            return
        #loop through users and calculate their total points from contributions
        for i, (uname, udata) in enumerate(users.items()):
            pts = sum(
                cl.contributions(
                    name=c.get("name", ""), user=uname,
                    submittedtime=c.get("submittedtime", ""),
                    hours=c.get("hours", 0), difficulty=c.get("difficulty", "e"),
                    comment=c.get("comment", "")
                )._pointcalc()
                for c in udata.get("contributions", [])
            )
            #make frame for each card to go in
            card = ctk.CTkFrame(self.body)
            #grid it in the window
            card.grid(row=i, column=0, sticky="ew", padx=5, pady=4)
            #make column 0 expand
            card.grid_columnconfigure(0, weight=1)
            #name and role if admin else member
            role = "Admin" if udata.get("isAdmin") else "Member"
            ctk.CTkLabel(card, text=f"{uname}  {role}",
                         font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w", padx=10, pady=(6, 2))
            #stats in gray cus secondary info 
            ctk.CTkLabel(card,
                         text=f"Hours: {udata.get('hours', 0)}  |  Tasks: {len(udata.get('tasks', []))}  |  Contributions: {len(udata.get('contributions', []))}  |  Points: {pts}",
                         text_color="gray").grid(row=1, column=0, sticky="w", padx=10, pady=(0, 6))


#admin window
class AdminDeleteWindow(ctk.CTkToplevel):
    #admin window shows all users with their stats
    def __init__(self, parent):
        super().__init__(parent)
        self.parent_dash = parent
        self.title("Delete Entry")
        self.geometry("400x380")
        #center window and make it focused on 
        self.grab_set()
        #window title
        ctk.CTkLabel(self, text="Delete Task / Contribution",
                     font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        #get all user names
        users = load_users()
        all_names = list(users.keys())

        #user dropdown
        ctk.CTkLabel(self, text="User:").pack()
        self.user_menu = ctk.CTkOptionMenu(self, values=all_names, width=260,
                                           command=self._load_entries)
        self.user_menu.pack(pady=4)

        #type dropdown: task or contribution
        ctk.CTkLabel(self, text="Type:").pack()
        self.type_menu = ctk.CTkOptionMenu(self, values=["task", "contribution"], width=260,
                                           command=lambda _: self._load_entries(self.user_menu.get()))
        self.type_menu.pack(pady=4)

        #entry dropdown: which specific entry to delete
        ctk.CTkLabel(self, text="Entry:").pack()
        self.entry_menu = ctk.CTkOptionMenu(self, values=["—"], width=260)
        self.entry_menu.pack(pady=4)

        #delete button in red cus its destructive lol
        ctk.CTkButton(self, text="Delete", fg_color="#c0392b",
                      command=self.do_delete).pack(pady=14)
        self.status_label = ctk.CTkLabel(self, text="", text_color="red")
        self.status_label.pack()

        #load entries for the first user on open
        if all_names:
            self._load_entries(all_names[0])

    #reload the entry dropdown when user or type changes
    def _load_entries(self, username):
        users = load_users()
        kind = self.type_menu.get()
        entries = users.get(username, {}).get(kind + "s", [])
        labels = [f"{e.get('name','?')}  [{e.get('submittedtime','')}]" for e in entries]
        self.entry_menu.configure(values=labels if labels else ["— none —"])
        self.entry_menu.set(labels[0] if labels else "— none —")

    #actually do the delete, only deletes the first match so duplicates are safe
    def do_delete(self):
        users = load_users()
        username = self.user_menu.get()
        kind = self.type_menu.get()
        selected = self.entry_menu.get()

        #if nothing to delete just bail bye bye
        if selected in ("— none —", "—"):
            self.status_label.configure(text="Nothing to delete.")
            return

        entries = users.get(username, {}).get(kind + "s", [])
        new_entries = []
        deleted = False
        for e in entries:
            label = f"{e.get('name','?')}  [{e.get('submittedtime','')}]"
            if label == selected and not deleted:
                deleted = True  # skip (delete) only the first match
            else:
                new_entries.append(e)

        if not deleted:
            self.status_label.configure(text="Entry not found.")
            return

        #save the updated list without the deleted entry
        users[username][kind + "s"] = new_entries
        save_users(users)
        self.status_label.configure(text=f"Deleted '{selected}' from {username}.", text_color="green")
        #reload the dropdown and refresh the dashboard
        self._load_entries(username)
        self.parent_dash.refresh_dashboard()


#entry point, run the home page
if __name__ == "__main__":
    app = HomePage()
    app.mainloop()