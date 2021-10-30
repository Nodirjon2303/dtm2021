import requests
from bs4 import BeautifulSoup
import datetime
from sqlite3 import connect
import psycopg2


def all_student():
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
    try:
        cursor.execute(f"SELECT talaba_id FROM talaba")
        res = cursor.fetchall()
    except Exception as e:
        print(e+"line29")
    conn.close()
    return res


class region_time:
    def __init__(self, fac_id, univer_id):
        self.fac_id = fac_id
        self.univer_id = univer_id
        self.time = f'https://mandat.dtm.uz/Home/AfterFilter?name=&region=14&university={self.univer_id}&faculty={self.fac_id}&edLang=1&edType=1'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
        self.full_page = requests.get(self.time, self.headers)
        self.soup = BeautifulSoup(self.full_page.content, 'html.parser')
        self.convert = self.soup.findAll('div', {'class': 'alert'}, '<b>')
        print("NATIJA:", self.convert[0])
        self.convert = str(self.convert)
        a = self.convert.rfind("<b>")
        b = self.convert.find(' ', a+4)
        print("a=", a)
        print('b=', b)
        self.ariza_soni = int(self.convert[a+3:b])
        print('Jami arizalar soni', self.ariza_soni)
        if int(self.ariza_soni) > 10:
            pass
        else:
            return None
        self.talaba = self.soup.find_all('tr')
        try:
            print("TEXT: ", self.talaba[4].text.split('\n'))
        except Exception as e:
            print(e+"line60")
        jami_talaba = all_student()
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

        for i in range(1, 11):
            a = self.talaba[i].text.split('\n')
            print("A:", a)
            try:
                print(a[2], a[1], a[5])
                if int(a[1]) not in jami_talaba[0]:
                    cursor.execute(
                        f"INSERT INTO talaba (name, talaba_id, result ) VALUES('{a[2]}' , {int(a[1])} ,'{a[5]}')")
                    conn.commit()
                else:
                    print(f"Ushbu talaba jadvalda mavjud: {a[1]}")
            except Exception as e:
                print(e+"line 91")
        conn.close()
        print("ARIZA", self.ariza_soni // 10 + 1)

    def get_users(self):
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
        for i in range(2, self.ariza_soni // 10 + 1):
            self.url = f'https://mandat.dtm.uz/Home/AfterFilter?page={i}&region=14&university={self.univer_id}&faculty={self.fac_id}&edLang=1&edType=1&nog=False&muy=False&soldier=False&iiv=False&prez=0&sortorder=ResultDesc'
            self.full_page = requests.get(self.url, self.headers)
            self.soup = BeautifulSoup(self.full_page.content, 'html.parser')
            self.talaba = self.soup.find_all('tr')
            jami_talaba = all_student()
            for j in range(1, 11):
                a = self.talaba[j].text.split('\n')
                print(a)
                try:
                    print(a[2], a[1], a[5])
                    if int(a[1]) not in jami_talaba[0]:
                        cursor.execute(
                            f"INSERT INTO talaba (name, talaba_id, result ) VALUES('{a[2]}' , {int(a[1])} ,'{a[5]}')")
                        conn.commit()
                    else:
                        print(f"Ushbu talaba jadvalda mavjud: {a[1]}")
                except Exception as e:
                    print(e+"line130")
        print(f'DATABASEGA {self.ariza_soni}', 'ta talaba yozildi')
        conn.close()


def fac_id():
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
    try:
        cursor.execute("""
        SELECT university_id, faculty_id FROM faculty
        WHERE status = 'bad'
""")
        res = cursor.fetchall()
    except Exception as e:
        print(e+"line159")
    conn.close()
    return res

def status_edit(fac_id):
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
    try:
        cursor.execute(f"UPDATE faculty SET status = 'good' WHERE faculty_id = {fac_id}")
        conn.commit()
    except Exception as e:
        print(e+"line184")
    conn.close()


faculties = fac_id()
print('Fakultitetlar:' , faculties)
for i in faculties:
    A = region_time(i[1], i[0])
    print(i[0], "id lik fakultet talabalari yozilmoqda DATABASEGA")

    A.get_users()
    status_edit(i[1])

