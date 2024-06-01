import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json


load_dotenv()   #load all the environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#Gemini pro response
def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response


def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())


#Prompt Template
input_prompt="""
Hey Act Like a skilled or very experience ATS(Application Tracking System)
with a deep understanding of tech field. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving the resumes. Assign the percentage Matching based 
on Jd and
the missing keywords with high accuracy

Your task is to evaluate the resume against the provided job description and return the output in the following format:

Matching Percentage: [percentage]

Missing Keywords:
in the format = [keyword1] | [keyword2] | [keyword3] |

Final Thoughts:
[final thoughts]

Recommendations:
* [recommendation1]
* [recommendation2]
* [recommendation3]
dont wanna send me back the resume and Job description

"""


#Streamlit app
st.title('Resume Analyzer')
st.text('Tailor your Resume for the Job Description')

jd = st.text_area('Paste the Job Description')
uploaded_file = st.file_uploader("Upload Your Resume",type="pdf",help="Please upload the pdf")
submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        response = get_gemini_response(input_prompt)
        st.subheader(response.text)