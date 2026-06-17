from datetime import datetime  # import datetime module
import uuid                     # import uuid module


class member:
    def __init__(self, name, hours=0, lastLogin=None, isAdmin=False, contributions=None, tasks=None):  # declare name, hours, lastLogin, isAdmin, contributions, tasks as attributes
        self.name = name
        self.hours = float(hours)
        self.lastLogin = lastLogin if lastLogin else datetime.now().isoformat()  # if lastLogin does not exist, set it to the time now
        self.isAdmin = isAdmin
        self.contributions = contributions if contributions is not None else []  # if contributions not provided, default to empty list
        self.tasks = tasks if tasks is not None else []                          # if tasks not provided, default to empty list

    def add_task(self, task):                    # add task to tasks list
        if isinstance(task, item):               # if task is an instance of item
            self.tasks.append(task.dictafy())    # convert to dict and append
        else:
            self.tasks.append(task)              # otherwise append as-is

    def add_contribution(self, contribution, task_uid=None):          # add contribution to contributions list
        if isinstance(contribution, item):                            # if contribution is an instance of item
            contribution_dict = contribution.dictafy()                # convert to dict
            self.contributions.append(contribution_dict)              # append dict to list
            self.hours += float(contribution_dict.get("hours", 0))    # update hours from dict
        else:
            self.contributions.append(contribution)                   # append contribution as-is
            self.hours += float(contribution.get("hours", 0))         # update hours
        if task_uid:                                                          # if task_uid provided
            self.tasks = [t for t in self.tasks if t.get("uid") != task_uid]  # remove original task by uid

    def dictafy(self):                                                        # return member attributes as a dictionary
        return {
            "name": self.name,
            "hours": self.hours,
            "lastLogin": self.lastLogin,
            "isAdmin": self.isAdmin,
            "contributions": self.contributions,
            "tasks": self.tasks
        }

    def vomit(self):                                                         # alias for dictafy
        return self.dictafy()


class item:
    def __init__(self, name, user, submittedtime, hours=0, difficulty="e", comment="", uid=None):# declare attributes
        self.name = name
        self.user = user
        self.submittedtime = submittedtime
        self.hours = float(hours)
        self.difficulty = difficulty.lower()
        self.comment = comment
        self.uid = uid if uid else str(uuid.uuid4()) # use provided uid or generate a new one

    def __pointcalculation(self):                    # private method, calculates score based on difficulty multiplier
        difficulty_map = {
            "e": 1,
            "m": 2,
            "h": 3
        }
        try:
            if self.difficulty not in difficulty_map:# if difficulty is invalid, return 0
                return 0
        except Exception as e:
            print(e)
            return 0

        multiplier = difficulty_map[self.difficulty] # get multiplier from map
        bonus = 0

        if self.comment is None or self.comment.strip() == "":  # no comment penalty
            bonus -= 30
        if self.hours > 5:                                      # high hours bonus
            bonus += 30 * self.hours * 1.5

        base = self.hours * multiplier * 10  # base score calculation
        total = int(base + bonus)
        return max(total, 0)                 # return highest possible score, minimum 0

    def _pointcalc(self):                    # public wrapper for private __pointcalculation
        return item.__pointcalculation(self)

    def dictafy(self):                       # return item attributes as a dictionary
        return {
            "uid": self.uid,                 # unique id used for task removal
            "name": self.name,
            "submittedtime": self.submittedtime,
            "hours": self.hours,
            "difficulty": self.difficulty,
            "comment": self.comment
        }

    @classmethod
    def from_dict(cls, data, user=""):                      # classmethod constructs instance from a dict instead of direct arugments
        return cls(
            name=data.get("name", ""),
            user=user,
            submittedtime=data.get("submittedtime", ""),
            hours=data.get("hours", 0),
            difficulty=data.get("difficulty", "e"),
            comment=data.get("comment", ""),
            uid=data.get("uid", None)                      # preserve existing uid if present
        )

    def vomit(self):                                       # alias for dictafy
        return self.dictafy()


class contributions(item):                                 # holds a contribution as a temp object, easier to convert than a static dict
    def __init__(self, name, user, submittedtime, hours, difficulty, comment):
        super().__init__(name, user, submittedtime, hours, difficulty, comment)

    def vomit(self):                                       # alias for dictafy
        return self.dictafy()


                                                           #REMOVE LATER? could potentially be merged into member class
class admin(member):
    def __init__(self, name, hours=0, lastLogin=None, isadmin=True, contributions=None, tasks=None):  # isAdmin forced True via super
        super().__init__(name, hours, lastLogin, True, contributions, tasks)
        self.isadmin = isadmin

    def __override(self):  # grants permission to modify data
        return True
