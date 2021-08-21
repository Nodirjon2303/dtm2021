import psycopg2

host = "ec2-18-211-41-246.compute-1.amazonaws.com"
database = 'd5jdt4hbsg5qai'
user = 'wsdvanlxnpdmfo'
password = '179ce8e470717e7b3296955ddda0d79cac002e492b30f9a869f0f6f2e1fdefcf'
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
print('database succesfully created')
conn.commit()

def add(university_id, faculty_id):
    cursor.execute(f"INSERT INTO faculty (university_id, faculty_id) VALUES ({university_id}, {faculty_id})")
    conn.commit()

# cursor.execute("DELETE FROM faculty WHERE university_id = 306")
# conn.commit()

for i in range(1000000):
    faculty_id = int(input("Fakultitet id sini kiriting:\n"))
    add(315, faculty_id)
    print(f"succesfully added {faculty_id}\n")




