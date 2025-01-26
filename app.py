import os
import streamlit as st
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Load environment variables
load_dotenv()

# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = "YOUR OPEN_API_KEY"
api_key = os.getenv("OPENAI_API_KEY")

# Define the prompt template for README generation
README_PROMPT_TEMPLATE = """
Generate a professional README file for a project based on the following details:
For the file {file_content}, write the following things
Project Name: 
Description: 
Installation Instructions: 
Usage: 
Contributing Guidelines: 
License: 

The README should be well-structured, concise, and written in markdown format. Include appropriate headings and sections.
"""

# Function to generate README using AI
def generate_readme(file_content):
    # Initialize the AI model
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7, api_key=api_key)

    # Create a prompt template
    prompt = PromptTemplate(
        input_variables=["file_content"],  # This must be a string variable name
        template=README_PROMPT_TEMPLATE,
    )

    # Create an LLM chain
    chain = LLMChain(llm=llm, prompt=prompt)

    # Generate the README (pass file_content as input)
    readme_content = chain.run({"file_content": file_content})

    return readme_content

# Main function to run the Streamlit app
def main():
    st.set_page_config(page_title="AI README Generator")

    st.title("AI README Generator")
    st.write("Upload your code file and generate a professional README file for your project using AI.")

    # File uploader for code file
    uploaded_file = st.file_uploader("Upload your code file", type=["py", "js", "java", "cpp", "html", "css"])

    if uploaded_file is not None:
        # Read the file content
        file_content = uploaded_file.getvalue().decode("utf-8")

        # Button to generate README
        if st.button("Generate README"):
            with st.spinner("Generating README..."):
                # Generate the README
                readme_content = generate_readme(file_content)

                # Display the generated README
                st.subheader("Generated README")
                st.markdown(readme_content)

                # Add a download button
                st.download_button(
                    label="Download README",
                    data=readme_content,
                    file_name="README.md",
                    mime="text/markdown",
                )

# Run the app
if __name__ == "__main__":
    main()
