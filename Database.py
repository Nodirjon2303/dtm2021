import psycopg2

host = "localhost"
database = 'hotelbot'
user = 'myprojectuser'
password = 'Nodir2303'
conn = psycopg2.connect(
    host=host,
    database=database,
    user=user,
    password=password,
    port=5432
)
if conn:
    print("succesfully connected")
else:
    print('error')

cursor = conn.cursor()
sql = '''
    CREATE TABLE IF NOT EXISTS faculty(
    id SERIAL PRIMARY KEY ,
    university_id INTEGER , 
    faculty_id INTEGER , 
    status CHAR(7) default 'bad' 
    )
    '''
cursor.execute(sql)
sql2 = '''
    CREATE TABLE IF NOT EXISTS talaba(
    id SERIAL PRIMARY KEY ,
    name CHAR(255), 
    talaba_id INTEGER , 
    result CHAR(55)
    )
    '''
cursor.execute(sql2)
print('database succesfully created')
conn.commit()


def add(university_id, faculty_id):
    cursor.execute(f"INSERT INTO faculty (university_id, faculty_id) VALUES ({university_id}, {faculty_id})")
    conn.commit()


# cursor.execute("DELETE FROM faculty WHERE university_id = 306")
# conn.commit()

for i in range(1000000):
    faculty_id = int(input("Fakultitet id sini kiriting:\n"))
    add(314, faculty_id)
    print(f"succesfully added {faculty_id}\n")
