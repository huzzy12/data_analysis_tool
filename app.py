import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from io import BytesIO

# Set page configuration
st.set_page_config(
    page_title="Data Analysis Tool",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #26A69A;
    }
    .card {
        padding: 20px;
        border-radius: 5px;
        margin-bottom: 20px;
        background-color: #f8f9fa;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/000000/statistics.png", width=100)
    st.markdown("## Data Analysis Tool")
    st.info("Upload your data to analyze, visualize, and gain insights.")

# Main content
st.markdown("<h1 class='main-header'>Data Analysis Tool</h1>", unsafe_allow_html=True)
st.write("Upload your dataset to explore and gain insights.")

# File uploader
uploaded_file = st.file_uploader("Upload your CSV or Excel file", type=["csv", "xls", "xlsx"])

@st.cache_data
def load_data(file):
    try:
        if file.name.endswith('.csv'):
            return pd.read_csv(file)
        elif file.name.endswith(('.xls', '.xlsx')):
            return pd.read_excel(file)
        else:
            st.error("Unsupported file type!")
            return None
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

if uploaded_file is not None:
    # Load data with error handling
    data = load_data(uploaded_file)
    
    if data is not None:
        st.success(f"Successfully loaded file: {uploaded_file.name}")
        
        # Data info
        with st.expander("Dataset Information", expanded=True):
            st.write(f"Rows: {data.shape[0]}, Columns: {data.shape[1]}")
            
            # Show column types
            col_types = pd.DataFrame({
                'Column Name': data.columns,
                'Data Type': data.dtypes.astype(str),
                'Missing Values': data.isnull().sum().values,
                'Missing %': (data.isnull().sum().values / len(data) * 100).round(2)
            })
            st.dataframe(col_types)
            
            # Data preview
            st.subheader("Data Preview")
            st.dataframe(data.head(10))
        
        # Data cleaning section
        with st.expander("Data Cleaning Tools", expanded=True):
            st.subheader("Data Cleaning")
            st.write("Clean your data to prepare it for analysis.")
            
            cleaning_col1, cleaning_col2 = st.columns(2)
            
            with cleaning_col1:
                # Remove duplicates
                if st.checkbox("Remove Duplicate Rows"):
                    duplicate_count = data.duplicated().sum()
                    if duplicate_count > 0:
                        data = data.drop_duplicates()
                        st.success(f"Removed {duplicate_count} duplicate rows!")
                    else:
                        st.info("No duplicates found in your data.")
                
                # Handle missing values
                if st.checkbox("Handle Missing Values"):
                    missing_method = st.radio(
                        "Choose method for handling missing values:",
                        ["Drop rows with any missing values", 
                         "Fill numeric columns with mean",
                         "Fill with custom value"]
                    )
                    
                    if missing_method == "Drop rows with any missing values":
                        missing_count = data.isnull().any(axis=1).sum()
                        if missing_count > 0:
                            data = data.dropna()
                            st.success(f"Dropped {missing_count} rows with missing values!")
                        else:
                            st.info("No missing values found in your data.")
                            
                    elif missing_method == "Fill numeric columns with mean":
                        numeric_cols = data.select_dtypes(include=['number']).columns
                        if len(numeric_cols) > 0:
                            for col in numeric_cols:
                                if data[col].isnull().any():
                                    data[col] = data[col].fillna(data[col].mean())
                            st.success(f"Filled missing values in numeric columns with their means!")
                        else:
                            st.warning("No numeric columns found.")
                            
                    elif missing_method == "Fill with custom value":
                        fill_value = st.text_input("Enter value to fill missing data with:", "0")
                        if st.button("Fill Missing Values"):
                            data = data.fillna(fill_value)
                            st.success(f"Filled all missing values with '{fill_value}'!")
            
            with cleaning_col2:
                # Data type conversion
                if st.checkbox("Convert Column Data Types"):
                    col_to_convert = st.selectbox("Select column to convert:", data.columns)
                    target_type = st.selectbox("Convert to:", ["string", "number", "date", "category"])
                    
                    if st.button("Convert"):
                        try:
                            if target_type == "string":
                                data[col_to_convert] = data[col_to_convert].astype(str)
                            elif target_type == "number":
                                data[col_to_convert] = pd.to_numeric(data[col_to_convert])
                            elif target_type == "date":
                                data[col_to_convert] = pd.to_datetime(data[col_to_convert])
                            elif target_type == "category":
                                data[col_to_convert] = data[col_to_convert].astype('category')
                            st.success(f"Converted {col_to_convert} to {target_type}!")
                        except Exception as e:
                            st.error(f"Error converting column: {e}")
                
                # Column selection
                if st.checkbox("Select Columns to Keep"):
                    selected_cols = st.multiselect("Choose columns to keep in your dataset:", data.columns, default=list(data.columns))
                    if st.button("Filter Columns"):
                        if selected_cols:
                            data = data[selected_cols]
                            st.success(f"Kept {len(selected_cols)} columns in your dataset!")
                        else:
                            st.warning("Please select at least one column.")
        
        # Data visualization
        with st.expander("Data Visualization", expanded=True):
            st.subheader("Data Visualization")
            st.write("Visualize your data to discover patterns and insights.")
            
            # Check if dataset has numeric columns for visualization
            numeric_columns = data.select_dtypes(include=['number']).columns.tolist()
            if len(numeric_columns) >= 1:
                # Chart type selection
                chart_type = st.selectbox(
                    "Select chart type:",
                    ["Bar Chart", "Line Chart", "Scatter Plot", "Histogram", "Box Plot", "Correlation Matrix"]
                )
                
                if chart_type != "Correlation Matrix":
                    x_axis = st.selectbox("Select X-axis:", data.columns)
                    
                    if chart_type in ["Bar Chart", "Line Chart", "Scatter Plot"]:
                        y_axis = st.selectbox("Select Y-axis:", numeric_columns)
                    
                # Create visualizations
                if st.button("Generate Visualization"):
                    st.subheader(f"{chart_type} Visualization")
                    
                    try:
                        if chart_type == "Bar Chart":
                            fig, ax = plt.subplots(figsize=(10, 6))
                            data.groupby(x_axis)[y_axis].mean().plot(kind='bar', ax=ax)
                            ax.set_title(f"{y_axis} by {x_axis}")
                            ax.set_ylabel(y_axis)
                            st.pyplot(fig)
                            
                        elif chart_type == "Line Chart":
                            fig, ax = plt.subplots(figsize=(10, 6))
                            data.plot(x=x_axis, y=y_axis, kind='line', ax=ax)
                            ax.set_title(f"{y_axis} over {x_axis}")
                            ax.set_ylabel(y_axis)
                            st.pyplot(fig)
                            
                        elif chart_type == "Scatter Plot":
                            fig, ax = plt.subplots(figsize=(10, 6))
                            data.plot(x=x_axis, y=y_axis, kind='scatter', ax=ax)
                            ax.set_title(f"{y_axis} vs {x_axis}")
                            ax.set_ylabel(y_axis)
                            st.pyplot(fig)
                            
                        elif chart_type == "Histogram":
                            fig, ax = plt.subplots(figsize=(10, 6))
                            data[x_axis].plot(kind='hist', ax=ax)
                            ax.set_title(f"Distribution of {x_axis}")
                            ax.set_xlabel(x_axis)
                            st.pyplot(fig)
                            
                        elif chart_type == "Box Plot":
                            fig, ax = plt.subplots(figsize=(10, 6))
                            data[x_axis].plot(kind='box', ax=ax)
                            ax.set_title(f"Box Plot of {x_axis}")
                            st.pyplot(fig)
                            
                        elif chart_type == "Correlation Matrix":
                            fig, ax = plt.subplots(figsize=(12, 8))
                            corr_data = data[numeric_columns].corr()
                            cax = ax.matshow(corr_data, cmap='coolwarm')
                            fig.colorbar(cax)
                            ax.set_xticks(range(len(corr_data.columns)))
                            ax.set_yticks(range(len(corr_data.columns)))
                            ax.set_xticklabels(corr_data.columns, rotation=90)
                            ax.set_yticklabels(corr_data.columns)
                            st.pyplot(fig)
                    
                    except Exception as e:
                        st.error(f"Error generating visualization: {e}")
            else:
                st.warning("Your dataset needs numeric columns for visualization.")
        
        # Data export
        with st.expander("Export Processed Data"):
            st.subheader("Export Your Processed Data")
            
            export_format = st.radio("Select export format:", ["CSV", "Excel"])
            filename = st.text_input("Enter filename (without extension):", f"processed_{uploaded_file.name.split('.')[0]}")
            
            if st.button("Export Data"):
                try:
                    if export_format == "CSV":
                        csv_data = data.to_csv(index=False)
                        st.download_button(
                            label="Download CSV",
                            data=csv_data,
                            file_name=f"{filename}.csv",
                            mime="text/csv"
                        )
                        st.success("CSV file ready for download!")
                        
                    elif export_format == "Excel":
                        output = BytesIO()
                        with pd.ExcelWriter(output, engine='openpyxl') as writer:
                            data.to_excel(writer, index=False, sheet_name="Processed_Data")
                        output.seek(0)
                        
                        st.download_button(
                            label="Download Excel",
                            data=output,
                            file_name=f"{filename}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                        st.success("Excel file ready for download!")
                
                except Exception as e:
                    st.error(f"Error exporting data: {e}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>Data Analysis Tool - Developed with Streamlit</p>
</div>
""", unsafe_allow_html=True) 