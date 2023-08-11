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

# Initialize conversation history
conversation_history = []

# Streamlit app
def main():
    st.title("Dynamic ChatGPT with SQL Data")

    global conversation_history
    user_input = st.text_input("You:", value="", key="user_input")

    if st.button("Send"):
        conversation_history.append(f"You: {user_input}")

        # Translate user input to SQL query using OpenAI
        sql_query = translate_to_sql_query(user_input)

        if sql_query:
            # Fetch data from SQL Server based on translated SQL query
            connection = pyodbc.connect(conn_str)
            cursor = connection.cursor()
            cursor.execute(sql_query)
            result = cursor.fetchall()

            # Generate response using ChatGPT
            chatgpt_response = openai.Completion.create(
                engine="davinci-codex",
                prompt="\n".join(conversation_history),
                max_tokens=50
            ).choices[0].text.strip()

            conversation_history.append(f"ChatGPT: {chatgpt_response}")

            # Display conversation history, SQL data, and ChatGPT's response
            st.write("Conversation:")
            for message in conversation_history:
                st.write(message)

            st.write("SQL Data:")
            for row in result:
                st.write(row)
        else:
            st.write("Sorry, I couldn't understand your request.")

def translate_to_sql_query(user_input):
    # Use OpenAI to translate user's English input into SQL-like query
    translated_query = openai.Completion.create(
        engine="davinci",
        prompt=user_input,
        max_tokens=50
    ).choices[0].text.strip()

    # Construct a basic SQL query based on the translated query
    return "SELECT * FROM MasterQuestions WHERE {}".format(translated_query)

if __name__ == "__main__":
    main()
