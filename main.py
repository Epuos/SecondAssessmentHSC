import customtkinter as ctk                                          # UI framework
import json                                                           # JSON read/write
import os                                                             # file system checks
from datetime import datetime                                         # timestamps
import classes as cl                                                  # member/item/contributions/admin classes
import matplotlib.pyplot as plt                                       # pie chart
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg      # embed matplotlib in ctk
import uuid as uuid                                                   # unique IDs

ctk.set_appearance_mode("dark")                                 # dark mode
ctk.set_default_color_theme("blue")                             # blue accent colour

DATA_FILE = "items.json"                                        # shared json filename constant


def load_users():
    if not os.path.exists(DATA_FILE):                           # if file doesn't exist, create it
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump({}, file, indent=4)                       # write empty dict
        return {}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
    except Exception as e:
        print(f"Error loading data: {e}")                       # log error and return empty
        return {}
    if not isinstance(data, dict):                              # guard against corrupt data
        print("Not a dict")
        return {}
    for username, user in data.items():                         # loop through users and backfill missing fields
        user.setdefault("name", username)
        user.setdefault("hours", 0)
        user.setdefault("lastLogin", datetime.now().isoformat())
        user.setdefault("isAdmin", False)
        user.setdefault("contributions", [])                    # default to empty lists
        user.setdefault("tasks", [])
        for task in user["tasks"]:                              # backfill task fields
            task.setdefault("name", "")
            task.setdefault("submittedtime", "")
            task.setdefault("hours", 0)
            task.setdefault("difficulty", "e")
            task.setdefault("comment", "")
            task.setdefault("uid", str(uuid.uuid4()))           # backfill uid for old tasks
        for contribution in user["contributions"]:              # backfill contribution fields
            contribution.setdefault("name", "")
            contribution.setdefault("submittedtime", "")
            contribution.setdefault("hours", 0)
            contribution.setdefault("difficulty", "e")
            contribution.setdefault("comment", "")
    return data


def save_users(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)                        # write data to json with pretty indent


def build_user_object(username, data):
    if data.get("isAdmin", False):                          # return admin object if flagged
        return cl.admin(
            name=data.get("name", username),                # .get pulls value from dict safely
            hours=data.get("hours", 0),
            lastLogin=data.get("lastLogin"),
            isadmin=True,
            contributions=data.get("contributions", []),
            tasks=data.get("tasks", [])
        )
    else:                                                   # otherwise return regular member
        return cl.member(
            name=data.get("name", username),
            hours=data.get("hours", 0),
            lastLogin=data.get("lastLogin"),
            contributions=data.get("contributions", []),
            tasks=data.get("tasks", [])
        )


class HomePage(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("FairShare")
        self.geometry("350x320")
        self.grab_set()

        ctk.CTkLabel(self, text="FairShare", font=ctk.CTkFont(size=28, weight="bold")).pack(pady=(30, 10))           # app title
        ctk.CTkLabel(self, text="Track Your Group Work Contributions", font=ctk.CTkFont(size=14)).pack(pady=(5, 20)) # subtitle

        self.name_entry = ctk.CTkEntry(self, placeholder_text="Enter your name", width=180)
        self.name_entry.pack(pady=10)
        ctk.CTkButton(self, text="Login", command=self.login_user, width=100).pack(pady=10)

    def login_user(self):
        name = self.name_entry.get().strip().capitalize()  # get and clean name input
        if not name:
            print("Please enter a name.")
            return
        users = load_users()
        if name not in users:                              # new user: create and save
            new_user = cl.member(name=name, hours=0, lastLogin=datetime.now().isoformat(), isAdmin=False, contributions=[], tasks=[])
            users[name] = new_user.dictafy()
            save_users(users)
        else:                                             # existing user: update last login
            obj = build_user_object(name, users[name])
            obj.lastLogin = datetime.now().isoformat()
            users[name] = obj.dictafy()
            save_users(users)
        self.destroy()                                   # close home page
        Dashboard(name).mainloop()                       # open dashboard


class Dashboard(ctk.CTk):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.title(f"FairShare — {username}")
        self.geometry("950x600")

        self.grid_columnconfigure(0, weight=0)  # sidebar fixed width
        self.grid_columnconfigure(1, weight=1)  # main content expands
        self.grid_rowconfigure(0, weight=1)

        self.taskbar = ctk.CTkFrame(self, width=220, corner_radius=0)  # left sidebar
        self.taskbar.grid(row=0, column=0, sticky="nsew")
        self.taskbar.grid_rowconfigure(20, weight=1)

        ctk.CTkLabel(self.taskbar, text="FairShare", font=ctk.CTkFont(size=22, weight="bold")).grid(row=0, column=0, padx=20, pady=(20, 10))  # sidebar title
        ctk.CTkButton(self.taskbar, text="Add Task",         command=self.add_task).grid(row=1, column=0, padx=20, pady=5)          # open add task window
        ctk.CTkButton(self.taskbar, text="Add Contribution", command=self.add_contribution).grid(row=2, column=0, padx=20, pady=5)  # open add contribution window
        ctk.CTkButton(self.taskbar, text="Refresh",          command=self.refresh_dashboard).grid(row=3, column=0, padx=20, pady=5) # refresh dashboard

        users = load_users()
        if users.get(username, {}).get("isAdmin", False):  # show admin controls if user is admin
            ctk.CTkLabel(self.taskbar, text="== Admin ==", font=ctk.CTkFont(size=11), text_color="gray").grid(row=4, column=0, padx=20, pady=(15, 5))
            ctk.CTkButton(self.taskbar, text="View Logs",             command=self.view_logs).grid(row=5, column=0, padx=20, pady=5)
            ctk.CTkButton(self.taskbar, text="View All Tasks",        command=self.view_all_tasks).grid(row=6, column=0, padx=20, pady=5)
            ctk.CTkButton(self.taskbar, text="View All Contributions", command=self.view_all_contributions).grid(row=7, column=0, padx=20, pady=5)
            ctk.CTkButton(self.taskbar, text="View All Users",        command=self.view_all_users).grid(row=8, column=0, padx=20, pady=5)
            ctk.CTkButton(self.taskbar, text="Delete Entry",          command=self.delete_entry).grid(row=9, column=0, padx=20, pady=5)

        ctk.CTkButton(self.taskbar, text="Logout", fg_color="gray", command=self.logout).grid(row=21, column=0, padx=20, pady=20, sticky="s")  # logout pinned to bottom

        self.main_content = ctk.CTkFrame(self, fg_color="transparent")  # transparent main area
        self.main_content.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_content.grid_columnconfigure(0, weight=1)
        self.main_content.grid_columnconfigure(1, weight=1)
        self.main_content.grid_rowconfigure(2, weight=1)

        self.welcome_label = ctk.CTkLabel(self.main_content, text=f"Welcome back, {username}!", font=ctk.CTkFont(size=24, weight="bold"))
        self.welcome_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))

        self.summary_label = ctk.CTkLabel(self.main_content, text="")
        self.summary_label.grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 15))

        self.task_list = ctk.CTkScrollableFrame(self.main_content, label_text="My Tasks")  # scrollable task list
        self.task_list.grid(row=2, column=0, sticky="nsew", padx=(0, 10))
        self.task_list.grid_columnconfigure(0, weight=1)

        self.leaderboard_frame = ctk.CTkFrame(self.main_content)  # leaderboard + pie chart
        self.leaderboard_frame.grid(row=2, column=1, sticky="nsew", padx=(10, 0))

        self.refresh_dashboard()

    def refresh_dashboard(self):
        users = load_users()
        if self.username not in users:
            return
        self.user_obj = build_user_object(self.username, users[self.username])

        for w in self.task_list.winfo_children():       # clear task list
            w.destroy()
        for w in self.leaderboard_frame.winfo_children():  # clear leaderboard
            w.destroy()

        pts = sum(                                       # calculate total points from contributions
            cl.contributions(
                name=c.get("name", ""), user=self.username,
                submittedtime=c.get("submittedtime", ""),
                hours=c.get("hours", 0), difficulty=c.get("difficulty", "e"),
                comment=c.get("comment", "")
            )._pointcalc()
            for c in self.user_obj.contributions
        )
        self.summary_label.configure(
            text=f"Hours: {self.user_obj.hours}  |  Tasks: {len(self.user_obj.tasks)}  |  Contributions: {len(self.user_obj.contributions)}  |  My Points: {pts}"
        )

        if self.user_obj.tasks:
            for i, td in enumerate(self.user_obj.tasks):  # render a card for each task
                card = ctk.CTkFrame(self.task_list)
                card.grid(row=i, column=0, sticky="ew", padx=5, pady=5)
                card.grid_columnconfigure(0, weight=1)
                obj = cl.item.from_dict(td, self.username)
                ctk.CTkLabel(card,
                             text=f"{obj.name}  |  {obj.submittedtime}  |  Difficulty: {obj.difficulty.upper()}",
                             font=ctk.CTkFont(weight="bold"), wraplength=280, anchor="w", justify="left"
                             ).grid(row=0, column=0, sticky="ew", padx=10, pady=(8, 2))
                ctk.CTkLabel(card, text=f"Comment: {obj.comment}",
                             wraplength=280, anchor="w", justify="left"
                             ).grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 8))
        else:
            ctk.CTkLabel(self.task_list, text="No tasks yet.").grid(row=0, column=0, pady=10)  # empty state

        leaderboard = []
        for uname, udata in users.items():              # calculate points for every user
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
        leaderboard.sort(key=lambda x: x[1], reverse=True)  # sort by points descending

        ctk.CTkLabel(self.leaderboard_frame, text="Leaderboard",
                     font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(10, 4))

        if not leaderboard:
            ctk.CTkLabel(self.leaderboard_frame,
                         text="No contributions yet.\nChart appears once points are logged.",
                         text_color="gray").pack(pady=20)
            return

        medals = ["🥇", "🥈", "🥉"]  # top 3 get medals, rest get numbers
        for i, (uname, p) in enumerate(leaderboard):
            medal = medals[i] if i < 3 else f"{i+1}"
            if i < 5:                                    # only show top 5
                ctk.CTkLabel(self.leaderboard_frame,
                             text=f"{medal}  {uname}  —  {p} pts",
                             font=ctk.CTkFont(weight="bold") if uname == self.username else ctk.CTkFont(),
                             text_color="#4e9af1" if uname == self.username else "white"  # highlight current user
                             ).pack(anchor="w", padx=16, pady=2)

        names   = [n for n, _ in leaderboard]
        values  = [p for _, p in leaderboard]
        colours = ["#4e9af1", "#f1c94e", "#f17c4e", "#6ef14e",
                   "#c44ef1", "#4ef1c4", "#f14e7c", "#a0a0a0"][:len(names)]  # slice to match count

        fig, ax = plt.subplots(figsize=(3, 3), facecolor="#2b2b2b")  # dark background to match ctk theme
        ax.pie(values, labels=names, colors=colours, startangle=90,
               autopct="%1.0f%%", pctdistance=0.75,
               textprops={"color": "white", "fontsize": 7},
               wedgeprops={"linewidth": 1, "edgecolor": "#2b2b2b"})
        ax.set_facecolor("#2b2b2b")
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.leaderboard_frame)  # embed matplotlib figure in ctk
        canvas.draw()
        canvas.get_tk_widget().pack(pady=(6, 10))
        plt.close(fig)  # close figure to prevent memory leak

    def add_task(self):             AddTaskWindow(self, self.username)
    def add_contribution(self):     AddContributionWindow(self, self.username)
    def view_logs(self):            AdminLogsWindow(self)
    def view_all_tasks(self):       AdminAllTasksWindow(self)
    def view_all_contributions(self): AdminAllContributionsWindow(self)
    def view_all_users(self):       AdminAllUsersWindow(self)
    def delete_entry(self):         AdminDeleteWindow(self)

    def logout(self):
        self.destroy()          # close dashboard
        HomePage().mainloop()   # return to home page


class AddTaskWindow(ctk.CTkToplevel):
    def __init__(self, parent, username):
        super().__init__(parent)
        self.parent = parent
        self.username = username
        self.title("Add Task")
        self.geometry("320x350")
        self.grab_set()  # block interaction with dashboard while open

        ctk.CTkLabel(self, text="Add a Task", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)

        users = load_users()
        self.is_admin = users.get(username, {}).get("isAdmin", False)  # check if user is admin

        ctk.CTkLabel(self, text="Task Name:").pack()
        self.name_entry = ctk.CTkEntry(self, width=220)
        self.name_entry.pack(pady=4)

        if self.is_admin:                                              # admin can assign to any user
            ctk.CTkLabel(self, text="Assignee:").pack()
            all_names = list(users.keys())
            self.assignee_menu = ctk.CTkOptionMenu(self, values=all_names, width=220)
            self.assignee_menu.pack(pady=4)
            self._target = all_names[0] if all_names else username
        else:
            self._target = username                                    # normal users assign to themselves only

        ctk.CTkLabel(self, text="Difficulty (e = easy m = medium h = hard):").pack()
        self.difficulty_menu = ctk.CTkOptionMenu(self, values=["e", "m", "h"], width=220)
        self.difficulty_menu.pack(pady=4)

        ctk.CTkLabel(self, text="Comment:").pack()
        self.comment_entry = ctk.CTkEntry(self, width=220)
        self.comment_entry.pack(pady=4)

        ctk.CTkButton(self, text="Submit", command=self.submit).pack(pady=14)
        self.status_label = ctk.CTkLabel(self, text="", text_color="red")  # inline error feedback
        self.status_label.pack()

    def submit(self):
        users = load_users()
        assignee   = self.assignee_menu.get() if self.is_admin else self.username
        name       = self.name_entry.get().strip()
        difficulty = self.difficulty_menu.get().strip().lower()
        comment    = self.comment_entry.get().strip()

        if not name:                          # validate name
            self.status_label.configure(text="Task name is required.")
            return
        if assignee not in users:             # validate assignee exists
            self.status_label.configure(text="Assignee does not exist.")
            return

        obj = build_user_object(assignee, users[assignee])
        obj.add_task(cl.item(name=name, user=assignee, submittedtime=datetime.now().strftime("%Y-%m-%d %H:%M"), hours=0, difficulty=difficulty, comment=comment))
        users[assignee] = obj.dictafy()
        save_users(users)
        self.parent.refresh_dashboard()  # update dashboard immediately
        self.destroy()


class AddContributionWindow(ctk.CTkToplevel):
    def __init__(self, parent, username):
        super().__init__(parent)
        self.parent = parent
        self.username = username
        self.title("Add Contribution")
        self.geometry("340x420")
        self.grab_set()

        ctk.CTkLabel(self, text="Add a Contribution", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)

        users = load_users()
        self.is_admin = users.get(username, {}).get("isAdmin", False)

        if self.is_admin:                                              # admin can log against any user's tasks
            ctk.CTkLabel(self, text="Assignee:").pack()
            all_names = list(users.keys())
            self.assignee_menu = ctk.CTkOptionMenu(self, values=all_names, width=220,
                                                   command=self._load_tasks)  # reload tasks on change
            self.assignee_menu.pack(pady=4)
            self._target = all_names[0] if all_names else username
        else:
            self._target = username                                    # normal users log against their own tasks

        ctk.CTkLabel(self, text="Select Task:").pack()
        self._task_map = {}                                            # display label -> task dict
        self._build_task_map(users)
        task_labels = list(self._task_map.keys()) or ["— no tasks —"]
        self.task_menu = ctk.CTkOptionMenu(self, values=task_labels, width=220)
        self.task_menu.pack(pady=4)

        ctk.CTkLabel(self, text="Hours spent:").pack()
        self.hours_entry = ctk.CTkEntry(self, width=220)
        self.hours_entry.pack(pady=4)

        ctk.CTkLabel(self, text="Comment:").pack()
        self.comment_entry = ctk.CTkEntry(self, width=220)
        self.comment_entry.pack(pady=4)

        ctk.CTkButton(self, text="Submit", command=self.submit).pack(pady=14)
        self.status_label = ctk.CTkLabel(self, text="", text_color="red")
        self.status_label.pack()

        if self._task_map:                                             # pre-select first task if available
            self._on_task_select(task_labels[0])

    def _build_task_map(self, users):                                  # build label -> task dict for dropdown
        self._task_map = {}
        tasks = users.get(self._target, {}).get("tasks", [])
        for t in tasks:
            label = f"{t.get('name','?')}  [{t.get('difficulty','e').upper()}]"
            self._task_map[label] = t

    def _load_tasks(self, assignee):                                   # reload task dropdown when assignee changes
        self._target = assignee
        users = load_users()
        self._build_task_map(users)
        labels = list(self._task_map.keys()) or ["— no tasks —"]
        self.task_menu.configure(values=labels)
        self.task_menu.set(labels[0])
        if self._task_map:
            self._on_task_select(labels[0])

    def submit(self):
        users = load_users()
        selected_label = self.task_menu.get()

        if selected_label not in self._task_map:                       # validate task selection
            self.status_label.configure(text="Please select a valid task.")
            return

        task_data  = self._task_map[selected_label]
        hours_text = self.hours_entry.get().strip()
        comment    = self.comment_entry.get().strip()

        try:                                                           # validate hours is a positive number
            hours = float(hours_text)
            if hours < 0:
                raise ValueError
        except ValueError:
            self.status_label.configure(text="Hours must be a valid positive number.")
            return

        if self._target not in users:
            self.status_label.configure(text="User not found.")
            return

        obj = build_user_object(self._target, users[self._target])
        contrib = cl.contributions(
            name=task_data.get("name", ""),
            user=self._target,
            submittedtime=datetime.now().strftime("%Y-%m-%d %H:%M"),
            hours=hours,
            difficulty=task_data.get("difficulty", "e"),
            comment=comment
        )
        obj.add_contribution(contrib, task_uid=task_data.get("uid"))  # link contribution to task by uid
        users[self._target] = obj.dictafy()
        save_users(users)
        self.parent.refresh_dashboard()
        self.destroy()


class _AdminBaseWindow(ctk.CTkToplevel):  # shared base for all admin windows
    def __init__(self, parent, title, size="600x500"):
        super().__init__(parent)
        self.title(title)
        self.geometry(size)
        self.grab_set()
        ctk.CTkLabel(self, text=title, font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)  # window title
        self.body = ctk.CTkScrollableFrame(self)                                                 # scrollable card area
        self.body.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.body.grid_columnconfigure(0, weight=1)


class AdminLogsWindow(_AdminBaseWindow):  # shows last login time for all users
    def __init__(self, parent):
        super().__init__(parent, "Login Logs")
        users = load_users()
        if not users:
            ctk.CTkLabel(self.body, text="No users found.").grid(row=0, column=0, pady=10)
            return
        for i, (uname, udata) in enumerate(users.items()):  # card per user
            card = ctk.CTkFrame(self.body)
            card.grid(row=i, column=0, sticky="ew", padx=5, pady=4)
            card.grid_columnconfigure(0, weight=1)
            role = "Admin" if udata.get("isAdmin") else "Member"
            ctk.CTkLabel(card, text=f"{uname}  [{role}]",
                         font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w", padx=10, pady=(6, 2))
            ctk.CTkLabel(card, text=f"Last login: {udata.get('lastLogin','—')}",
                         text_color="gray").grid(row=1, column=0, sticky="w", padx=10, pady=(0, 6))  # secondary info in gray


class AdminAllTasksWindow(_AdminBaseWindow):  # shows every task across all users
    def __init__(self, parent):
        super().__init__(parent, "All Tasks")
        users = load_users()
        row = 0
        for uname, udata in users.items():
            tasks = udata.get("tasks", [])
            if not tasks:
                continue
            ctk.CTkLabel(self.body, text=f"── {uname} ──",
                         font=ctk.CTkFont(weight="bold"), text_color="#4e9af1"  # user header in blue
                         ).grid(row=row, column=0, sticky="w", padx=8, pady=(10, 2))
            row += 1
            for td in tasks:                                           # card per task
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


class AdminAllContributionsWindow(_AdminBaseWindow):  # shows every contribution with points
    def __init__(self, parent):
        super().__init__(parent, "All Contributions")
        users = load_users()
        row = 0
        for uname, udata in users.items():
            contribs = udata.get("contributions", [])
            if not contribs:
                continue
            ctk.CTkLabel(self.body, text=f"── {uname} ──",
                         font=ctk.CTkFont(weight="bold"), text_color="#4e9af1"  # user header in blue
                         ).grid(row=row, column=0, sticky="w", padx=8, pady=(10, 2))
            row += 1
            for cd in contribs:
                c_obj = cl.contributions(                              # build object to call _pointcalc
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


class AdminAllUsersWindow(_AdminBaseWindow):  # shows all users with stats
    def __init__(self, parent):
        super().__init__(parent, "All Users")
        users = load_users()
        if not users:
            ctk.CTkLabel(self.body, text="No users found.").grid(row=0, column=0, pady=10)
            return
        for i, (uname, udata) in enumerate(users.items()):
            pts = sum(                                                  # total points from all contributions
                cl.contributions(
                    name=c.get("name", ""), user=uname,
                    submittedtime=c.get("submittedtime", ""),
                    hours=c.get("hours", 0), difficulty=c.get("difficulty", "e"),
                    comment=c.get("comment", "")
                )._pointcalc()
                for c in udata.get("contributions", [])
            )
            card = ctk.CTkFrame(self.body)
            card.grid(row=i, column=0, sticky="ew", padx=5, pady=4)
            card.grid_columnconfigure(0, weight=1)
            role = "Admin" if udata.get("isAdmin") else "Member"
            ctk.CTkLabel(card, text=f"{uname}  {role}",
                         font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w", padx=10, pady=(6, 2))
            ctk.CTkLabel(card,
                         text=f"Hours: {udata.get('hours', 0)}  |  Tasks: {len(udata.get('tasks', []))}  |  Contributions: {len(udata.get('contributions', []))}  |  Points: {pts}",
                         text_color="gray").grid(row=1, column=0, sticky="w", padx=10, pady=(0, 6))  # stats in gray


class AdminDeleteWindow(ctk.CTkToplevel):  # admin window to delete a task or contribution
    def __init__(self, parent):
        super().__init__(parent)
        self.parent_dash = parent
        self.title("Delete Entry")
        self.geometry("400x380")
        self.grab_set()

        ctk.CTkLabel(self, text="Delete Task / Contribution",
                     font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)

        users = load_users()
        all_names = list(users.keys())

        ctk.CTkLabel(self, text="User:").pack()
        self.user_menu = ctk.CTkOptionMenu(self, values=all_names, width=260,
                                           command=self._load_entries)  # reload entries on user change
        self.user_menu.pack(pady=4)

        ctk.CTkLabel(self, text="Type:").pack()
        self.type_menu = ctk.CTkOptionMenu(self, values=["task", "contribution"], width=260,
                                           command=lambda _: self._load_entries(self.user_menu.get()))  # reload on type change
        self.type_menu.pack(pady=4)

        ctk.CTkLabel(self, text="Entry:").pack()
        self.entry_menu = ctk.CTkOptionMenu(self, values=["—"], width=260)
        self.entry_menu.pack(pady=4)

        ctk.CTkButton(self, text="Delete", fg_color="#c0392b",
                      command=self.do_delete).pack(pady=14)  # red = destructive action
        self.status_label = ctk.CTkLabel(self, text="", text_color="red")
        self.status_label.pack()

        if all_names:
            self._load_entries(all_names[0])  # pre-load entries for first user

    def _load_entries(self, username):                                 # reload entry dropdown on user/type change
        users = load_users()
        kind = self.type_menu.get()
        entries = users.get(username, {}).get(kind + "s", [])
        labels = [f"{e.get('name','?')}  [{e.get('submittedtime','')}]" for e in entries]
        self.entry_menu.configure(values=labels if labels else ["— none —"])
        self.entry_menu.set(labels[0] if labels else "— none —")

    def do_delete(self):
        users    = load_users()
        username = self.user_menu.get()
        kind     = self.type_menu.get()
        selected = self.entry_menu.get()

        if selected in ("— none —", "—"):                             # nothing selected, bail
            self.status_label.configure(text="Nothing to delete.")
            return

        entries     = users.get(username, {}).get(kind + "s", [])
        new_entries = []
        deleted     = False
        for e in entries:
            label = f"{e.get('name','?')}  [{e.get('submittedtime','')}]"
            if label == selected and not deleted:
                deleted = True                                         # skip only the first match (safe for duplicates)
            else:
                new_entries.append(e)

        if not deleted:
            self.status_label.configure(text="Entry not found.")
            return

        users[username][kind + "s"] = new_entries
        save_users(users)
        self.status_label.configure(text=f"Deleted '{selected}' from {username}.", text_color="green")
        self._load_entries(username)          # refresh dropdown
        self.parent_dash.refresh_dashboard()  # refresh dashboard


if __name__ == "__main__":
    app = HomePage()
    app.mainloop()
