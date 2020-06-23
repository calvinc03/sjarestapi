import sqlite3

DB_PATH = './forms.db'   # Update this path accordingly

def add_members(req_data):
    members = [tuple(e) for e in req_data['members']]
    group = req_data['group']
    length = req_data['length']

    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        s = ''
        for i in range(length):
            s += f'{members[i]}'
            if (length - 1 != i):
                s += ','

        c.execute('insert into {} (name, email) values {}'.format(group, s))
        conn.commit()
        return {group: "Members Added"}

    except Exception as e:
        return {"error": str(e)}

def get_all_member(group):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("select * from {}".format(group))
        rows = c.fetchall()
        return { "count": len(rows), "members": rows }
    except Exception as e:
        return {"error": str(e)}


def update_group(req_data):
    group = req_data['group']
    data = [tuple(e) for e in req_data['data']]
    length = req_data['length']

    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        c.execute('delete from {}'.format(group))
        
        s = ''
        for i in range(length):
            s += f'{data[i]}'
            if (length - 1 != i):
                s += ','

        c.execute('insert into {} values {}'.format(group, s))
        conn.commit()

        return {'status': f'{group} updated'}
    except Exception as e:
        return {"error": str(e)}

def delete_members(req_data):
    members = req_data['members']
    group = req_data['group']
    length = req_data['length']

    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        s = ''
        for i in range(length):
            s += f'name="{members[i]}"'
            if (length - 1 != i):
                s += ' or '

        c.execute("delete from {} where {}".format(group, s))
        conn.commit()
        return {group: "Members Deleted"}
    except Exception as e:
        return {"error": str(e)}

def add_columns(req_data):
    column = req_data['column'].replace(" ", "_")
    groups = req_data['groups']

    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        for group in groups:
            c.execute('alter table {} add {} TEXT default "no"'.format(group, column))

        conn.commit()
        return {"column": column}

    except Exception as e:
        return {"error": str(e)}


def delete_columns(req_data):
    columns = req_data['columns']
    group = req_data['group']

    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        c.execute("PRAGMA table_info({})".format(group))
        column_names = []
        results = c.fetchall()
        for entry in results:
            if entry[1] not in columns:
                columnstr = ''
                columnstr += f'{entry[1]} {entry[2]}'
                if (int(entry[3]) == 1):
                    columnstr += ' not null'
                if (int(entry[5]) == 1):
                    columnstr += ' primary key'

                column_names.append(columnstr)
        
        column_names = ','.join(column_names)

        c.execute('create table temp({})'.format(column_names))

        results = [entry[1] for entry in results if entry[1] not in columns]
        results = ','.join(results)

        c.execute('insert into temp select {} from {}'.format(results, group))
        c.execute('drop table if exists {}'.format(group))
        c.execute('alter table temp rename to {}'.format(group))

        conn.commit()
        return {'deleted': columns}
    except Exception as e:
        return {"error": str(e)}


def get_table(group):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("PRAGMA table_info({})".format(group))
        columns = c.fetchall()
        columns = [entry[1] for entry in columns ]
        return columns
    except Exception as e:
        return {"error": str(e)}