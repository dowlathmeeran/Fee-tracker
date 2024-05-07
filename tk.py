import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import mysql.connector
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, TableStyle,Spacer 
from reportlab.lib import colors 
from reportlab.lib.pagesizes import A4 
from reportlab.lib.styles import getSampleStyleSheet
from tkinter import messagebox
from datetime import datetime
#from uuid import uuid4
from os import path
from twilio.rest import Client
from io import BytesIO

'''def send_sms(to_phone, message_body, account_sid, auth_token, from_phone):
    try:
        account_sid = 'AC214f3b989948b7462000dc8e7107e530'
        auth_token = '5876cd4bf0fe526cd6b1da59b513335e'   
        from_phone_number = '+16206708899'  
        pdf_directory = 'E:/python/python project/receipt'
        receipt_number = f"R-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        pdf_filename = path.join(pdf_directory, f"{receipt_number}.pdf")

        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body=message_body,
            from_=from_phone,
            to=to_phone
        )
        
        return message.sid
    except Exception as e:
        print(f"Error sending SMS: {e}")
        return None





    try:
        account_sid = 'AC214f3b989948b7462000dc8e7107e530'
        auth_token = '5876cd4bf0fe526cd6b1da59b513335e'   
        from_phone_number = '+16206708899'  
        pdf_directory = 'E:/python/python project/receipt'
        receipt_number = f"R-{datetime.now().strftime('%Y%m%d%H%M%S')}-{str(student_id)[-4:]}"
        pdf_filename = path.join(pdf_directory, f"{receipt_number}.pdf")

        paying_amount = entry_am.get()
        paying_amounts = int(paying_amount)
        student_id = entry_stu.get()


        to_phone_number = '+919500470870'
        message_body = f'Hi Sir/Madam, Payment received. Receipt Number: {receipt_number}'

        sms_sid = send_sms(to_phone_number, message_body, account_sid, auth_token, from_phone_number)

        messagebox.showinfo("Success", f"Receipt generated successfully: {pdf_filename}\nSMS sent with SID: {sms_sid}")
    except Exception as e:
        messagebox.showerror("Error", f"Error generaating receipt: {e}")
'''
def generate_receipt(student_id): 
    receipt_number = f"R-{datetime.now().strftime('%Y%m%d%H%M%S')}-{str(student_id)[-4:]}"
    paying_amount = entry_am.get()
    paying_amounts = int(paying_amount)
    student_id = entry_stu.get()

    student_details = fetch_student_details(student_id)
    if student_details:
        pdf_directory = 'E:/python/python project/receipt'
        pdf_filename = path.join(pdf_directory, f"{receipt_number}.pdf")

        pdf = SimpleDocTemplate(pdf_filename, pagesize=A4)
        styles = getSampleStyleSheet()
        content = []
        

        college_name_style = styles["Heading1"]
        college_name_style.alignment = 1
        college_name_style.fontsize=50
        college_name = Paragraph("Hogwarts University", college_name_style)
        content.append(college_name)

        college_addres_style = styles["Heading4"]
        college_addres_style.alignment = 1
        college_addres_style.fontSize=8
        college_addres = Paragraph("NAAC 'A' Grade, MHRD NIRF University Ranking 2022: 12", college_addres_style)
        content.append(college_addres)

        spacer = Spacer(1, -15.5)
        content.append(spacer)


        college_address_style = styles["Heading4"]
        college_address_style.alignment = 1
        #college_address_style.fontSize=14
        college_address = Paragraph("0492, Hercules Street,Valencia,Somalia AZ143", college_address_style)
        content.append(college_address)

        title_style = styles["Heading4"]
        title_style.alignment = 1
        #college_name_style.fontSize=14
        fees_receipt = Paragraph("FEES RECEIPT", title_style)
        content.append(fees_receipt)
        
        style = TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 1, colors.black),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgreen),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("BACKGROUND", (0, 1), (-1, -1), colors.white),
            ]
        )
        table_data = []

        if student_details:
            headers = ['Student ID', 'Name', 'Major', 'Phone Number']
            for header, value in zip(headers, student_details):
                table_data.append([header, str(value)])

        table = Table(table_data, style=style)
        content.append(table)
        
        spacer = Spacer(1, 20)
        content.append(spacer)

        receipt_no_style = styles["Heading5"]
        receipt_no_style.alignment = 0
        receipt_no = Paragraph(f"Receipt Number: {receipt_number}",  receipt_no_style)
        content.append(receipt_no)

        paying_amount = entry_am.get()
        DATA = [
            ["  SI.NO  ", "                                              Particulars                                              ", "  Amount  "],
            ["1", "Education Fees", str(paying_amounts)],
            ["",  ],
            ["",  ],
            ["",  ],
            ["",  ],
            ["", "Total amount: ", str(paying_amounts)],
        ]
        style1 = TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 1, colors.black),
                ("GRID", (0, 0), (2, 5), 1, colors.black),
                ("BACKGROUND", (0, 0), (2, 0), colors.gray),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ]
        )
        table1 = Table(DATA, style=style1)
        content.append(table1)
        
        spacer = Spacer(1, 20)
        content.append(spacer)

        if paying_amounts < 22000:
            bal = 22000 - paying_amounts
            balance_style = styles["Normal"]
            balance_style.alignment = 0
            balance = Paragraph("Pending Amount is "+str(bal)+" /-", balance_style)
            content.append(balance)
        else:
            nill_style = styles["Normal"]
            nill_style.alignment = 0
            nill = Paragraph("Pending Amount is NILL ", nill_style)
            content.append(nill)

        spacer = Spacer(1, 20)
        content.append(spacer)
            
        current_date = datetime.now().strftime("%Y-%m-%d")
        date_style = styles["Heading5"]
        date_style.alignment = 0
        date_paragraph = Paragraph(f"Date: {current_date}", date_style)
        content.append(date_paragraph)

        current_time = datetime.now().strftime("%H:%M:%S")
        time_style = styles["Heading5"]
        time_style.alignment = 0
        time_paragraph = Paragraph(f"Time: {current_time}", time_style)
        content.append(time_paragraph)

        spacer = Spacer(1, -15.5)
        content.append(spacer)


        cash_holder_signature_style = styles["Normal"]
        cash_holder_signature_style.alignment = 2
        cash_holder_signature_paragraph = Paragraph("Cash Holder Signature: ____________________", cash_holder_signature_style)
        content.append(cash_holder_signature_paragraph)

        pdf.build(content)

        messagebox.showinfo("Success", f"Receipt generated successfully: {pdf_filename}")
    else:
        messagebox.showinfo("Info", "No student details found for the given ID.")

def fetch_student_details(student_id):
    try:
        db = mysql.connector.connect(host="localhost", user="root", password="2003", database="university")
        cursor = db.cursor()
        cursor.execute("SELECT StudentID, CONCAT(FirstName, ' ', LastName) as Name, Major, PH_number FROM students WHERE StudentID = %s", (student_id,))
        student_details = cursor.fetchone()
        db.close()
        return student_details
    except Exception as e:
        messagebox.showerror("Error", f"Error fetching student details: {e}")
        return None

button_click_count = 0
def Reset():
    entry_stu.delete(0, tk.END)
    if tree1.get_children():
        for item in tree1.get_children():
            tree1.delete(item)
    details.place_forget()
    tree.place_forget()
    label2.place_forget()
    tree1.place_forget()
    pay.place_forget()
    dis.place_forget()
    DD.place_forget()
    DD1.place_forget()
    DD2.place_forget()
    DD3.place_forget()
    amount.place_forget()
    entry_am.place_forget()
    amounts.place_forget()
    balam.place_forget()
    toggle_confirm.place_forget()
    imag.place_forget()
    hidden_cancel.place_forget()
    paid_button.place_forget()
    scan.place_forget()
    tan.place_forget()
    f4.pack_forget()
    payment.place_forget()
    global button_click_count
    button_click_count = 0
    
def enter():
    student_id = entry_stu.get()
    a=mysql.connector.connect(host="localhost",user="root",password="2003",database="university")
    b=entry_stu.get()
    m=a.cursor()
    m.execute("select * from students where StudentID = %s",(b,))
    rows = m.fetchall()
    a.close()
    for row in tree.get_children():
        tree.delete(row)
    if rows:
        for row in rows:
            tree.insert("", "end", values=row)
        data =[]
        if student_id == b:
            tree.place(x=20, y=280)
            details.place(x=10, y=230)
            label2.place(x=10, y=380)
            pay.place(x=320, y=600)
            tree1.place(x=70, y=430)

            global button_click_count
            if button_click_count == 0:
                tree1.place(x=70, y=430)
                data = [
                    ("SEMESTER 1", "25,000", "PAID"),
                    ("SEMESTER 2", "30,000", "PAID"),
                    ("SEMESTER 3", "22,000", "pending"),
                    ("SEMESTER 4", "28,000", "opening soon"),
                    ("SEMESTER 5", "45,000", "opening soon"),
                    ("SEMESTER 6", "20,000", "opening soon")
                ]
            for row in data:
                tree1.insert("", "end", values=row)
            button_click_count += 1

        else:
            details.place_forget()
            tree1.place_forget()
            label2.place_forget()
            tree.place_forget()
            pay.place_forget()
    else:
        details.place_forget()
        tree.place_forget()
        tree1.place_forget()
        label2.place_forget()
        pay.place_forget()

def pay():
    dis.place(x=20,y=10)
    DD.place(x=60,y=52)
    DD1.place(x=20,y=74)
    DD2.place(x=20,y=96)
    DD3.place(x=20,y=118)
    amount.place(x=20, y=165)
    entry_am.place(x=120, y=160)
    amounts.place(x=243, y=165)
    toggle_confirm.place(x=100, y=210)
    entry_am.delete(0, tk.END)
    
def show_image():
    photo = ImageTk.PhotoImage(Image.open('E:\\python\\python project\\QR.jpg'))
    imag.config(image=photo)
    imag.image = photo

def toggle_button():
    try:
        student = entry_am.get()
        students = int(student)
        imag.place(x=270, y=350)
        hidden_cancel.place(x=280, y=580)
        show_image()
        scan.place(x=280, y=300)
        balam.place(x=20, y=250)
        payment.place_forget()
        tan.place_forget()
        f4.pack_forget()
        paid_button.place(x=380, y=580)
        if students <= 22000:
            balance = 22000 - students
            balam.config(text=f"BALANCE AMOUNT: {balance}",fg='GREEN')
        else:
            balam.config(text="Your amount exceeds the limit",fg='red')
            imag.place_forget()
            hidden_cancel.place_forget()
            paid_button.place_forget()
            scan.place_forget()
            payment.place_forget()
            tan.place_forget()
            f4.pack_forget()
    
    except ValueError:
        balam.config(text="Please enter a valid amount! ",fg='red')
        imag.place_forget()
        hidden_cancel.place_forget()
        paid_button.place_forget()
        scan.place_forget()
        payment.place_forget()
        tan.place_forget()
        f4.pack_forget()
    
def cancel():
    entry_am.delete(0, tk.END)
    imag.place_forget()
    hidden_cancel.place_forget()
    paid_button.place_forget()
    scan.place_forget()
    balam.place_forget()
    
def paid():
    student_id = entry_stu.get()
    generate_receipt(student_id)
    entry_am.delete(0, tk.END)
    imag.place_forget()
    hidden_cancel.place_forget()
    scan.place_forget()
    tan.place(x=300, y=10)
    f4.pack(side ='bottom',fill='both',expand=False)
    paid_button.place_forget()
    payment.place(x=180,y=500)
''' amount.place_forget()
    amounts.place_forget()
    toggle_confirm.place_forget()
    balam.place_forget()
    entry_am.place_forget()'''

root = tk.Tk()
root.title("FEE TRACKER AND PAYMENT")
root.geometry('1525x830')

#------------header------------
f= tk.Frame(root,width=1520,bg="lightgreen",height=120,relief= tk.GROOVE)
f.pack(pady=10,expand= 'false')

logo_image = tk.PhotoImage(file=r'E:\python\python project\3.png')
logo_label = tk.Label(root, bg='lightgreen', image=logo_image)
logo_label.place(x=500, y=15)



label21=tk.Label(f, font=("Arial", 35, 'bold'), text="Hogwarts University",bg="lightgreen", fg="darkslateblue")
label21.place(x=600, y=10)

label22=tk.Label(f, font=("Arial", 12, 'bold'), text="0492, Hercules Street,Valencia,Somalia AZ143",bg="lightgreen", fg="darkorchid4")
label22.place(x=650, y=90)

label21=tk.Label(f, font=("Arial", 12), text="NAAC 'A' Grade, MHRD NIRF University Ranking 2022: 12",bg="lightgreen", fg="darkorchid4")
label21.place(x=620, y=70)


#------------students----------
f2 = tk.Frame(root,width=755,bg="lightblue",height=700, relief= tk.RIDGE)
f2.pack(side ='left',fill='both',padx=10,pady=10,expand=False)

label1=tk.Label(f2, font=("Arial", 20, 'bold'), text="FEE TRACKER AND PAYMENT",bg="white", fg="black")
label1.place(x=170, y=40)

label=tk.Label(f2, font=("Arial", 13, 'bold'), text="STUDENT ID: ", fg="black",bg="lightblue")
label.place(x=230, y=106)

entry_stu = tk.Entry(f2, font=("aria", 15, 'bold'), bd=6,width=12,bg="white")
entry_stu.place(x=360, y=100)

reset_button =tk.Button(f2, bd=1, fg="white", bg="black", font=("ariel", 13, 'bold'), width=8, text="Reset", command=Reset)
reset_button.place(x=270, y=150)

enter_button =tk.Button(f2, bd=1, fg="black", bg="lightgreen", font=("ariel", 13, 'bold'), width=8, text="Enter", command=enter)
enter_button.place(x=360, y=150)

#------------students_detail----------
details =tk.Label(f2, font=("Arial", 20, 'bold'), text="STUNDENT DETAILS", fg="black",bg="lightblue")

style = ttk.Style()
style.configure("Custom.Treeview", font=('Arial', 10),bd=10)
tree = ttk.Treeview(f2, columns=("Column1", "Column2", "Column3", "Column4","Column5", "Column6", "Column7", "Column8","Column9"),show="headings",height=1,style="Custom.Treeview")

tree.heading("Column1", text="StudentID")
tree.heading("Column2", text="FirstName")
tree.heading("Column3", text="LastName")
tree.heading("Column4", text="DateOfBirth")
tree.heading("Column5", text="Gender")
tree.heading("Column6", text="Major")
tree.heading("Column7", text="GPA")
tree.heading("Column8", text="EnrollmentYear")
tree.heading("Column9", text="Phone no.")

tree.column("Column1", width=80)
tree.column("Column2", width=80)
tree.column("Column3", width=80)
tree.column("Column4", width=80)
tree.column("Column5", width=50)
tree.column("Column6", width=130)
tree.column("Column7", width=40)
tree.column("Column8", width=90)
tree.column("Column9", width=80)

#---------------payment_Details-------------
label2=tk.Label(f2, font=("Arial", 20, 'bold'), text="PAYMENT DETAILS", fg="black",bg="lightblue")

style = ttk.Style()
style.configure("Custom1.Treeview", font=('Arial', 13),bd=10,command=enter)

tree1 = ttk.Treeview(f2, columns=("Column1", "Column2", "Column3"), show="headings", height=7,style="Custom1.Treeview")

tree1.heading("Column1", text="SEMESTERS")
tree1.heading("Column2", text="AMOUNT")
tree1.heading("Column3", text="STATUS")

tree1.column("Column1", width=200)
tree1.column("Column2", width=200)
tree1.column("Column3", width=200)

pay =tk.Button(f2, bd=1, fg="white", bg="green", font=("ariel", 13, 'bold'), width=8, text="pay", command=pay)

#---------------------------------------------------RIGHT_FRAME--------------------------------------
f3 =tk.Frame(root, width=755,bg="lightblue",height=700,relief= tk.RIDGE)
f3.pack(side ='right',fill='both',padx=10,pady=10,expand='false')

#------------disclaimer---------------
dis = tk.Label(f3, text="DISCLAIMER:", font=('Arial', 15), bg="#ffcc99")

DD = tk.Label(f3, text="Please be advised that the payment of fees should be executed with utmost care. In the event of errors or",font=('Arial', 10),bg="lightblue")

DD1 = tk.Label(f3, text="discrepancies, we reserve the right to refund the amount with applicable penalties. Kindly verify the payment details", font=('Arial', 10),bg="lightblue")

DD2 = tk.Label(f3, text="diligently,as double-checking the accuracy is your responsibility. We appreciate your understanding and cooperation", font=('Arial', 10),bg="lightblue")

DD3 = tk.Label(f3, text="in ensuring a smooth financial transaction process", font=('Arial', 10),bg="lightblue")

#------------amount calaculation---------------

amount=tk.Label(f3, font=("Arial", 15, 'bold'), text="AMOUNT: ", fg="black",bg="lightblue")

entry_am = tk.Entry(f3, font=("aria", 15, 'bold'), bd=6,width=12,bg="lightpink")

amounts=tk.Label(f3, font=("Arial", 15, 'bold'), text="/-", bg="black",fg="white")

toggle_confirm =tk.Button(f3, bd=1, fg="white", bg="darkviolet", font=("ariel", 13, 'bold'),width=8, text="CONFIRM", command=toggle_button)

balam=tk.Label(f3, font=("Arial", 15, 'bold'), text="BALANCE AMOUNT: ",bg="lightblue")

#-------------SCAN-----------------
scan=tk.Label(f3, font=("Arial", 20, 'bold'), text="SCAN TO PAY", bg='lightblue')

#-------------image---------
imag = tk.Label(f3, bg='lightblue')

#------------ok-------------
hidden_cancel =tk.Button(f3, bd=1, fg="white", bg="RED", font=("ariel", 13, 'bold'),width=8, text="CANCEL",command=cancel)

paid_button =tk.Button(f3, bd=1, fg="white", bg="GREEN", font=("ariel", 13, 'bold'),width=8, text="PAID", command=paid)

payment=tk.Label(f3, font=("Arial", 20, 'bold'), text="PAYMENT SUCCESSFULL", bg='lightblue',fg='darkgreen')

#-----------thanks---------
f4 = tk.Frame(f3,width=755,bg="green",height=50, relief= tk.RIDGE)

tan=tk.Label(f4, font=("bradley hand ITC", 15, 'bold'), text="THANK  YOU !!", bg="green",fg="white")

entry_am.bind('<Return>', lambda event=None: toggle_button())
entry_stu.bind('<Return>', lambda event=None: enter())

root.mainloop()
