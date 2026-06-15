#import modules
from datetime import datetime
import uuid

#Member class
class member:
    #initializer, declare name, hours, lastLogin, isAdmin, contributions, tasks as attributes
    def __init__(self, name, hours=0, lastLogin=None, isAdmin=False, contributions=None, tasks=None):
        self.name = name
        self.hours = float(hours)
        #if lastLogin is does not exist, set it to the time now
        self.lastLogin = lastLogin if lastLogin else datetime.now().isoformat()
        self.isAdmin = isAdmin
        #if contributions or tasks are not provided, set them to an empty list
        self.contributions = contributions if contributions is not None else []
        self.tasks = tasks if tasks is not None else []
    #add task method
    def add_task(self, task):
        #if the task is an instance of item, add it to the tasks list
        if isinstance(task, item):#if instance exists 
            self.tasks.append(task.dictafy())#make it into a dict
        else: #if not, add it to the tasks list, by itself
            self.tasks.append(task)
#add contribution method
    def add_contribution(self, contribution, task_uid=None):
        #if the contribution is an instance of item, add it to the contributions list
        if isinstance(contribution, item): #if instance exist
            contribution_dict = contribution.dictafy()#make it into a dict
            self.contributions.append(contribution_dict)#add the dict to the list
            self.hours += float(contribution_dict.get("hours", 0))#get the hours from the dict and update hour attribute
        else:
            self.contributions.append(contribution)#add the contribution to the list
            self.hours += float(contribution.get("hours", 0))#update the hours
        #remove the original task by uid if provided
        if task_uid:
            self.tasks = [t for t in self.tasks if t.get("uid") != task_uid]

    def dictafy(self): #return the member's attributes as a dictionary
        return {
            "name": self.name,
            "hours": self.hours,
            "lastLogin": self.lastLogin,
            "isAdmin": self.isAdmin,
            "contributions": self.contributions,
            "tasks": self.tasks
        }

    def vomit(self):
        return self.dictafy()#return the dictionary as is

#Item class
class item:
    #initializer with name, user, submittedtime, hours, difficulty, comment as attributes
    def __init__(self, name, user, submittedtime, hours=0, difficulty="e", comment="", uid=None):
        self.name = name
        self.user = user
        self.submittedtime = submittedtime
        self.hours = float(hours)
        self.difficulty = difficulty.lower()
        self.comment = comment
        if uid:
            self.uid = uid
        else:
            self.uid = str(uuid.uuid4())  #generate a unique id if not provided
#pointcalc method, sets a map for the multiplier based on difficulty priv method
    def __pointcalculation(self):
        difficulty_map = {
            "e": 1,
            "m": 2,
            "h": 3
        }
        #if the difficulty is not in the map, return 0
        try:
            if self.difficulty not in difficulty_map:
                return(0)
        except Exception as e:
            print(e)
            return (0)
        #else, get the multiplier based on the difficulty
        multiplier = difficulty_map[self.difficulty]
        bonus = 0
        #if the comment is empty, subtract 30 from total scoer
        if self.comment is None or self.comment.strip() == "":
            bonus -= 30
        #if the hours are greater than 5, add 30 to total score and then multiply by 1.5
        if self.hours > 5:
            bonus += 30 * self.hours * 1.5
        #calculate the total score
        base = self.hours * multiplier * 10
        total = int(base + bonus)
        #returns the biggest score based on these calulations
        return max(total, 0)
    def _pointcalc(self):
        return item.__pointcalculation(self)
#dictafy method
    def dictafy(self):
        #return the item's attributes as a dictionary
        return {
            "uid": self.uid,  #unique id for task removal
            "name": self.name,
            "submittedtime": self.submittedtime,
            "hours": self.hours,
            "difficulty": self.difficulty,
            "comment": self.comment
        }

    @classmethod #classmethod for the from_dict method meaning that it is a static method that is based on class not instance
    def from_dict(cls , data, user=""):#gets data and user, instead of self, its cls
        return cls( #returns a new instance of the class
            name=data.get("name", ""),
            user=user,
            submittedtime=data.get("submittedtime", ""),
            hours=data.get("hours", 0),
            difficulty=data.get("difficulty", "e"),
            comment=data.get("comment", ""),
            uid=data.get("uid", None)  #preserve existing uid if present
        )

    def vomit(self):#returns the dictionary        
        return self.dictafy()

#Contributions class, this one is more of to hold the contributions as an temp obj that can be changed into a dict etc, instead of a static dict
class contributions(item):
    #initializer with name, user, submittedtime, hours, difficulty, comment as attributes
    def __init__(self, name, user, submittedtime, hours, difficulty, comment):
        super().__init__(name, user, submittedtime, hours, difficulty, comment)
    #vomit method, returns the dictionary as it
    def vomit(self):
        return self.dictafy()

#admin class
#REMOVE LATER MAYBE???? could just be in one class.
class admin(member):
    #initializer with name, hours, lastLogin, isadmin, contributions, tasks  
    def __init__(self, name, hours=0, lastLogin=None, isadmin=True, contributions=None, tasks=None):
        super().__init__(name, hours, lastLogin, True, contributions, tasks)
        self.isadmin = isadmin
    #override method, to give perms to change data etc
    def __override(self):
        return True