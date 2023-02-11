import pandas as pd
import psycopg2
import streamlit as st
from configparser import ConfigParser
import decimal

@st.cache
def get_config(filename="database.ini", section="postgresql"):
    parser = ConfigParser()
    parser.read(filename)
    return {k: v for k, v in parser.items(section)}


def query_db(sql: str):
    # print(f"Running query_db(): {sql}")
    db_info = get_config()
    # Connect to an existing database
    conn = psycopg2.connect(**db_info)
    # Open a cursor to perform database operations
    cur = conn.cursor()
    # Execute a command: this creates a new table
    cur.execute(sql)
    # Obtain data
    data = cur.fetchall()
    column_names = [desc[0] for desc in cur.description]
    # Make the changes to the database persistent
    conn.commit()
    # Close communication with the database
    cur.close()
    conn.close()
    df = pd.DataFrame(data=data, columns=column_names)

    return df

def insert_db(sql: str):
    # print(f"Running query_db(): {sql}")
    db_info = get_config()
    # Connect to an existing database
    conn = psycopg2.connect(**db_info)
    # Open a cursor to perform database operations
    cur = conn.cursor()
    # Execute a command: this creates a new table
    cur.execute(sql)
    # Make the changes to the database persistent
    conn.commit()
    # Close communication with the database
    cur.close()
    conn.close()

st.title("University Management System")

sidemenu = [ "Admin", "Professor", "Student", "University"]
user = st.sidebar.selectbox('User Menu', sidemenu)

if user == "Admin":
    menu = [ "Profile", "Professor Payrolls", "Accessibilty Requests","Student Payment Activity"]
    choice = st.selectbox( "Menu", menu )

    if choice == "Profile":        
        st.subheader("Admin profile")

        with st.form('profile_form'):
            aId = st.text_input('Administrator ID')
            firstName = st.text_input('First Name')
            lastName = st.text_input('Last Name')
            dob = st.date_input('Date of Birth')
            address = st.text_input('Address')
            ph = st.text_input('10-digit Mobile Number')
            email = st.text_input('Email') 
            university = st.selectbox('What university do you belong to?', ('New York University', 'Harvard University', 'Columbia University', 'Yale University') )       
            
            profileSubmit = st.form_submit_button('Submit') 

            if profileSubmit:
                try:
                    qry = f"""INSERT into Admins_employ( aid, afirst, alast, aphno, aemail, address, dob, uname ) values ( {aId}, '{firstName}', '{lastName}', '{ph}', '{email}', '{address}', '{dob}', '{university}' )"""            
                    insert_db(qry)
                    st.info('Profile Updated')   
                except Exception as E:
                    st.write("Sorry! Something went wrong with your query, please try again.")
                    st.write(E)

    if choice == "Professor Payrolls":
        st.subheader('Professor Payrolls')
        try:
            sql_pids = f"select p.pid from Professors p"
            pids = query_db(sql_pids)["pid"].tolist()
            choice = st.selectbox("Select the Professor ID",pids)
        except Exception as E:
            st.write("Sorry! Something went wrong with your query, please try again.")
            st.write(E)

        with st.form('emp_payroll_form'):
                
                salary = st.number_input("Enter Payment")
                adminid = st.text_input("Enter Admin ID")
                date = st.date_input("Enter Date")

                paySubmit = st.form_submit_button('Pay')

                if paySubmit:
                    try:
                        qry = f"""INSERT into Pay( amount, dates, pid, aid ) values ( {salary}, '{date}', {choice},{adminid} )"""
                        insert_db( qry )
                        st.info('Pay Updated!')
                    except Exception as E:
                        st.write("Sorry! Something went wrong with your query, please try again.")
                        st.write(E)

    if choice == "Accessibilty Requests":
        st.write('All Requests')
        try:        
            sql_req = f"SELECT * FROM Requests;"
            req_info = query_db(sql_req)
            st.dataframe(req_info)
        except Exception as E:
            st.write("Sorry! Something went wrong with your query, please try again.")
            st.write(E)


        col1, col2 = st.columns(2)
        with col1:
            try:
                sql_req = f"SELECT * FROM Requests where status='pending';"
                req = query_db(sql_req)["rid"].tolist()
                choice1 = st.selectbox("Select a pending request to assign",req)
            except Exception as E:
                st.write("Sorry! Something went wrong with your query, please try again.")
                st.write(E)


        with col2:     
            try:       
                choice2 = st.text_input("Enter Professor ID")
            except Exception as E:
                st.write("Sorry! Something went wrong with your query, please try again.")
                st.write(E)

        with st.form('Requests'):
            taskSubmit = st.form_submit_button('Send') 
            if taskSubmit:
                try:
                    qry = f"""INSERT into Send_To( pid,rid ) values ( {choice2},{choice1})"""      
                    insert_db(qry)
                    st.info('Approval sent!')      
                except Exception as E:
                    st.write("Sorry! Something went wrong with your query, please try again.")
                    st.write(E) 

                try:
                    qry= f"""UPDATE Requests SET status = 'Approved' WHERE rid = {choice1}"""     
                    insert_db(qry); 
                    st.info("Status changed!")
                except Exception as E:
                    st.write("Sorry! Something went wrong with your query, please try again.")
                    st.write(E)


    if choice== "Student Payment Activity":
        st.write("All Payments")
        try:
            sql_pay = f"SELECT * FROM Payments;"
            pay_info = query_db(sql_pay)
            st.dataframe(pay_info)
        except Exception as E:
            st.write("Sorry! Something went wrong with your query, please try again.")
            st.write(E)     

        try:
            st.write("Student wise Payments")
            sql_stutermfee = f"SELECT sid,term, sum(amount) from Payments GROUP BY(sid,term)"
            stutermfee = query_db(sql_stutermfee)
            st.dataframe(stutermfee)
        except Exception as E:
            st.write("Sorry! Something went wrong with your query, please try again.")
            st.write(E)        


                
if user == "Professor":
    menu = [ "Professor Enrollment", "Professor Information", "Paycheck", "Accesibility Requests"]
    choice = st.selectbox( "Menu", menu )

    if choice == "Professor Enrollment":        
        st.subheader("New Professor Enrollment")

        with st.form('profile_form'):
            professorId = st.text_input('Professor ID')
            firstName = st.text_input('First Name')
            lastName = st.text_input('Last Name')
            dob = st.date_input('Date of Birth')
            address = st.text_input('Address')
            ph = st.text_input('10-digit Mobile Number')
            email = st.text_input('Email')  
            dept = st.selectbox('What department do you belong to?', ('CS', 'EC', 'CE', 'MOT') )  


            
            proSubmit = st.form_submit_button('Submit') 

            if proSubmit:
                qry1 = f"""INSERT into Professors( pid, pfirst, plast, phno, email, address, dob, dept) values ( {professorId}, '{firstName}', '{lastName}', '{ph}', '{email}', '{address}', '{dob}', '{dept}' )"""     
                try:
                    insert_db(qry1)
                    st.info('Profile Updated')  
                except Exception as E:
                    st.write("Sorry! Something went wrong with your query, please try again.")
                    st.write(E)
        
    if choice == "Paycheck":
        with st.form('emp_paycheck'):
            professorId = st.text_input('Professor ID')
            paySubmit = st.form_submit_button('Submit')

        if paySubmit:
            try:
                #joining the tables pay and admins
                sql_salary = f"SELECT p.amount as Amount, p.dates as Date, a.afirst as Paid_by, a.aemail as Admin_mail FROM Pay p, Admins_employ a WHERE p.aid=a.aid AND p.pid={professorId};"
                salary_info = query_db(sql_salary)
                st.subheader("Your Paycheck")
                st.dataframe(salary_info)
            except Exception as E:
                    st.write("Sorry! Something went wrong with your query, please try again.")
                    st.write(E)

    if choice== "Professor Information":
        st.subheader("Professor Information")
        with st.form('Professor_info'):
            professorId = st.text_input('Professor ID')
            infoSubmit = st.form_submit_button('Submit')
        
        if infoSubmit:
            try:
                st.write("Classes")
                sql_class = f"SELECT p.pfirst as Name, c.cid as Course_Id, c.cname as Course, c.day as Day, c.time as Class_Time  FROM Taught t, Professors p, Classes_located c WHERE p.pid = {professorId} and p.pid = t.pid and t.cid = c.cid "
                class_info = query_db(sql_class)
                #st.write(str(class_info['class_time']))
                st.write(class_info.astype('string'))
            except Exception as E:
                st.write("Sorry! Something went wrong with your query, please try again.")
                st.write(E)
            

            try:
                st.write("School")
                sql_school = f"SELECT p.pfirst as Name, e.sname as School FROM Professors p, Employs e  WHERE p.pid = {professorId} and p.pid = e.pid"
                school_info = query_db(sql_school)
                st.dataframe(school_info)
            except Exception as E:
                st.write("Sorry! Something went wrong with your query, please try again.")
                st.write(E)
    
    if choice ==  "Accesibility Requests":
        with st.form('emp_tasks'):
            professorId = st.text_input('Professor ID')
            taskSubmit = st.form_submit_button('Submit')

        if taskSubmit:
            #joining the tables requests and assigned_to 
            try:
                sql_tasks_prev = f"SELECT s.rid as Request_ID, st.sfirst as Name, r.description as Description FROM Send_To s, Requests r, Students st WHERE s.rid = r.rid AND s.pid={professorId} AND r.status='Approved' AND r.sid = st.sid;"
                prev_tasks_info = query_db(sql_tasks_prev)
                st.subheader("Approved Requests")
                st.dataframe(prev_tasks_info)
            except Exception as E:
                    st.write("Sorry! Something went wrong with your query, please try again.")
                    st.write(E)
                    
                
if user == "Student":
    menu = [ "Profile", "Student Accesibility Request", "Requests Status Update", "Fees Payment", "Classes", "Dorm Information"]
    choice = st.selectbox( "Menu", menu )

    if choice == "Profile":        
        st.subheader("Student Profile")

        with st.form('profile_form'):
            sId = st.text_input('Student ID')
            firstName = st.text_input('First Name')
            lastName = st.text_input('Last Name')
            dob = st.date_input('Date of Birth')
            address = st.text_input('Address')
            ph = st.text_input('10-digit Mobile Number')
            email = st.text_input('Email')            
            dept = st.selectbox('What department are you enrolled in?', ('CS', 'CE', 'MOT', 'Cybersecurity') )
            pType = st.selectbox('What is your program type?',('MS','BS')) 

            proSubmit = st.form_submit_button('Submit') 

            if proSubmit:
                qry = f"""INSERT into Students( sid, sfirst, slast, phno, email, address, dob, dept, program_type ) values ( {sId}, '{firstName}', '{lastName}', '{ph}', '{email}', '{address}', '{dob}', '{dept}', '{pType}' )"""            
                try:
                    insert_db(qry)
                    st.info('Profile Updated') 
                except Exception as E:
                    st.write("Sorry! Something went wrong with your query, please try again.")
                    st.write(E)


    if choice == "Student Accesibility Request":
        st.subheader("Student Accesibility Form")
        
        with st.form('requests_form'):
            sId = st.text_input('Student ID')
            category = st.selectbox('Choose category', ('Physical Health','Mental Health'))
            desc = st.text_input('Description')
            professorId = st.text_input("Professor ID")

            reqSubmit = st.form_submit_button('Submit')

            if reqSubmit:
                qry = f"""INSERT into Requests(category, description, sid, prof_id, status ) values ( '{category}', '{desc}', {sId}, {professorId}, 'pending' )"""
                try:
                    insert_db( qry )
                    st.info('Request Registered')
                except Exception as E:
                    st.write("Sorry! Something went wrong with your query, please try again.")
                    st.write(E)

    if choice == "Requests Status Update":
        st.subheader("Student Requests Status Update")

        sql_sid = f"SELECT sid from Students;"
        try:
                sid_info = query_db( sql_sid )["sid"].tolist()
                sid = st.selectbox("Student ID", sid_info)
                sql_req_sid = f"SELECT * FROM Requests WHERE sid = {sid};"
                req_sid_info = query_db(sql_req_sid)
                st.dataframe(req_sid_info)
        except Exception as E:
                st.write("Sorry! Something went wrong with your query, please try again.")
                st.write(E)  


    if choice == "Fees Payment":
        st.subheader("Student Fees Payments")

        with st.form('payments_form'):
            sId = st.text_input('Student ID')
            term = st.selectbox('Choose term', ('Spring', 'Summer', 'Fall'))
            amount = st.number_input('Enter Amount')

            paySubmit = st.form_submit_button('Submit')

            if paySubmit:
                qry = f"""INSERT into Payments( sid, amount, term ) values ( {sId}, {amount}, '{term}' )"""
                try:
                    insert_db( qry )
                    st.info('Payment Done')
                except Exception as E:
                    st.write("Sorry! Something went wrong with your query, please try again.")
                    st.write(E)  
    
    if choice == "Classes":
        st.subheader("Classes Enrolled")

        with st.form("class_form"):
            sId = st.text_input('Student ID')

            classSubmit = st.form_submit_button('Submit')

            if classSubmit:
                try:
                    class_req = f"SELECT c.cid as Course_Id, c.cname as Course_Name, c.day as Day, c.time as Time, c.bname as Building_Name FROM Enroll e, Classes_located c WHERE e.cid = c.cid and e.sid = {sId} ;"
                    class_inform = query_db(class_req)
                    st.write(class_inform.astype('string'))
                except Exception as E:
                    st.write("Sorry! Something went wrong with your query, please try again.")
                    st.write(E) 


    if choice == "Dorm Information":
        st.subheader("Dorm Information")

        with st.form("dorm_form"):
            sId = st.text_input('Student ID')

            dormSubmit = st.form_submit_button('Submit')

            if dormSubmit:
                st.write('Dorm:')
                try:        
                    sql_req = f"SELECT d.name as Dorm, d.address as Address, d.pincode as Pin_code, d.warden as Warden FROM Dorms d, Live l, Students s WHERE s.sid = {sId} and s.sid = l.sid and l.dname = d.name;"
                    req_info = query_db(sql_req)
                    st.dataframe(req_info)
                except Exception as E:
                    st.write("Sorry! Something went wrong with your query, please try again.")
                    st.write(E)

                # st.write('Room:')
                # try:        
                #     sql_req = f"SELECT r.rno as Room_No, r.floor as Floor FROM Dorms d, Live l, Students s, Rooms_have r WHERE s.sid = {sId} and s.sid = l.sid and l.dname = d.name and d.name = r.dname;"
                #     req_info = query_db(sql_req)
                #     st.dataframe(req_info)
                # except Exception as E:
                #     st.write("Sorry! Something went wrong with your query, please try again.")
                #     st.write(E)

####Think about printing roomate names

if user == "University":
    menu = [ "University Information", "Buildings Information"]
    choice = st.selectbox( "Menu", menu )

    if choice == "University Information":
        st.subheader("University Information")

        with st.form("uni_form"):
            uni_name = st.selectbox('University',('New York University','Harvard University', 'Yale University')) 

            uniSubmit = st.form_submit_button('Submit')

            if uniSubmit:
                st.write('Schools:')
                try:        
                    sql_req = f"SELECT s.name as School_Name, s.address as Address, s.dean as Dean FROM Universities u, Schools_partof s WHERE s.uname = u.name and u.name = '{uni_name}';"
                    req_info = query_db(sql_req)
                    st.dataframe(req_info)
                except Exception as E:
                    st.write("Sorry! Something went wrong with your query, please try again.")
                    st.write(E)

                st.write('Buidlings:')
                try:        
                    sql_req = f"SELECT s.name as School_Name,b.name as Building_Name, b.address as Building_Address, b.no_of_rooms as No_of_Rooms FROM Schools_partof s, Universities u, Buildings_belong_to b  WHERE u.name = '{uni_name}' and u.name = s.uname and s.name = b.schoolname;"
                    req_info = query_db(sql_req)
                    st.dataframe(req_info)
                except Exception as E:
                    st.write("Sorry! Something went wrong with your query, please try again.")
                    st.write(E)

    if choice == "Buildings Information":
        st.subheader("Building Information")

        with st.form('buildings_form'):
            uni_name = st.selectbox('University',('New York University','Harvard University', 'Yale University')) 
            school_name = st.text_input('School Name')
            building_name = st.text_input('Building Name')
            start_time = st.time_input('Select start time')
            end_time = st.time_input('Select end time')

            buildingSubmit = st.form_submit_button('Submit')

            if buildingSubmit:
                st.write('Classes_Information')
                try:        
                    sql_req = f"SELECT b.name as Building_Name, c.cid as Course_ID, c.cname as Course_Name, c.time as Time FROM  Classes_located c, Schools_partof s, Universities u, Buildings_belong_to b  WHERE u.name = '{uni_name}' and s.name = '{school_name}' and b.name = '{building_name}' and u.name = s.uname and s.name = b.schoolname and b.name = c.bname and c.time >= '{start_time}' and c.time <= '{end_time}' ;"
                    req_info = query_db(sql_req)
                    st.write(req_info.astype('string'))
                except Exception as E:
                    st.write("Sorry! Something went wrong with your query, please try again.")
                    st.write(E)











                
                

                

                    
                    
                  


            


 

    