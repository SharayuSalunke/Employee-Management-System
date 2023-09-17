import mysql.connector
import re

#-------------Connecting to DB--------------------------------
mydb = mysql.connector.connect(host = "localhost", user = "root", password = "Annem@1234", database = "ems")#connecting to mysql Db
print(mydb)


#----------------------------Class----------------------------------
class employee: # defining class
    def disp_basic_info(self,i):
        # Displays data from "Employee_Basic_Details" table
        c = mydb.cursor(buffered=True)
        c.execute("select * from Employee_Basic_Details")
        for row in c:
            temp = row[0]
            if(temp == i):
                return(row)
                
    def disp_work_hist(self,i):
        # Displays data from "Working_History" table
        c = mydb.cursor(buffered=True)
        c.execute("select * from Working_History")
        for row in c:
            temp = row[1]
            if(temp == i):
                return row
            
    def disp_time_info(self,i):
        # Displays data from "Time_Information_Per_Week" table
        c = mydb.cursor(buffered=True)
        c.execute("select * from Time_Information_Per_Week")
        for row in c:
            temp = row[1]
            if(temp == i):
                return row
            
    def disp_salary_info(self,i):
        # Displays data from "Salary_Information" table
        c = mydb.cursor(buffered=True)
        c.execute("select * from Salary_Information")
        for row in c:
            temp = row[1]
            if(temp == i):
                return row
            
    def disp_contact_info(self,i):
        # Displays data from "Contact_Person_Information" table
        c = mydb.cursor(buffered=True)
        c.execute("select * from Contact_Person_Information")
        for row in c:
            temp = row[1]
            if(temp == i):
                return row
            
    def disp_holiday_info(self,i):
        # Displays data from "Holiday_Information" table
        c = mydb.cursor(buffered=True)
        c.execute("select * from Holiday_Information")
        for row in c:
            temp = row[1]
            if(temp == i):
                return row
            
    def dele(self,i):
        #We are deleteing information from child tables
        #first and lastly deleting dat of parent table,
        # As deleteing parent table raises error
        c = mydb.cursor(buffered=True)
        c.execute("delete from Working_History where employee_id = %s ",i)        
        mydb.commit()
        c = mydb.cursor(buffered=True)
        c.execute("delete from Time_Information_Per_Week where employee_id = %s ",i)        
        mydb.commit()
        c = mydb.cursor(buffered=True)
        c.execute("delete from Salary_Information where employee_id = %s ",i)        
        mydb.commit()
        c = mydb.cursor(buffered=True)
        c.execute("delete from Contact_Person_Information where employee_id = %s ",i)        
        mydb.commit()
        c = mydb.cursor(buffered=True)
        c.execute("delete from Holiday_Information where employee_id = %s ",i)        
        mydb.commit()
        c = mydb.cursor(buffered=True)
        c.execute("delete from Employee_Basic_Details where employee_id = %s ",i)        
        mydb.commit()
        print("Successfully deleted")

    def add(self,i):
        # adding new employee data to all tables in database
        print("Adding data in Employee_Basic_Details")
        emp_id = i
        first = input("Enter First Name: ")
        last = input("Enter last Name: ")
        birthdate = input("Enter birth date (yyyy-mm-dd): ")
        mob = input("Enter mobile no.: ")
        line = input("Enter landline no.: ")
        cty = input("Enter city: ")
        edu = input("Enter qualification: ")
        exp = input("Enter years of experience: ")
        doj = input("Enter date of joining:")
        dol = input("Enter date of leaving:")
        emp_typ = "Permanent"
        gen = input("Enter gender:")
        mrg_state = input("Enter marital status :")   
                

        c = mydb.cursor(buffered=True)
        newempdata = (emp_id, first, last, birthdate, mob, line, cty, edu, exp, doj, dol, emp_typ, gen, mrg_state)
        add = """insert into Employee_Basic_Details(employee_id,first_name, last_name, date_of_birth,mobile_number, landline_number,
        city, qualification, year_of_experience, date_of_joining, date_of_leaving, employee_type, gender, marital_status)
        values(%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        c.execute(add,newempdata)
        mydb.commit()

        print("Adding data in Working_History")
        c = mydb.cursor(buffered=True)
        c.execute("select sr_no from Working_History")
        for row in c:
            last_sr_no = row[0]
            
        new_sr_no = last_sr_no + 1
        new_employee_id = i
        new_previous_company_name = input("Enter previous company name: ")
        new_previous_date_of_joining = input("Enter previous date of joining: ")
        new_previous_date_of_leaving = input("Enter previous date of leaving: ")
        newworkdata = (new_sr_no, new_employee_id, new_previous_company_name, new_previous_date_of_joining, new_previous_date_of_leaving  )
        add = """insert into Working_History(sr_no, employee_id, previous_company_name, previous_date_of_joining, previous_date_of_leaving)
        values(%s,%s, %s, %s, %s)"""
        c.execute(add,newworkdata)
        mydb.commit()

        print("Adding data in  Time_Information_Per_Week")
        c = mydb.cursor(buffered=True)
        c.execute("select t_sr_no from Time_Information_Per_Week")
        for row in c:
            last_t_sr_no = row[0]
            # storing last sr number to auto calculate next sr no.
            
        new_t_sr_no = last_t_sr_no + 1
        new_employee_id = i
        new_Worked_hours = input("Enter worked hours: ")
        new_Off_hours = input("Enter off/idle hours: ")
        new_days_off = input("Enter no. off days: ")
        new_overtime = input("Enter overtime in hours: ")
        newtimedata = (new_t_sr_no, new_employee_id, new_Worked_hours,new_Off_hours,new_days_off,new_overtime )
        add = """insert into Time_Information_Per_Week(t_sr_no, employee_id, Worked_hours,Off_hours, days_off, overtime)
        values(%s,%s, %s, %s, %s,%s)"""
        c.execute(add,newtimedata)
        mydb.commit()
    

        print("Adding data in  Salary_Information")
        c = mydb.cursor(buffered=True)
        c.execute("select s_sr_no from Salary_Information")
        for row in c:
            last_s_sr_no = row[0]
            
        new_s_sr_no = last_s_sr_no + 1
        new_employee_id = i
        new_annual_salary = input("Enter annual salary: ")
        int_salary = int(new_annual_salary)
        #Calculating annual tax as per annual salary
        if(250000 < int_salary < 500000 ):
            new_annual_tax = str(int_salary * 0.05)
        if(500000 < int_salary < 1000000 ):
            new_annual_tax = str(int_salary * 0.2)
        if(1000000 < int_salary ):
            new_annual_tax = str(int_salary * 0.3)            
        #Calculating monthly PF deductions as per rules
        new_monthly_PF_deductions = str((int_salary/12)*0.12 + (int_salary/12)*0.0367)
        new_medical_policy_premium_deduction = 5000 #fixed
        newsalarydata = (new_s_sr_no,new_employee_id,new_annual_salary, new_annual_tax,new_monthly_PF_deductions,new_medical_policy_premium_deduction)
        add = """insert into Salary_Information(s_sr_no, employee_id, annual_salary, annual_tax, monthly_PF_deductions, medical_policy_premium_deduction)
        values(%s,%s, %s, %s, %s,%s)"""
        c.execute(add,newsalarydata)
        mydb.commit()
    
        print("Adding data in  Contact_Person_Information")
        c = mydb.cursor(buffered=True)
        c.execute("select c_sr_no from Contact_Person_Information")
        for row in c:
            last_c_sr_no = row[0]
            
        new_c_sr_no = last_c_sr_no + 1
        new_employee_id = i
        new_c_first_name = input("Enter first name: ")
        new_c_last_name = input("Enter last name: ")
        new_relationship = input("Enter relationship with person: ")
        new_c_mobile_number = input("Enter mobile number: ")
        new_c_landline_number = input("Enter landline number: ")
        new_c_city = input("Enter city of recident of contact person: ")
        newcondata = (new_c_sr_no, new_employee_id,new_c_first_name,new_c_last_name, new_relationship,new_c_mobile_number, new_c_landline_number, new_c_city)
        add = """insert into Contact_Person_Information(c_sr_no,employee_id, c_first_name, c_last_name, relationship, c_mobile_number, c_landline_number, c_city )
        values(%s,%s, %s, %s, %s,%s,%s,%s)"""
        c.execute(add,newcondata)
        mydb.commit()
    

        print("Adding data in  Holiday_Information")
        c = mydb.cursor(buffered=True)
        c.execute("select h_sr_no from Holiday_Information")
        for row in c:
            last_h_sr_no = row[0]
            
        new_h_sr_no = last_h_sr_no + 1
        new_employee_id = i
        new_previlage_leave_balance = input("privlage leave balance : ")
        new_sick_leave_balance = input("Enter sick leave balance: ")
        new_emergency_leave_balance = input("Enter emergency leave balance: ")
        newholydata = (new_h_sr_no,new_employee_id, new_previlage_leave_balance,new_sick_leave_balance,new_emergency_leave_balance  )
        add = """insert into Holiday_Information(h_sr_no, employee_id, previlage_leave_balance, sick_leave_balance, emergency_leave_balance )
        values(%s,%s, %s, %s, %s)"""
        c.execute(add,newholydata)
        mydb.commit()

    def update(self, i):
        
        c = mydb.cursor(buffered=True)
        c.execute(i)
        mydb.commit()
        print("Data update successful")

    def exit(self):
        return

#---------------------------Functions--------------------------------------            

def display():
    
    emp_obj = employee()
    #creating object of employee class
    eid_list = [] #creating list to store employee id
    c = mydb.cursor()
    c.execute("select employee_id from Employee_Basic_Details")
    for row in c:
        eid_list.append(row[0])

    search = input("Enter employee ID to search: ")
    if search not in eid_list:
        print("Employee not found")

    for item in eid_list:
        if (item == search):
            print(emp_obj.disp_basic_info(item))#button
            print()
            print(emp_obj.disp_work_hist(item))#button
            print()
            print(emp_obj.disp_time_info(item))#button
            print()
            print(emp_obj.disp_salary_info(item))#button
            print()
            print(emp_obj.disp_contact_info(item))#button
            print()
            print(emp_obj.disp_holiday_info(item))#button

def delete():
    emp_obj = employee()#creating object of employee class

        
    search = input("Enter employee  ID to delete data: ")
    c = mydb.cursor()
    c.execute("select employee_id from Employee_Basic_Details")
    for row in c:
        if search in row:
            eid = row
    emp_obj.dele(eid)
    
    
            
def create():
    #function to Generating next employee ID
    def next_eid():
        c = mydb.cursor()
        c.execute("select employee_id from Employee_Basic_Details")
        for row in c:
            last_employee_id = row[0]
            if(last_employee_id == ""):
                test_str = "E100"
            else:
                test_str = last_employee_id
        res = re.sub(r'[0-9]+$',
                lambda x: f"{str(int(x.group())+1).zfill(len(x.group()))}",
                test_str)
        return str(res)
    emp_obj = employee()
    #creating object of employee class
    empl_id = next_eid()
    emp_obj.add(empl_id)
    print("New employee added successfully")

def update():
    emp_obj = employee()
    #creating object of employee class
    eid_list = []
    c = mydb.cursor()
    c.execute("select employee_id from Employee_Basic_Details")
    for row in c:
        eid_list.append(row[0])

    search = input("Enter employee  ID to update data: ")
    if search not in eid_list:
        print("Employee not found")

    for item in eid_list:
        if (item == search):
            eid = item
            table_name = input("""Enter table name to update:
                  Employee_Basic_Details
                  Working_History
                  Time_Information_Per_Week
                  Salary_Information
                  Contact_Person_Information
                  Holiday_Information
                  """)
            if(table_name == "Employee_Basic_Details"):
                column_name = input("""Select field name to update:
                                       first_name, last_name, date_of_birth,mobile_number, landline_number,
                                       city, qualification, year_of_experience, date_of_joining, date_of_leaving,
                                       gender, marital_status
                                       """)
                new_value = input("Enter new value: ")
            if(table_name == "Working_History"):
                column_name = input("""Select field name to update:
                                       previous_company_name, previous_date_of_joining, previous_date_of_leaving
                                       """)
                new_value = input("Enter new value: ")
            if(table_name == "Time_Information_Per_Week"):
                column_name = input("""Select field name to update:
                                       Worked_hours,Off_hours, days_off, overtime
                                       """)
                new_value = input("Enter new value: ")
            if(table_name == "Salary_Information"):
                column_name = input("""Select field name to update:annual_salary""")
                new_value = input("Enter new value: ")
                
            if(table_name == "Contact_Person_Information"):
                column_name = input("""Select field name to update:
                                       c_first_name, c_last_name, relationship, c_mobile_number, c_landline_number, c_city
                                       """)
                new_value = input("Enter new value: ")
            if(table_name == "Holiday_Information"):
                column_name = input("""Select field name to update:
                                       previlage_leave_balance, sick_leave_balance, emergency_leave_balance
                                       """)
                new_value = input("Enter new value: ")
            command = "update {0} set {1} ='{2}'  where employee_id = '{3}' ".format(table_name, column_name, new_value, eid )
            emp_obj.update(command)
            if(column_name == "annual_salary"):
                i_sal = int(new_value)
                
                if(250000 < i_sal <= 500000 ):
                    update_annual_tax = str(i_sal * 0.05)
                if(500000 < i_sal <= 1000000 ):
                    update_annual_tax = str(i_sal * 0.2)
                if(1000000 < i_sal ):
                    update_annual_tax = str(i_sal * 0.3)            
        
                update_monthly_PF_deductions = str((i_sal/12)*0.12 + (i_sal/12)*0.0367)
                cmd = "update {0} set {1} ='{2}', {3}= '{4}' where employee_id = '{5}' ".format(table_name, 'annual_tax',  update_annual_tax,'monthly_PF_deductions', update_monthly_PF_deductions, eid )
                emp_obj.update(cmd)
        
            
def exitapp():
    emp_obj = employee()#creating object of employee class
    emp_obj.exit()
      
#-----------------------Main-------------------------------
print("""Select action to perform from 1 to 5:
                1. Search
                2. Create
                3. Update
                4. Delete
                5. Exit""")
action = int(input("Enter action: "))
if(action == 1):
    display()
if(action == 2):
    create()
if(action == 3):
    update()
if(action == 4):
    delete()
if(action == 5):
    exitapp()

 

