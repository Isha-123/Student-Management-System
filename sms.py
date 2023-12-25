from tkinter import *
import time
import ttkthemes
from tkinter import ttk,messagebox,filedialog
import pymysql
import pandas

def iexit():
    result=messagebox.askyesno('Confirm','Do you want to exit?')
    if result:
       root.destroy()
    else:
        pass

def export_data():
    url=filedialog.asksaveasfilename(defaultextension='.csv')
    indexing=studentTable.get_children()
    newlist=[]
    for index in indexing:
        content=studentTable.item(index)
        datalist=content['values']
        newlist.append(datalist)

    table=pandas.DataFrame(newlist,columns=['Id','Name','class','Mobile No','city','Date of birth'])
    table.to_csv(url,index=False)
    messagebox.showinfo('Success','Data is saved successfully')


def toplevel_data(title,button_text,command):
    global idEntry,nameEntry,classEntry,mobileEntry,cityEntry,dobEntry,screen
    screen = Toplevel()
    screen.title(title)
    screen.grab_set()
    screen.resizable(0, 0)
    idLabel = Label(screen, text='Id', font=('times new roman', 13, 'bold'),fg='red')
    idLabel.grid(row=0, column=0, padx=30, pady=15)
    idEntry = Entry(screen, font=('times new roman', 13, 'bold'), width=24)
    idEntry.grid(row=0, column=1, pady=15, padx=10)

    nameLabel = Label(screen, text='Name', font=('times new roman', 13, 'bold'),fg='red')
    nameLabel.grid(row=1, column=0, padx=30, pady=15)
    nameEntry = Entry(screen, font=('times new roman', 13, 'bold'), width=24)
    nameEntry.grid(row=1, column=1, pady=15, padx=10)

    classLabel = Label(screen, text='Class', font=('times new roman', 13, 'bold'),fg='red')
    classLabel.grid(row=2, column=0, padx=30, pady=15)
    classEntry = Entry(screen, font=('times new roman', 13, 'bold'), width=24)
    classEntry.grid(row=2, column=1, pady=15, padx=10)

    mobileLabel = Label(screen, text='Mobile No', font=('times new roman', 13, 'bold'),fg='red')
    mobileLabel.grid(row=3, column=0, padx=30, pady=15)
    mobileEntry = Entry(screen, font=('times new roman', 13, 'bold'), width=24)
    mobileEntry.grid(row=3, column=1, pady=15, padx=10)

    cityLabel = Label(screen, text='City', font=('times new roman', 13, 'bold'),fg='red')
    cityLabel.grid(row=4, column=0, padx=30, pady=15)
    cityEntry = Entry(screen, font=('times new roman', 13, 'bold'), width=24)
    cityEntry.grid(row=4, column=1, pady=15, padx=10)

    dobLabel = Label(screen, text='Date of birth', font=('times new roman', 13, 'bold'),fg='red')
    dobLabel.grid(row=5, column=0, padx=30, pady=15)
    dobEntry = Entry(screen, font=('times new roman', 13, 'bold'), width=24)
    dobEntry.grid(row=5, column=1, pady=15, padx=10)

    student_button = ttk.Button(screen, text=button_text, command=command)
    student_button.grid(row=7, columnspan=2, pady=15)



    if title=='Update student':
        indexing = studentTable.focus()

        content = studentTable.item(indexing)
        listdata = content['values']
        idEntry.insert(0, listdata[0])
        nameEntry.insert(0, listdata[1])
        classEntry.insert(0, listdata[2])
        mobileEntry.insert(0, listdata[3])
        cityEntry.insert(0, listdata[4])
        dobEntry.insert(0, listdata[5])



def update_data():
    query='update student set name=%s,class=%s,city=%s where id=%s'
    mycursor.execute(query,(nameEntry.get(),classEntry.get(),cityEntry.get(),idEntry.get()))
    con.commit()
    messagebox.showinfo('success',f' Id{idEntry.get()} is modified successfully',parent=screen)
    screen.destroy()
    show_student()






def show_student():
    query = 'select * from student'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert('', END, values=data)



def delete_student():
    indexing=studentTable.focus()
    print(indexing)
    content=studentTable.item(indexing)
    content_id=content['values'][0]
    query='delete from student where id=%s'
    mycursor.execute(query,content_id)
    con.commit()
    messagebox.showinfo('Deleted',f' Id  {content_id} is deleted successfully')
    query='select * from student'
    mycursor.execute(query)
    fetched_data=mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert('', END, values=data)




def search_data():
    query='select *from student where id=%s or name=%s'
    mycursor.execute(query,(idEntry.get(),nameEntry.get()))
    studentTable.delete(*studentTable.get_children())
    fetched_data=mycursor.fetchall()
    for data in fetched_data:
        studentTable.insert('', END, values=data)




def add_data():
    if idEntry.get()=='' or nameEntry.get()=='' or classEntry.get()=='' or mobileEntry.get()=='' or cityEntry.get()=='' or dobEntry.get()=='':
       messagebox.showerror('Error','All fields are required',parent=screen)
    else:
         try:
             query='insert into student values(%s,%s,%s,%s,%s,%s)'
             mycursor.execute(query,(idEntry.get(),nameEntry.get(),classEntry.get(),mobileEntry.get(),cityEntry.get(),dobEntry.get()))
             con.commit()
             result=messagebox.askyesno('Confirm','Data added successfully.Do you want to clean the form?',parent=screen)
             if result:
                idEntry.delete(0,END)
                nameEntry.delete(0, END)
                classEntry.delete(0, END)
                mobileEntry.delete(0, END)
                cityEntry.delete(0, END)
                dobEntry.delete(0, END)

             else:
                 pass
         except:
             messagebox.showerror('Error','Id cannot be repeated',parent=screen)
             return

             query='select * from student'
             mycursor.execute(query)
             fetched_data=mycursor.fetchall()
             studentTable.delete(*studentTable.get_children())
             for data in fetched_data:
                studentTable.insert('',END,values=data)






def connect_database():
    def connect():
        global mycursor,con
        try:
            con=pymysql.connect(host='localhost',user='root',password='123')
            mycursor=con.cursor()
            messagebox.showinfo('Success','Database Connection is successfully',parent=connectWindow)

        except:
            messagebox.showerror('Error','Invalid Details',parent=connectWindow)
            return
        try:
            query='create database studentmanagementsystem'
            mycursor.execute(query)
            query='use studentmanagementsystem'
            mycursor.execute(query)
            query='create table student(Id int not null primary key,name varchar(30),class varchar(12),Mobile_no varchar(10),city varchar(12),Date_of_birth varchar(30))'
            mycursor.execute(query)
        except:
            query = 'use studentmanagementsystem'
            mycursor.execute(query)
        messagebox.showinfo('Success', 'Database Connection is successfully', parent=connectWindow)
        connectWindow.destroy()
        addstudentButton.config(state=NORMAL)
        searchstudentButton.config(state=NORMAL)
        deletestudentButton.config(state=NORMAL)
        updatestudentButton.config(state=NORMAL)
        showstudentButton.config(state=NORMAL)
        exportstudentButton.config(state=NORMAL)
        exitButton.config(state=NORMAL)


    connectWindow=Toplevel()
    connectWindow.grab_set()
    connectWindow.geometry('470x250+730+230')
    connectWindow.title('Databse Connection')
    connectWindow.resizable(0,0)

    hostnameLabel=Label(connectWindow,text='Host Name',font=('arial',23,  'bold'))
    hostnameLabel.grid(row=0,column=0,padx=20)

    hostEntry=Entry(connectWindow,font=(' roman',13,' bold'),bd=2)
    hostEntry.grid(row=0,column=1,padx=40,pady=20)

    UsernameLabel = Label(connectWindow, text='User name', font=('arial', 23, ' bold'))
    UsernameLabel.grid(row=1, column=0,padx=20)

    UsernameEntry = Entry(connectWindow, font=(' roman', 13, ' bold'), bd=2)
    UsernameEntry.grid(row=1, column=1, padx=40,pady=20)

    passwordLabel = Label(connectWindow, text='Password', font=('arial', 23, ' bold'))
    passwordLabel.grid(row=2, column=0, padx=20)

    passwordEntry = Entry(connectWindow, font=(' roman', 13, ' bold'), bd=2)
    passwordEntry.grid(row=2, column=1, padx=40, pady=20)

    connectButton=ttk.Button(connectWindow,text='Connect',command=connect)
    connectButton.grid(row=3,columnspan=2)


count=0
text=''
def slider():
    global text,count
    if count==len(s):
        count+0
        text=''
    text=text+s[count]
    sliderLabel.config(text=text)
    count+=1
    sliderLabel.after(300,slider)
def clock():
    date=time.strftime('%d/%m/%Y')
    currenttime=time.strftime('%H:%M:%S')
    datetimeLabel.config(text=f' Date:{date}\nTime:{currenttime}')
    datetimeLabel.after(1000,clock)
root=ttkthemes.ThemedTk()

root.get_themes()

root.set_theme('elegance')
root.geometry('1174x680+0+0')
root.resizable(0,0)
root.title('Student Management System')

datetimeLabel=Label(root,font=('times new roman',18,'bold'))
datetimeLabel.place(x=5,y=5)
clock()
s='Student Management System'
sliderLabel=Label(root,font=('times new roman',23,'italic bold'),width=30)
sliderLabel.place(x=200,y=0)
slider()

connectButton=ttk.Button(root,text='Connect database',command=connect_database)
connectButton.place(x=980,y=0)
leftFrame=Frame(root)
leftFrame.place(x=50,y=80,width=300,height=600)

logo_image=PhotoImage(file='student.png')
logo_Label=Label(leftFrame,image=logo_image)
logo_Label.grid(row=0,column=0)


addstudentButton=ttk.Button(leftFrame,text='Add Student',width=25,state=DISABLED,command=lambda :toplevel_data('Add student','Add ',add_data))
addstudentButton.grid(row=1,column=0,pady=20)

searchstudentButton=ttk.Button(leftFrame,text='Search Student',width=25,state=DISABLED,command=lambda :toplevel_data('Search student','Search',search_data))
searchstudentButton.grid(row=2,column=0,pady=20)

deletestudentButton=ttk.Button(leftFrame,text='Delete Student',width=25,state=DISABLED,command=delete_student)
deletestudentButton.grid(row=3,column=0,pady=20)

updatestudentButton=ttk.Button(leftFrame,text='Update Student',width=25,state=DISABLED,command=lambda :toplevel_data('Update student','Update',update_data))
updatestudentButton.grid(row=4,column=0,pady=20)

showstudentButton=ttk.Button(leftFrame,text='Show Student',width=25,state=DISABLED,command=show_student)
showstudentButton.grid(row=5,column=0,pady=20)

exportstudentButton=ttk.Button(leftFrame,text='Export Data',width=25,state=DISABLED,command=export_data)
exportstudentButton.grid(row=6,column=0,pady=20)

exitButton=ttk.Button(leftFrame,text='Exit',width=25,command=iexit)
exitButton.grid(row=7,column=0,pady=20)

rightFrame=Frame(root)
rightFrame.place(x=350,y=80,width=820,height=600)

scrollBarX=Scrollbar(rightFrame,orient=HORIZONTAL)
scrollBarY=Scrollbar(rightFrame,orient=VERTICAL)

studentTable=ttk.Treeview(rightFrame,columns=('Id','Name','class','Mobile no','city','Date of Birth'),
                          xscrollcommand=scrollBarX.set,yscrollcommand=scrollBarY.set)
scrollBarX.config(command=studentTable.xview)
scrollBarY.config(command=studentTable.yview)

scrollBarX.pack(side=BOTTOM,fill=X)
scrollBarY.pack(side=RIGHT,fill=Y)
studentTable.pack(fill=BOTH,expand=1)

studentTable.heading('Id',text='Id')
studentTable.heading('Name',text='Name')
studentTable.heading('class',text='class')
studentTable.heading('Mobile no',text='Mobile no')
studentTable.heading('city',text='city')
studentTable.heading('Date of Birth',text='Date of Birth')

studentTable.column('Id',width=50,anchor=CENTER)
studentTable.column('Name',width=200,anchor=CENTER)
studentTable.column('class',width=100,anchor=CENTER)
studentTable.column('Mobile no',width=200,anchor=CENTER)
studentTable.column('city',width=200,anchor=CENTER)
studentTable.column('Date of Birth',width=100,anchor=CENTER)

style=ttk.Style()

style.configure('Treeview',rowheight=40,font=('arial',10,'bold'),background='white',fieldbackground='white')
style.configure('Treeview.Heading',font=('arial',10,'bold'))
studentTable.config(show='headings')

root.mainloop()