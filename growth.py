import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Data Sweeper", layout='wide')

# Apply CSS
st.markdown(
    """
    <style>
    .stApp{
        background-color: black ;
        color: white;
        }
         /* Scrollbar Track (Background) */
    ::-webkit-scrollbar {
        width: 10px;
        background: white;
    }

    /* Scrollbar Handle */
    ::-webkit-scrollbar-thumb {
        background: white;  /* Change to your preferred color */
        border-radius: 10px;
    }

    /* Scrollbar Handle on Hover */
    ::-webkit-scrollbar-thumb:hover {
        background: white;  /* Slightly darker shade */
    }

    /* Scrollbar Track when scrolling */
    ::-webkit-scrollbar-track {
        background: #121212; /* Match background color */
    }
        </style>
    """,
    unsafe_allow_html=True
)

# Title and Description
st.title("🧹 Data Sweeper Sterling Integrator By Sofia Ibrahim")
st.write("🚀 Transform Your File between CSV And Excel formats With built-in data cleaning and visualization ")

# Upload File
uploaded_files = st.file_uploader("📂 Upload Your Files (accept CSV Or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

# Process Uploaded Files
if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        # Read File with Header Fix
        if file_ext == ".csv":
            df = pd.read_csv(file, header=0)  # Ensuring the first row is treated as headers
        elif file_ext == ".xlsx":
            df = pd.read_excel(file, header=0)  # Ensuring first row as headers
        else:
            st.error(f"❌ Unsupported file type: {file_ext}")
            continue

        if df.empty:
            st.error(f"⚠️ {file.name} is empty! Please upload a valid file.")
            continue  # Skip empty files

        # Fix Column Names Issue
        if all(df.columns.str.contains("Unnamed")):
            df.columns = df.iloc[0]  # Set first row as header if unnamed
            df = df[1:].reset_index(drop=True)  # Remove first row from data

        # File Preview
        st.subheader(f"👀 Preview of {file.name}")
        st.dataframe(df.head())

        # Data Cleaning
        st.subheader(f"🧼 Data Cleaning Options for {file.name}")

        if st.button(f"🗑️ Remove duplicates from {file.name}"):
            df.drop_duplicates(inplace=True)
            st.write("✅ Duplicates Removed!")

        if st.button(f"🔧 Fill Missing Values for {file.name}"):
            numeric_cols = df.select_dtypes(include=['number']).columns
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
            st.write("✅ Missing Values Filled!")

        # Column Selection
        st.subheader(f"📌 Select Columns to Display for {file.name}")
        selected_columns = st.multiselect(f"📝 Choose columns for {file.name}", df.columns, default=df.columns)
        df = df[selected_columns]

        # Data Visualization
        st.subheader(f"📊 Data Visualization for {file.name}")

        if st.checkbox(f"📉 Show Visualization for {file.name}"):
            numeric_df = df.select_dtypes(include=['number'])

            if numeric_df.shape[1] >= 1:
                st.line_chart(numeric_df)  # Change to line chart if only 1 column
            else:
                st.error("⚠️ Not enough numerical columns for visualization.")

        # File Conversion
        st.subheader(f"🔄 Convert {file.name}")
        conversion_type = st.radio(f"📂 Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        if st.button(f"💾 Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)

            st.download_button(
                label=f"⬇️ Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

st.success("✅ All Files Processed Successfully!")
