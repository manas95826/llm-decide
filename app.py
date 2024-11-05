import streamlit as st
from openai import OpenAI
import anthropic

anthropic_api_key = st.text_input("Enter your Anthropic API key:", type="password")
openai_api_key = st.text_input("Enter your OpenAI API key:", type="password")

# Initialize API clients if keys are provided
if anthropic_api_key or openai_api_key:
    openai_client = OpenAI(api_key=openai_api_key)
    anthropic_client = anthropic.Anthropic(api_key=anthropic_api_key)

# Define function for interacting with Claude API
def get_claude_response(prompt):
    message = anthropic_client.messages.create(
        model="claude-3-5-sonnet-20241022",  # Specify Claude model version here
        max_tokens=1000,
        temperature=0,
        system="You are a helpful Indian legal assistant. Respond clearly and concisely.",
        messages=[{"role": "user", "content": [{"type": "text", "text": prompt}]}]
    )
    return message.content

# Define function for interacting with OpenAI API
def get_openai_response(prompt, model="gpt-4"):
    completion = openai_client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful Indian legal assistant. Respond clearly and concisely."},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content

# Streamlit App UI
st.title("Court Craft Legal Assistant")
st.write("Select a model to get legal assistance for your queries.")

# Model selection
model_choice = st.selectbox("Choose the model", ["Claude", "GPT"])

# User input for legal question
user_input = st.text_area("Enter your legal question:", "")

# Button to get response
if st.button("Get Response"):
    if user_input:
        if model_choice == "Claude":
            try:
                response = get_claude_response(user_input)
                st.write("### Claude's Response")
                st.write(response)
            except Exception as e:
                st.write("Error in fetching response from Claude:", e)
        elif model_choice == "GPT":
            try:
                response = get_openai_response(user_input)
                st.write(f"### GPT's Response")
                st.write(response)
            except Exception as e:
                st.write("Error in fetching response from OpenAI:", e)
    else:
        st.write("Please enter a question.")

