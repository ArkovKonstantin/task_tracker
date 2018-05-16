from faker import Faker
from Connection import *
fake = Faker()
num_of_row = 10

con = Connection("root", "12345", "task_tracker")

name = fake.name()
with con:
    c = con.connection.cursor()
    for _ in range(num_of_row):
        c.execute("INSERT INTO users (name) VALUES (%s);", (fake.name(),))
    con.connection.commit()
        
    


