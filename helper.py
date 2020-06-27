import sqlite3
import smtplib
from email.message import EmailMessage
from flask_bcrypt import Bcrypt
import random
import string

DB_PATH = './forms.db'  
bcrypt = Bcrypt()

def add_members(req_data):
    members = [tuple(e) for e in req_data['members']]
    length = req_data['length']

    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        s = ''
        for i in range(length):
            s += f'{members[i]}'
            if (length - 1 != i):
                s += ','
        
        print(s)

        c.execute('insert into members (Name, Email, `Group`) values {}'.format(s))
        conn.commit()
        return {"Result": "Members Added"}

    except Exception as e:
        return {"error": str(e)}

def get_all_member():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""select * from members 
                        order by case 
                            when `Group` = 'junior' then 1
                            when `Group` = 'cadet two' then 2
                            when `Group` = 'cadet one' then 3
                            when `Group` = 'crusader' then 4
                            when `Group` = 'leader' then 5 
                        end;""")
        rows = c.fetchall()
        return { "count": len(rows), "members": rows }
    except Exception as e:
        return {"error": str(e)}

def get_member_names():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""select Name from members""")
        rows = [row[0] for row in c.fetchall()]
        return { "names": rows }
    except Exception as e:
        return {"error": str(e)}

def update_group(req_data):
    data = [tuple(e) for e in req_data['data']]
    length = req_data['length']

    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        c.execute('delete from members')
        
        s = ''
        for i in range(length):
            s += f'{data[i]}'
            if (length - 1 != i):
                s += ','

        c.execute('insert into members values {}'.format(s))
        conn.commit()

        return {'status': 'members updated'}
    except Exception as e:
        return {"error": str(e)}

def delete_members(req_data):
    members = req_data['members']
    length = req_data['length']

    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        s = ''
        for i in range(length):
            s += f'Name="{members[i]}"'
            if (length - 1 != i):
                s += ' or '

        c.execute("delete from members where {}".format(s))
        conn.commit()
        return {"Result": "Members Deleted"}
    except Exception as e:
        return {"error": str(e)}

def add_columns(req_data):
    columns = req_data['columns']

    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        for column in columns:
            c.execute('alter table members add {} TEXT default "no"'.format(column.replace(" ", "_")))

        conn.commit()
        return {"Added": columns}

    except Exception as e:
        return {"error": str(e)}


def delete_columns(req_data):
    columns = req_data['columns']

    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        c.execute("PRAGMA table_info(members)")
        column_names = []
        results = c.fetchall()
        for entry in results:
            if entry[1] not in columns:
                columnstr = ''
                columnstr += f'"{entry[1]}" {entry[2]}'
                if (int(entry[3]) == 1):
                    columnstr += ' not null'
                if (int(entry[5]) == 1):
                    columnstr += ' primary key'

                column_names.append(columnstr)
        
        column_names = ','.join(column_names)
        print(column_names)

        c.execute('create table temp({})'.format(column_names))

        results = [f'"{entry[1]}"' for entry in results if entry[1] not in columns]
        results = ','.join(results)
        print(results)
        c.execute('insert into temp select {} from members'.format(results))
        c.execute('drop table if exists members')
        c.execute('alter table temp rename to members')

        conn.commit()
        return {'deleted': columns}
    except Exception as e:
        return {"error": str(e)}


def get_table():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("PRAGMA table_info(members)")
        columns = c.fetchall()
        columns = [entry[1] for entry in columns ]
        return columns
    except Exception as e:
        return {"error": str(e)}


def send_email(req_data):
    members = req_data['members']

    try:
        with smtplib.SMTP('smtp-mail.outlook.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()

            smtp.login('calvin.chen@sjabcy.ca', 'Xeifoo4x')

            for member in members:
                msg = EmailMessage()
                msg['Subject'] = 'Missing Fees and Forms'
                msg['From'] = 'calvin.chen@sjabcy.ca'

                forms = ''
                for i in range(2, len(member)):
                    forms += f'{member[i]}\n'
                msg['To'] = f'{member[1]}'
                content = f'Hi {member[0]},\n\nYou are missing the following forms:\n\n{forms}\n\nThanks,\nCalvin Chen'
                msg.set_content(content)

                smtp.send_message(msg)
        return {"Emails": "Sent"}
    except Exception as e:
        return {"error": str(e)}

def login(req_data):
    user_name = req_data['user'].lower()
    password = req_data['pass']

    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("select * from users where user='{}'".format(user_name))
        user_data = c.fetchone()
        print(user_data)

        if user_data is None:
            return {"error": "User Not Found"}

        if bcrypt.check_password_hash(user_data[1], password):
            access_token = ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))
            
            c.execute("update users set access_token='{}' where user='{}'".format(access_token, user_data[0]))
            conn.commit()

            return {'access_token': access_token, 'permissions': user_data[3]}

        return {'error': 'Incorrect Password'}
    except Exception as e:
        return {"error": str(e)}


def auth(req_data):
    token = req_data['access_token']

    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("select * from users where access_token='{}'".format(token))
        user_data = c.fetchone()

        if user_data is None:
            return {"error": "User Is Not Logged In"}
            
        return {"success": "User Logged In"}
    except Exception as e:
        return {"error": str(e)}
