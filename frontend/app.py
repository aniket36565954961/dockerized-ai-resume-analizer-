import streamlit as st
import requests

st.set_page_config(page_title="Resume Perfect AI", layout="centered")

st.title("?? Resume Perfect AI")
st.write("If you see this text, the app is WORKING!")

# Input fields
uploaded_file = st.file_uploader("1. Upload Resume (PDF/TXT)", type=["pdf", "txt"])
job_description = st.text_area("2. Paste Job Description")

if st.button("Analyze Resume"):
    st.info("Sending to backend...")
    # This connects to the backend container
    try:
        files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
        data = {"job_description": job_description}
        response = requests.post("http://ai-backend:8000/analyze", files=files, data=data)
        
        if response.status_code == 200:
            st.success("Analysis Complete!")
            st.json(response.json())
        else:
            st.error(f"Error: {response.status_code}")
    except Exception as e:
        st.error(f"Connection Error: {e}")
