#pip install mysql-connector-python

#from getpass import getpass
from mysql.connector import connect, Error
#from .Settings import settings

def run_query(hosts, port, db_query, user, pwd):
    try:
        result_all = []
        for host in hosts:     
            print(f'Host:{host}')                   
            # user=input("Enter username: "), password=getpass("Enter password: ")
            with connect(host=host,port=port, user=user,
                    password=pwd) as connection:  
                with connection.cursor() as cursor:                      
                    res = cursor.execute(db_query, multi=True)                                    
                    for result in res:                                      
                        if result.with_rows:
                            print("Rows produced by statement '{}':".format(result.statement))
                            res_list = result.fetchall()
                            for row in res_list:
                                print(row)
                            result_all.append(res_list)
                        else:
                            print("Number of rows affected by statement '{}': {}".format(
                            result.statement, result.rowcount))
                connection.commit() 
        return result_all        
    except Error as e:
        print(e)
    
    
    
#if __name__ == '__main__':   
def sql_request():
    hosts = ['localhost']
    port = 3306
    db_query = f"SELECT score,life FROM game.jackson;"
    res_list = run_query(hosts, port, db_query, 'user3', '123')
    #print("RESULT ALL")
    res = ''
    for row in res_list:
        #print(row)
        res = row
    
    res = list(res)
    #print(res[0][0])
    #print(res[0][1])
    return res[0]


def sql_update(score, life):
    hosts = ['localhost']
    port = 3306
    db_query = f"UPDATE game.jackson SET score = {score}, life = {life} WHERE (id = '1');"
    res_list = run_query(hosts, port, db_query, 'user3', '123')
    return res_list
