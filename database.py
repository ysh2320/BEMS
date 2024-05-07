# database.py
import pymssql

conn = pymssql.connect(server='localhost', database='BEMS', charset='utf8')

def get_user(id, password):
    cursor = conn.cursor(as_dict=True)
    query = "SELECT * FROM Member WHERE M_ID = %s AND M_Password = %s"
    params = (id, password)
    cursor.execute(query, params)
    row = cursor.fetchone()
    if row:
        user = {
            'id': row['M_id'],
            'name': row['M_name'],
            'age': row['M_age'],
            'password': row['M_password'],
            'floorID' : row['M_floorID'],
            'buildID' : row['M_buildingId'],
        }
        return user
    else:
        return None


def login_admin(id, password):
    cursor = conn.cursor(as_dict=True)
    query = "SELECT * FROM admin WHERE A_id = %s AND A_password = %s"
    params = (id, password)
    cursor.execute(query, params)
    row = cursor.fetchone()
    if row:
        admin = {
            'id': row['A_id']
        }
        return admin
    else:
        return None


def get_admin(id):
    cursor = conn.cursor(as_dict=True)
    query = "SELECT * FROM admin WHERE A_id = %s"
    params = (id)
    cursor.execute(query, params)
    row = cursor.fetchone()
    if row:
        admin = {
            'id': row['A_id'],
            'name': row['A_name'],
            'age': row['A_age'],
            'secPassword': row['A_secpassword'],
            'buildid' :  row['A_buildID'],
            'walletAddress':row['A_walletaddress']
        }
        return admin
    else:
        return None
