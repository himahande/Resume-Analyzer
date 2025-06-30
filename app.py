import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf

# Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("GEMINI_API_KEY environment variable not set. Please set it to your Gemini API key.")
else:
    genai.configure(api_key=api_key)

def get_gemini_response(prompt):
    model=genai.GenerativeModel('gemini-2.0-flash')
    response=model.generate_content(prompt)
    return response.text

def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

# Streamlit App
st.set_page_config(page_title="AI Resume Analyzer", page_icon=":robot_face:")

st.title("AI Resume Screening Assistant")
st.markdown("---")
st.markdown("### Let's analyze a resume together! :sparkles:")

input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully! :heavy_check_mark:")

submit1 = st.button("Tell Me About the Resume")
submit2 = st.button("Percentage Match")

input_prompt1 = """
You are an experienced Technical Human Resource Manager, your task is to review the provided resume against the job description.
Please share your professional evaluation on whether the candidate's profile aligns with the role.
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt2 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_text(uploaded_file)
        full_prompt = input_prompt1 + "\n\nJob Description:\n" + input_text + "\n\nResume:\n" + pdf_content
        response=get_gemini_response(full_prompt)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit2:
    if uploaded_file is not None:
        pdf_content=input_pdf_text(uploaded_file)
        full_prompt = input_prompt2 + "\n\nJob Description:\n" + input_text + "\n\nResume:\n" + pdf_content
        response=get_gemini_response(full_prompt)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

st.markdown("---")
st.markdown("Made by Hima Hande")