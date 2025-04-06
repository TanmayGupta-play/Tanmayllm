import streamlit as st
import pdf2final_list
import text2ppt
import shutil
import os
import tempfile
from pathlib import Path

# Set page config (optional)
st.set_page_config(
    page_title="PDF2PPT Generator",
    page_icon="📊",
    layout="centered"
)

# Add some custom styling
st.markdown("""
    <style>
    .main-header {
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .success-message {
        color: #0f5132;
        background-color: #d1e7dd;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    .error-message {
        color: #842029;
        background-color: #f8d7da;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Display header
st.markdown('<div class="main-header">PDF to PowerPoint Generator</div>', unsafe_allow_html=True)

# Input field for topics
topics_input = st.text_input("Enter comma-separated topics:", placeholder="e.g. Artificial Intelligence, Machine Learning, Data Science")

# Process button
if st.button("Generate PowerPoint", type="primary", use_container_width=True):
    if topics_input:
        try:
            # Show processing status
            status_placeholder = st.empty()
            status_placeholder.info("Processing your request... Please wait.")
            
            # Parse input topics
            if "," in topics_input:
                topics_list = [topic.strip() for topic in topics_input.split(",")]
            else:
                topics_list = [topics_input.strip()]
            
            # Process topics
            st.write(f"Processing topics: {topics_list}")
            result = pdf2final_list.process(topics_list)
            
            # Generate presentation
            st.write("Generating PowerPoint presentation...")
            text2ppt.presentate(result)
            
            # Create a temporary file for the user to download
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pptx') as tmp_file:
                temp_path = tmp_file.name
            
            # Copy the presentation to the temporary file
            shutil.copy("PPT.pptx", temp_path)
            
            # Create a download button
            with open(temp_path, "rb") as file:
                status_placeholder.empty()
                st.markdown('<div class="success-message">Presentation created successfully!</div>', unsafe_allow_html=True)
                st.download_button(
                    label="Download PowerPoint Presentation",
                    data=file,
                    file_name=f"presentation_{'-'.join(topics_list)}.pptx",
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                    use_container_width=True
                )
                
        except Exception as e:
            status_placeholder.empty()
            st.markdown(f'<div class="error-message">Error: {str(e)}</div>', unsafe_allow_html=True)
    else:
        st.error("Please enter at least one topic.")

# Add some information about the application
with st.expander("How to use this application"):
    st.write("""
    1. Enter one or more topics separated by commas
    2. Click the 'Generate PowerPoint' button
    3. Wait for the presentation to be generated
    4. Download the PowerPoint file
    5. Open it in PowerPoint or any compatible presentation software
    """)

# Footer
st.markdown("---")
st.caption("PDF2PPT Generator © 2025")