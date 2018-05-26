import sqlite3   #enable control of an sqlite database

db_file = ""

def db_init(file_name):
    global db_file
    db_file = file_name

def db_setup():
    global db_file
    db = sqlite3.connect(db_file)
    c = db.cursor()
    querystring = """
    CREATE TABLE teams (
            team_num INTEGER PRIMARY KEY,
            name TEXT,
            location TEXT,
            robot_picture TEXT,
            member INTEGER,
            last_reached_worlds INTEGER
    );
    """
    c.execute(querystring)
    querystring = """
    CREATE TABLE match_performance (
            entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
            team_num INTEGER,
            match_num INTEGER,
            alliance INTEGER,
            user_id INTEGER,
            notes TEXT
    );
    """
    c.execute(querystring)
    
    querystring = """
    CREATE TABLE match_tasks (
            entry_id INTEGER,
            task_name TEXT,
            count INTEGER
    );
    """
    c.execute(querystring)
    
    querystring = """
    CREATE TABLE pre_scout (
            team_num INTEGER,
            auton_prediction INTEGER,
            teleop_prediction INTEGER,
            endgame_prediction INTEGER,
            notes TEXT
    );
    """
    c.execute(querystring)
    querystring = """
    CREATE TABLE users (
            user_id INTEGER PRIMARY KEY,
            name TEXT,
            password TEXT,
            permission INTEGER
    );
    """
    c.execute(querystring)
    db.commit()
    db.close()


def make_param_tuple(data):
    temp = []
    for key in data:
        if type(data[key]) == type({}):
            for inner in data[key]:
                temp.append(data[key][inner])
        else:
            temp.append(data[key])
    return tuple(temp)

def add_tasks_to_db(data):
    global db_file
    db = sqlite3.connect(db_file)
    c = db.cursor()
    
    param_tuple = (
        data["team"],
        data["match"],
        data["alliance"],
        data["u_id"],
        data["tasks"][0],
        data["tasks"][1],
        data["tasks"][2],
        data["tasks"][3],
        data["tasks"][4],
        data["tasks"][5],
        data["tasks"][6],
        data["tasks"][7],
        data["tasks"][8],
        data["tasks"][9],
        data["tasks"][10],
        data["tasks"][11],
        data["tasks"][12],
        data["notes"]
    )
    param_tuple = make_param_tuple(data)
    
    querystring = '''
        INSERT INTO match_performance VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''
    c.execute(querystring, param_tuple)
    db.commit()
    db.close()

def valid_login(u_id, pw):
    global db_file
    db = sqlite3.connect(db_file)
    c = db.cursor()
    
    param_tuple = (u_id, pw)
    querystring = """
        SELECT user_id, password FROM users WHERE user_id = ? AND password = ?
    """
    c.execute(querystring, param_tuple)

    res = c.fetchall()
    db.close()

    if len(res) > 0:
        return True
    return False

def add_user(data):
    '''
        Data should be in format:
        {
            "u_id": <number>,
            "name": <string>,
            "password": <string>,
            "permission": <number>
        }
    '''
    global db_file
    db = sqlite3.connect(db_file)
    c = db.cursor()
    
    param_tuple = (
        data["u_id"],
        data["name"],
        data["password"],
        data["permission"],
    )
    querystring = "INSERT INTO users VALUES (?, ?, ?, ?)"
    
    c.execute(querystring, param_tuple)
    db.commit()
    db.close()

def add_team(data):
    global db_file
    db = sqlite3.connect(db_file)
    c = db.cursor()
    
    '''
        Data should be in format:
        {
            "team": <number>,
            "team_name": <string>,
            "location": <string>,
            "num_mem": <number>,
            "notes": <string or null>,
            "pic": <string>
        }
    '''
    param_tuple();
    querystring = "INSERT INTO teams VALUES (?, ?, ?, ?, ?, ?)"
    
    c.execute(querystring, param_tuple)
    db.commit()
    db.close()

def get_team(data):
    querystring = "INSERT INTO teams VALUES (?, ?, ?, ?, ?, ?)"

if __name__ == "__main__":
    db_init("database.db")
    db_setup()

