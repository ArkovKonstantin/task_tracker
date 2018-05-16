from Connection import *


class TaskTracker:
    def __init__(self, db_connection, user_id):
        self.db_connection = db_connection.connection
        self.user_id = user_id
        self.dict_of_status = {1: 'ожидает выполнения', 2: 'выполняется', 3: 'завершена'}

    def add_task(self, id_parent=None):
        c = self.db_connection.cursor()
        if id_parent is not None:
            c.execute("INSERT INTO tasks (status, id_parent) VALUES (%s, %s);", (1, id_parent))
        else:
            c.execute("INSERT INTO tasks (status) VALUES (%s);", (1,))
        self.db_connection.commit()
        c.close()


con = Connection("root", "12345", "task_tracker")

with con:
    task = TaskTracker(con, 19)
    task.add_task()
