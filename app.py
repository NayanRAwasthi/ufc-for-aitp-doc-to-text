import streamlit as st
import os
from markitdown import MarkItDown
from io import BytesIO

# Initialize the conversion engine
md = MarkItDown()

st.set_page_config(page_title="Universal Document Reader", page_icon="📄")
st.title("📄 Universal Document Reader")

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
                # Process file
                file_bytes = uploaded_file.getvalue()
                original_size_mb = len(file_bytes) / (1024 * 1024)
                
                result = md.convert_stream(BytesIO(file_bytes), extension=file_extension)
                converted_text = result.text_content
                converted_size_mb = len(converted_text.encode('utf-8')) / (1024 * 1024)

                # Tabs for Content and Comparison
                tab1, tab2 = st.tabs(["📝 Converted Content", "📊 File Size Comparison"])

                with tab1:
                    st.text_area("Preview", value=converted_text, height=300, key=f"prev_{uploaded_file.name}")
                    
                    # Download buttons
                    c1, c2 = st.columns(2)
                    c1.download_button("Download .md", converted_text, f"{base_name}.md", "text/markdown")
                    c2.download_button("Download .txt", converted_text, f"{base_name}.txt", "text/plain")

                with tab2:
                    # [NEW] File Size Comparison Logic
                    st.subheader("Efficiency Metrics")
                    
                    # Create Table
                    data = {
                        "File State": ["Original File", "Converted Text"],
                        "Size (MB)": [f"{original_size_mb:.2f} MB", f"{converted_size_mb:.2f} MB"]
                    }
                    st.table(data)

                    # Calculate Percentage Reduction
                    if original_size_mb > 0:
                        reduction = ((original_size_mb - converted_size_mb) / original_size_mb) * 100
                        st.success(f"💡 **Text version is {reduction:.1f}% smaller.**")

            except Exception as e:
                st.error(f"⚠️ Could not read {uploaded_file.name}. Please check the format.")
