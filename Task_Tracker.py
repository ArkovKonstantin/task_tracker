from Connection import *


class TaskTracker:
    def __init__(self, db_connection, user_id):
        self.db_connection = db_connection.connection
        # Каждый экзепляр класса принадлежит определенному пользователю
        self.user_id = user_id
        self.dict_of_status = {1: 'new_task', 2: 'perform', 3: 'completed'}

    def add_task(self, id_parent=None):
        c = self.db_connection.cursor()
        # Проеряем, является ли данная задача вложенной
        if id_parent is not None:
            c.execute("INSERT INTO tasks (status, id_parent) VALUES (%s, %s);", (1, id_parent))
        else:
            c.execute("INSERT INTO tasks (status) VALUES (%s);", (1,))
        self.db_connection.commit()
        c.close()

    def perform(self, id_task):
        c = self.db_connection.cursor()

        # Меняем параметры родительской задачи
        c.execute("UPDATE tasks SET status = %s, user_id = %s WHERE id = %s;",
                  (2, self.user_id, id_task))

        # Получаем список дочерних задач
        c.execute("SELECT id FROM tasks WHERE id_parent = %s;", (id_task,))
        entries = c.fetchall()
        self.db_connection.commit()
        c.close()
        # Обрабатываем нижние уровни вложенности
        for task_id in entries:
            self.perform(task_id)

    def complete(self, id_task):
        c = self.db_connection.cursor()
        c.execute("UPDATE tasks SET status = %s WHERE id = %s;", (3, id_task))
        c.execute("SELECT id FROM tasks WHERE id_parent = %s;", (id_task,))
        entries = c.fetchall()
        self.db_connection.commit()
        c.close()
        for task_id in entries:
            self.complete(task_id)

    def get_status(self, id_task):
        c = self.db_connection.cursor()
        c.execute("SELECT status FROM tasks WHERE id = %s;", (id_task,))
        status = c.fetchone()
        c.close()
        return status[0]


con = Connection("root", "12345", "task_tracker")

with con:
    task = TaskTracker(con, 22)
    # task.add_task()
    # task.perform(4)
    task.complete(19)
    print(task.get_status(19))
