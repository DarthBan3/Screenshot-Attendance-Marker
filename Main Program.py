from PIL import Image, ImageEnhance
import mysql.connector
import pytesseract as tess
from datetime import date
import numpy as np
import pandas as pd
import pymysql as pq
import tkinter
from tkinter import filedialog as fd
import userdata #You can skip this line if you are adding the connection deatils directly in line 147.



#Functions used in this program and stuff

def present(person, text):
    a1 = person.lower()
    a2 = person.upper()
    #Checks if the person, the person's name in Lowercase, or Person's name in Uppercase is there in the text
    if (a1 in text) or (a2 in text) or (person in text):
        return True
    else:
        return False

def crop(image):
    shape = np.shape(image)
    #Took the coordinates of a selection on a screenshot from My computer
    #Based on that position, here I'm taking the closest ratio
    #To crop out JUST the list of zoom participants

    left = shape[1]*1050//1366
    right = shape[1]*1351//1366
    top = shape[0]*100//768
    bottom = shape[0]*680//768

    #Using the PIL's Inbuilt function to crop the image
    new_image = image.crop((left, top, right, bottom))
    return new_image

#Exporting as an exel file
def export_exel():
    global connection
    df=pd.read_sql("select * from student;",connection)
    df.to_excel("Students attendance.xlsx")

#Main function put into a function so it runs when the button is pressed
def main_thing_executed_when_you_press_tkinter_button():
    a= fd.askopenfilenames()
    print(a)
    for fyl in a:
        # Importing and cropping image to only the part with the list of names
        image = Image.open(fyl)
        image = crop(image)  # Function is there in the definitions file

        # Enhancing the image so the words are more likely to pop out.
        enhancer = ImageEnhance.Contrast(image)
        image2 = enhancer.enhance(3)

        text = tess.image_to_string(image)
        # Reading the text in the screenshot
        print("THIS IS THE TEXT THAT YOU GET FROM THE IMAGE:")
        print(
            "______________________________________________________________________________________________________________")
        print(text)
        print(
            "______________________________________________________________________________________________________________")

        # Finding the date and converting it to a string. Replacing the MySQL's Unsupported Hyphens into an Underscore
        today = str(date.today())
        column_name = 'D'
        for i in today:
            if i == "-":
                column_name += '_'
            else:
                column_name += i

        try:
            # Creating a new row with the name "D+Date"
            stmt = "alter table student add " + column_name + " char(1);"
            cursor.execute(stmt)
            connection.commit()
        except:
            # IF program is run second time, there's no need to create a new column and it'll show an error
            print("Column exists already")

        cursor.execute("select student_name from student;")
        list_of_students = cursor.fetchall()
        # Getting the full list of all the students from the database
        # Arrives in the form of a list of tuples
        for i in range(len(list_of_students)):
            list_of_students[i] = (list_of_students[i][0], list_of_students[i][0].split())
            # Element of List = (student's name, [each part of student's name])

        for student in list_of_students:
            # Iterating with each student seperately
            for i in student[1]:
                if len(i) > 2:
                    x = present(i,
                                text)  # Function just checks if any part of the student's name is there in the text taken from image
                    if x:
                        print(student[0], 'is Present')
                        # Modifying the student's column under the created column as present
                        cursor.execute(
                            "update student set " + column_name + " = 'P' where student_name ='" + student[0] + "';")
                        connection.commit()
                        break
            else:
                # If the student isn't in the image, they could be either already marked, or are absent.
                cursor.execute("select " + column_name + " from student where student_name ='" + student[0] + "';")
                x = cursor.fetchall()
                # Taking what's already marked in the column. Present, Absent, or NULL
                if x[0][0] == "A":
                    # If student is marked absent, there's no need to make any more amends
                    print(student[0], "is Absent")
                    cursor.execute(
                        "update student set " + column_name + " = 'A' where student_name ='" + student[0] + "';")
                    connection.commit()
                elif x[0][0] == 'P':
                    # If student is marked present, there's no need to make further changes
                    print(student[0], 'is Present')
                    cursor.execute(
                        "update student set " + column_name + " = 'P' where student_name ='" + student[0] + "';")
                    connection.commit()
                else:
                    # If it's NULL, then it needs to be changed to Absent
                    print(student[0], 'is Absent')
                    cursor.execute(
                        "Update student set " + column_name + " = 'A' where student_name = '" + student[0] + "';")
                    connection.commit()

        # Printing the final database in the end
        cursor.execute('Select * from student')
        print(
            "______________________________________________________________________________________________________________")
        print("FINAL TABLE AFTER DOING THE UPDATES WITH THAT IMAGE")
        print(
            "______________________________________________________________________________________________________________")
        A = cursor.fetchall()
        for i in A:
            print(i)



#Connecting with Tesseract OCR. MODIFY THIS TO MATCH THE LOCATION OF PYTESSERACT IN YOUR INSTALLATION.
tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
#Conection with My SQL
connection = mysql.connector.connect(host = userdata.host,
                                     database = userdata.database,
                                     user = userdata.user,
                                     password = userdata.password)


#Checking connection with MySQL
db_Info = connection.get_server_info()
print("Connected to MySQL Server version ", db_Info)
#making a cursor to do work
cursor = connection.cursor()


#Making the Tkinter Interface
#Creating a window instance
window = tkinter.Tk()
#Giving the window a title
window.title("Attendance Program")


#Giving the details about the characteristics of all the buttons
export_exel_button = tkinter.Button(window, activebackground = 'red', activeforeground = 'yellow', bg = 'blue', fg = 'white',
                            text = "Export as exel file", width = 25, height = 5, command = export_exel)
#command = part calls the function mentioned so that it runs
import_image_button = tkinter.Button(window, activebackground = 'yellow', activeforeground = 'blue', bg = 'red', fg = 'white',
                            text = "Import Screenshots from Zoom", width = 25, height = 5, command=main_thing_executed_when_you_press_tkinter_button)

#packing the buttons into the window
import_image_button.pack()
export_exel_button.pack()

#Main Loop of the tkinter window
window.mainloop()

#Closing the MySQL Connection
connection.close()
