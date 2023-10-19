import streamlit as st
import mysql.connector
import pandas as pd

mydb= mysql.connector.connect(

    host = "localhost",
    user = "root",
    password = '8046',
    database = "crud_db")

cursor=mydb.cursor()
def crud():
    st.title("MySQL Database :blue[CRUD] Operations :sunglasses:",)
    st.subheader('''This Project is basically create, read, update and delete data from database.
            ''')
    st.sidebar.header("Hello....")
    option=st.sidebar.selectbox("Choose CRUD Operations",["Create","Read","Update","Delete"]
                        ,index=None)
    if option == "Create":
        st.subheader("Create a Table")
        first_name=st.text_input("Enter Your First Name")
        last_name=st.text_input("Enter Your Last Name")
        roll=st.text_input("Enter Your Roll Number")
        if first_name and last_name and roll:
            if st.button("Create"):
                query ='Insert into student_info(first_name,last_name,rollid) values(%s,%s,%s)'
                value = (first_name,last_name,roll)
                cursor.execute(query,value)
                mydb.commit()
                st.success('Record Created')
                st.balloons()
        else: st.warning("Fill all the above details")


    elif option == "Read":
        st.subheader("Read Table Data")
        if st.selectbox("Select Your Table",["student_info"],index=None):
            if st.button("Show"):
                query_select= "Select * from student_info"
                cursor.execute(query_select)
                output = cursor.fetchall()
                column_name = [desc[0] for desc in cursor.description]
                df= pd.DataFrame(output,columns=column_name,)
                st.dataframe(df,width=680,hide_index=True,)


    elif option == "Update":
        st.subheader("Update your Table")
        if st.selectbox("Select Your Table",["student_info"],index=None):
            first_name = st.text_input("Edit Your First Name")
            last_name = st.text_input("Edit Your Last Name")
            roll = st.text_input("Edit Your Roll Number")
            cursor.execute("select id from student_info")
            id_value=[]
            for row in cursor.fetchall():
                id_value.append(row[0])
            selected_value=st.selectbox("Choose Id",id_value)
            if st.button("Update"):
                query="Update student_info set first_name=%s,last_name=%s,rollid=%s where id=%s"
                value = first_name, last_name, roll, selected_value
                cursor.execute(query,value)
                mydb.commit()
                st.success("Table Updated")

    
    elif option == "Delete":
        st.subheader("Delete a Table")
        if st.selectbox("Select Your Table",["student_info"],index=None):
            query= "Select * from student_info"
            cursor.execute(query)
            result= cursor.fetchall()
            column_name= [desc[0] for desc in cursor.description]
            df = pd.DataFrame(result,columns=column_name)
            st.dataframe(df,hide_index=True)
        
            query1= "Select id from student_info"
            cursor.execute(query1)
            output=[row[0] for row in cursor.fetchall()]
            sel_value=st.selectbox("Choose Your ID",output)
            if st.button("Delete"):
                query3= "Delete from student_info where id = %s"
                cursor.execute(query3,(sel_value,))
                mydb.commit()
                st.success("Selected Row deleted")
        




if __name__ == '__main__':
    crud()

