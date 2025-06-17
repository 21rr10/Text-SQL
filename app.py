from dotenv import load_dotenv

load_dotenv()
import streamlit as st
import os
import sqlite3

import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def initialize_database(db_path):
    if not os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE STUDENT(NAME VARCHAR(25), CLASS VARCHAR(25), SECTION VARCHAR(25), MARKS INT);")
        cursor.execute("INSERT INTO STUDENT VALUES('Ritesh','Data Science','A',90);")
        cursor.execute("INSERT INTO STUDENT VALUES('Ashish','DEVOPS','A',100);")
        cursor.execute("INSERT INTO STUDENT VALUES('Rishit','Data Science','A',86);")
        cursor.execute("INSERT INTO STUDENT VALUES('Ayush','DEVOPS','A',50);")
        cursor.execute("INSERT INTO STUDENT VALUES('Ojha','DEVOPS','A',35);")
        conn.commit()
        conn.close()
DB_PATH = "./student.db"
initialize_database(DB_PATH)
def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-2.0-flash')
    response=model.generate_content([prompt[0],question])
    return response.text


def read_sql_query(sql,db=DB_PATH):
    conn=sqlite3.connect(db)
    cur=conn.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows

prompt=[
    """
You are an expert in converting English questions into SQL query!
The SQL database is named STUDENT and contains the following columns:NAME,CLASS,SECTION
,MARKS
Examples:
1. Question: How many entries of records are present?
SELECT COUNT(*) FROM STUDENT;
2. Question: Tell me all the students studying in Data Science class?
SELECT * FROM STUDENT WHERE CLASS = "Data Science";
Instructions:
Do not include the words "SQL" or "sql" or 'query'at the  beginning or end of the output.
Return only the query.
Keep the prompt clean and focused on accurate conversions.
"""
]

st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("App To Fetch SQL Data")


question = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

if submit:
    response = get_gemini_response(question, prompt)
    print(response)
    data = read_sql_query(response, DB_PATH)
    st.subheader("The Response is")
    for row in data:
        print(row)
        st.header(row)
