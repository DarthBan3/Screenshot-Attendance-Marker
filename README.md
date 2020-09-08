# Screenshot-Attendance-Marker
Upload a screenshot and this program marks the attendance for you in a MySQL database. You can export the database as an Exel File whenever you want.

Limitations: This program currently only works for Windows devices, with 16:9 displays. Modifications to meet the differnt platforms and display ratios will be done in the next couple of versions.

Prerequsites: 

Software: PyTesseract OCR Engine, Python 3.6 or higher, and MySQL must be installed before hand.Preferably Dropbox as well. It automatically stores any screenshots you take.

Python Libraries:PyTesseract, Tkinter, Numpy, Python Image Library (PIL), mysql.connector, datetime, pandas.

Steps to setup: 

1. Make a text file with the list of the students in your class,and save it in the same folder as the main program.

2.Modify the "Reading file and making an SQL table.py" by replacing the userdata.---- with the relevant information to connect with your MySQL.Then, run the program "Reading file and making an SQL table.py"  It will create a table in your database with the list of students as one column.

3.Modify the "Main Program.py" so that a connection with MySQL is created and refers to the right database. Change the location of the tesseract cmd in line 145 to match with your particular installation.

4. Take a screenshot of your full desktop while zoom is open with list of participants open on the right hand portion of the display, and save it somewhere accessible. If you have Dropbox installed, it's as simple as pressing the print screen. Repeat if you have to take multiple screenshots to get all the students in the same list. 

5. Run "Main Program.py" In the GUI that pops up, press "Import Screenshots from Device" and select all your screenshots wherever you stored them. The program automatically updates the database with the attendance of the day. If you wish, you can export the table as an exel file. 
