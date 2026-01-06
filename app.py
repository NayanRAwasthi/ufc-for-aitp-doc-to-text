import streamlit as st
import os
from markitdown import MarkItDown
from io import BytesIO

# Initialize MarkItDown engine
# Note: MarkItDown handles the internal logic for MS Office and PDF
md = MarkItDown()

# Page configuration
st.set_page_config(page_title="Universal Document Reader", page_icon="📄")

st.title("📄 Universal Document Reader")
st.markdown("Convert Office docs, PDFs, and HTML into clean Markdown or Plain Text.")

# [2] Upload Area
uploaded_files = st.file_uploader(
    "Drag and drop files here", 
    type=["docx", "xlsx", "pptx", "pdf", "html", "zip"], 
    accept_multiple_files=True
)

if uploaded_files:
    for uploaded_file in uploaded_files:
        file_extension = os.path.splitext(uploaded_file.name)[1].lower()
        base_name = os.path.splitext(uploaded_file.name)[0]
        
        with st.expander(f"📄 Processing: {uploaded_file.name}", expanded=True):
            try:
                # [3] Resilience: Use a temporary byte stream to avoid disk writes
                file_bytes = uploaded_file.getvalue()
                
                # MarkItDown requires a file path or a stream-like object
                # We pass the file name to help it identify the format
                result = md.convert_stream(
                    BytesIO(file_bytes), 
                    extension=file_extension
                )
                
                converted_text = result.text_content

                # [2] Instant Preview
                st.text_area(
                    label="Preview", 
                    value=converted_text, 
                    height=300, 
                    key=f"text_{uploaded_file.name}"
                )

                # [2] Download Options
                col1, col2 = st.columns(2)
                
                with col1:
                    st.download_button(
                        label="Download as Markdown (.md)",
                        data=converted_text,
                        file_name=f"{base_name}_converted.md",
                        mime="text/markdown",
                        key=f"md_{uploaded_file.name}"
                    )
                
                with col2:
                    st.download_button(
                        label="Download as Text (.txt)",
                        data=converted_text,
                        file_name=f"{base_name}_converted.txt",
                        mime="text/plain",
                        key=f"txt_{uploaded_file.name}"
                    )

            except Exception as e:
                # [3] Resilience: Error Handling
                st.error(f"⚠️ Could not read {uploaded_file.name}. Please check the format.")
                # Optional: Uncomment the next line for debugging
                # st.info(f"Error details: {e}")

# Footer
st.divider()
st.caption("Powered by Microsoft MarkItDown & Streamlit")
