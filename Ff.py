import mysql.connector
import requests
mydb = mysql.connector.connect(
host = "127.0.0.1",
user = "root",
password = "2077",
database = "login_page"
)

cursor = mydb.cursor()

#[FOR_ADD_ROWS_INTO_TABLES]
# sqlFurmola = "INSERT INTO users ( UserName , Password) VALUES (%s , %s)"
# sqlFurmola1 = [("ali" , "09po09po"),("lp" "ko90ko87")]
# cursor.executemany(sqlFurmola , sqlFurmola1)

# mydb.commit()
# id = input("user:")
# pas = input("pasord:")

l = []
cursor.execute(f"SELECT * FROM user_pass" )
result = cursor.fetchall()
print(result)
for i in result:
    print(i)


# I = 0
# for i  in l :
#     if i[0] == id and i[1] == pas:
#             print("T")
#             break
#     elif i[0] == id and i[1] != pas :
#             print("is wrong pass")
#     else :
#             print("This acc is not exist")


# sql = "SELECT * FROM users WHERE UserName like '%m%'"
# cursor.execute(sql)
# result = cursor.fetchall()
# for i in result :
#     print(i)

# response = requests.get("https://api.myip.com")
# print(response.json()["ip"])
