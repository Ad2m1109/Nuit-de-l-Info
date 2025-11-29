from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai



# Load environment variables
load_dotenv()

# Configure the Generative AI model
genai.configure(api_key="")
model = genai.GenerativeModel("gemini-2.5-flash") 
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

# Initialize the Streamlit app
st.set_page_config(page_title="Gemini Application")

st.header("Ask with Gemini or Generate Images with DALL·E")

# Initialize session state for chat history if it doesn't exist
if 'history' not in st.session_state:
    st.session_state['history'] = []

# Sidebar with expandable history items
st.sidebar.header("Chat History")

def delete_history(index):
    del st.session_state.history[index]

# Display history in the sidebar with expanders
for i, entry in enumerate(st.session_state.history):
    with st.sidebar.expander(f"Q{i+1}"):
        st.write(f"**Input:** {entry['input']}")
        st.write(f"**Response:** {entry['response']}")
        if st.button(f"Delete", key=f"delete_{i}"):
            delete_history(i)
            # Force rerun by setting query parameters
            st.query_params.update(deleted_index=i)

# Input and submit button for new questions
input = st.text_input("", key="input")
submit = st.button("Submit")



if submit and input:
    response = get_gemini_response(input)
    response_text = ''.join([chunk.text for chunk in response])
    st.session_state.history.append({"input": input, "response": response_text})
    st.write(response_text)
    st.query_params.update(new_question=input)

items = ["AI ", "ML "]
selected_item = st.selectbox("Select an item:", items)
st.write(f"You selected: {selected_item}")
s2 = st.button("Ask AI")
if s2:
    response = get_gemini_response(selected_item)
    response_text = ''.join([chunk.text for chunk in response])
    st.session_state.history.append({"input": selected_item, "response": response_text})
    st.write(response_text)
    st.query_params.update(new_question=selected_item)


# streamlit run app.py