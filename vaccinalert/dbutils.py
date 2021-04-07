import pymysql

# Open database connection
# returns databse object db, cursor
def connect():
    db = pymysql.connect(host='localhost',user='root',password='',database='vaccinalert')
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    return db, cursor

def print_version(cursor):
    # execute SQL query using execute() method.
    cursor.execute("SELECT VERSION()")
    # Fetch a single row using fetchone() method.
    data = cursor.fetchone()
    print ("Database version : %s " % data)

# disconnect from server
# called when finished
def close(db):
    db.close()

def insert_email(email,region, db, cursor):
    sql = "INSERT INTO `Users` (`email`, `region`, `verified`) VALUES (%s, %s, FALSE)"
    cursor.execute(sql, (email, region))
    db.commit()

def get_all_verified_emails(region, db, cursor):
    sql = "SELECT `email` FROM `Users` WHERE `verified`=TRUE AND `region`=%s"
    cursor.execute(sql, (region))
    return cursor.fetchall()

    '''
    emails = []
    for tup in res:
        emails.append(tup[0])
    return emails
    '''

# Example usage:
# https://pymysql.readthedocs.io/en/latest/user/examples.html
#db,cursor = connect()
#insert_email("adam@aaa.com", "stockholm", db, cursor)
#res = get_all_verified_emails("stockholm", db,cursor)
#print(res)
