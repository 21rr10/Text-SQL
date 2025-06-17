from dotenv import load_dotenv

load_dotenv()
import streamlit as st
import os
import sqlite3

import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-2.0-flash')
    response=model.generate_content([prompt[0],question])
    return response.text


def read_sql_query(sql,db):
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
    data = read_sql_query(response, "student.db")
    st.subheader("The Response is")
    for row in data:
        print(row)
        st.header(row)
