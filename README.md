<h1 style="font-size: 100px"> FairShare </h1>

To install past below into terminal: <br>
<code>pip install uuid customtkinter matplotlib pillow</code>

# KNOWN PROBLEMS

- When Opening new tabs, tkinter cannot multithread tasks, thus it might be unreactive.
    - To Solve this just click the tab on top (shown below in logging in)
- Deleting tasks can be buggy, this again is because of the multithreading. You might just have to wait a little bit for it to process or just search around tabs

# Logging in
First to Log in, enter your name into the entry box<br>
<img src="SS/Screenshot 2026-06-08 at 15.26.40.png" style = "width: 25%"><br>
(You might need to click the browser heading in order to type, this is a tkinter threading error on their side) THIS APPLIES FOR EVEY NEW TAB OPEN<br>
<img src="SS/Screenshot 2026-06-08 at 15.29.42.png" style = "width: 25%">

# Main Menu
In the Dashboard, You will see this menu:

<img src="SS/Screenshot 2026-06-08 at 15.37.47.png" style = "width: 50%">

## Refreshing
The Leaderboard or your tasks may update from time to time. To see changes, click refresh every so often to see changes.


## Adding a Task
Right now you have not tasks and no contributions. It should look something like this

<img src="SS/Screenshot 2026-06-08 at 15.37.12.png" style = "width: 25%">

Lets change that!

Click the add task button.

You should see something like this

<img src="SS/Screenshot 2026-06-08 at 15.45.43.png" style = "width: 25%">

Name is the Name of the task
Difficulty is how hard the task is
>e is easy <br>
>m is medium<br>
>h is hard<br>

The comment is any note or short description on what you should do

After adding a task it should appear in the main menu

<img src="SS/Screenshot 2026-06-13 at 11.46.16.png" style = "width: 25%">

## Adding a contribution
Click the add contribution button

It should look like this

<img src="SS/Screenshot 2026-06-08 at 15.58.20.png" style = "width: 25%">

First you must select a task (You most likely only have one)

The put how long the task took

then add a comment, though it is optional
## Logging out

Click the logout button on the bottom left 

# Admin
I've made a admin account for you, usually you would change the json file <br>
In the login entry box, type:
> alice 

<img src="SS/Screenshot 2026-06-08 at 15.29.20.png" style = "width: 25%">

You will see an admin panel in additioin to your simple tasks.

## Admin commands 
Since you are admin, you have a few extra commands at your disposal to regular other memebers.

### Adding tasks and contributions as Admin
When Addings task and Contributions, you can now <b>Assign</b> them to other memebers. 

 This can be accessed the same way you normally add a task or contribution

<img src="SS/Screenshot 2026-06-11 at 20.40.38.png" style = "width: 25%">
<img src="SS/Screenshot 2026-06-11 at 20.40.49.png" style = "width: 25%">

Each member can see their tasks assigned by you

### Viewing logs
You can see when each member has last logged on.

<img src="SS/Screenshot 2026-06-11 at 20.42.48.png" style = "width: 25%">

### Viewing tasks and contribs
You can see every task and contribution of every user

<img src="SS/Screenshot 2026-06-11 at 20.43.21.png" style = "width: 25%">
<img src="SS/Screenshot 2026-06-11 at 20.43.30.png" style = "width: 25%">

### Viewing users
You can see every user in the grouptask

<img src="SS/Screenshot 2026-06-11 at 20.43.36.png" style = "width: 25%">

### Deleting entries
You can delete a contribution or task. NOTE: after deleting, it might bug out a little bit.

<img src="SS/Screenshot 2026-06-11 at 20.43.43.png" style = "width: 25%">

You have to choose the user, type and specific task.
