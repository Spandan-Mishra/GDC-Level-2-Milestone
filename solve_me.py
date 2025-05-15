class TasksCommand:
    TASKS_FILE = "tasks.txt"
    COMPLETED_TASKS_FILE = "completed.txt"

    current_items = {}
    completed_items = []

    def read_current(self):
        try:
            file = open(self.TASKS_FILE, "r")
            for line in file.readlines():
                item = line[:-1].split(" ")
                self.current_items[int(item[0])] = " ".join(item[1:])
            file.close()
        except Exception:
            pass

    def read_completed(self):
        try:
            file = open(self.COMPLETED_TASKS_FILE, "r")
            self.completed_items = file.readlines()
            file.close()
        except Exception:
            pass

    def write_current(self):
        with open(self.TASKS_FILE, "w+") as f:
            f.truncate(0)
            for key in sorted(self.current_items.keys()):
                f.write(f"{key} {self.current_items[key]}\n")

    def write_completed(self):
        with open(self.COMPLETED_TASKS_FILE, "w+") as f:
            f.truncate(0)
            for item in self.completed_items:
                f.write(f"{item}\n")

    def run(self, command, args):
        self.read_current()
        self.read_completed()
        if command == "add":
            self.add(args)
        elif command == "done":
            self.done(args)
        elif command == "delete":
            self.delete(args)
        elif command == "ls":
            self.ls()
        elif command == "report":
            self.report()
        elif command == "help":
            self.help()

    def help(self):
        print(
            """Usage :-
$ python tasks.py add 2 hello world # Add a new item with priority 2 and text "hello world" to the list
$ python tasks.py ls # Show incomplete priority list items sorted by priority in ascending order
$ python tasks.py del PRIORITY_NUMBER # Delete the incomplete item with the given priority number
$ python tasks.py done PRIORITY_NUMBER # Mark the incomplete item with the given PRIORITY_NUMBER as complete
$ python tasks.py help # Show usage
$ python tasks.py report # Statistics"""
        )

    def add(self, args):
        priority = args[0]
        desc = args[1]
        if(self.current_items.get(int(priority))):
            self.current_items[int(priority)+1] = self.current_items[int(priority)]
            self.current_items[int(priority)] = desc
        else:
            self.current_items[int(priority)] = desc
        print(f"Added task: \"{desc}\" with priority {priority}")
        self.write_current()
        pass

    def done(self, args):
        priority = args[0]
        if self.current_items.get(int(priority)):
            completed_item = self.current_items[int(priority)]
            self.completed_items.append(completed_item)
            del self.current_items[int(priority)]
            print(f"Marked item as done.")
            self.write_current()
            self.write_completed()
        else:
            print(f"Error: no incomplete item with priority {priority} exists.")
        pass

    def delete(self, args):
        priority = args[0]
        if self.current_items.get(int(priority)):
            del self.current_items[int(priority)]
            print(f"Deleted item with priority {priority}")
            self.write_current()
        else:
            print(f"Error: item with priority {priority} does not exist. Nothing deleted.")
        pass

    def ls(self):
        i = 1
        for key in sorted(self.current_items.keys()):
            print(f"{i}. {self.current_items[key]} [{key}]")
            i+= 1
        pass

    def report(self):
        self.read_current()
        self.read_completed()
        print(f"Pending : {len(self.current_items)}")
        i = 1
        for key in sorted(self.current_items.keys()):
            print(f"{i}. {self.current_items[key]} [{key}]")
            i+= 1
        print()
        i = 1
        print(f"Completed : {len(self.completed_items)}")
        for item in self.completed_items:
            if item != "\n":
             print(f"{i}. {item[:-1]}")
             i+= 1
        pass
