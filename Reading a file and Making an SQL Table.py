import userdata #You can remove this line when you're directly making a connection in line 5. 
import mysql.connector

#Making a connection
conn = mysql.connector.connect(
    host = userdata.host,
    database = userdata.database,
    user = userdata.user,
    password = userdata.password
)

#Setting Autocommit. Saves lines of code later on
conn.autocommit = True

#Checking if connection is connected
if conn.is_connected():
    print("Yeah")
else:
    print("Newp")

#Making a cursor
cursor = conn.cursor()

#Creating a new table with the name student
cursor.execute("create table student (roll_no int(3), student_name varchar(50));")

#Opening and reading a new file. Splitting it linewise. 
#MODIFY THIS ONE SO THAT YOUR PARTICULAR FILE WITH STUDENT'S NAMES is accessed.
fyl = open(r'E:\Coding Tools\Python\OCR\12_cs_studentnames.txt')
fyl_lines = fyl.read().split('\n')

#Inserting each student's name and roll number as a seperate record
i = 1
for line in fyl_lines:
    stmt = "insert into student(roll_no, student_name) values(" + str(i) + ", '" + line + "');"
    cursor.execute(stmt)
    i+=1

#Printing the entire table once just to make sure that the table is made properly
cursor.execute("Select * from student;")
print(cursor.fetchall())

#Closing the file
fyl.close()
#CLosing the MySQL COnnection
conn.close()
