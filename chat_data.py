import streamlit as st
import openai
import pyodbc
from dotenv import load_dotenv

# Set up OpenAI API
load_dotenv()

# Set up SQL Server connection
server = 'tcp:uatbriskserver.database.windows.net,1433'
database = 'BriskUATEducationSystem'
username = 'uatbriskserver'
password = 'UatBrisk@2023'
conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

conversation_history = []

# Streamlit app
def main():
    st.title("ChatGPT with SQL Data")

    user_input = st.text_input("You:", value="", key="user_input")

    if st.button("Send"):

        conversation_history.append(f"You: {user_input}")

        # Fetch relevant data from SQL Server based on user input
        connection = pyodbc.connect(conn_str)
        cursor = connection.cursor()
        query = f"SELECT top 10 QuestionAnswer, QuestionDescription, QuestionMark FROM [dbo].[MasterQuestions] WHERE column_name LIKE '%{user_input}%'"
        cursor.execute(query)
        result = cursor.fetchall()

        # Generate response using ChatGPT
        chatgpt_response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=user_input,
            max_tokens=50
        ).choices[0].text.strip()

        # Display SQL data and ChatGPT's response
        st.write("SQL Data:")
        for row in result:
            st.write(row)
        
        conversation_history.append(f"ChatGPT: {chatgpt_response}")

        # Display conversation history, SQL data, and ChatGPT's response
        st.write("Conversation:")
        for message in conversation_history:
            st.write(message)


        st.write("ChatGPT's Response:", chatgpt_response)

if __name__ == "__main__":
    main()
