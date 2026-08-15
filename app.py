import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
import asyncio
import matplotlib.pyplot as plt

# --------------------------------------------------
# SESSION STATE FOR DATA CLEANING
# --------------------------------------------------

if "cleaned_df" not in st.session_state:
    st.session_state.cleaned_df = None

if "original_df" not in st.session_state:
    st.session_state.original_df = None

if "pending_action" not in st.session_state:
    st.session_state.pending_action = None

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AutoGen Data Analyst",
    page_icon="📊",
    layout="wide"
)

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("📊 AutoGen Data Analyst")

st.subheader(
    "AI-Powered Automated Data Analysis System"
)

st.write(
    "Upload a CSV or Excel file and let the system analyze your data."
)

# --------------------------------------------------
# FILE UPLOAD
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload your dataset",
    type=["csv", "xlsx"]
)

# --------------------------------------------------
# DATA PROCESSING
# --------------------------------------------------

if uploaded_file is not None:

    try:

        # --------------------------------------------------
        # READ FILE
        # --------------------------------------------------

        if uploaded_file.name.lower().endswith(".csv"):

            df = pd.read_csv(uploaded_file)

        elif uploaded_file.name.lower().endswith(".xlsx"):

            df = pd.read_excel(uploaded_file)

        else:

            st.error("Unsupported file format.")
            st.stop()

        # --------------------------------------------------
        # SUCCESS MESSAGE
        # --------------------------------------------------

        st.success(
            f"Dataset '{uploaded_file.name}' uploaded successfully!"
        )
        # Store original dataset
        if st.session_state.original_df is None:
            st.session_state.original_df = df.copy()

        if st.session_state.cleaned_df is None:
             st.session_state.cleaned_df = df.copy()

        # --------------------------------------------------
        # DATASET OVERVIEW
        # --------------------------------------------------

        st.header("📊 Dataset Overview")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Rows",
                df.shape[0]
            )

        with col2:

            st.metric(
                "Columns",
                df.shape[1]
            )

        with col3:

            st.metric(
                "Duplicate Rows",
                int(df.duplicated().sum())
            )

        # --------------------------------------------------
        # DATA PREVIEW
        # --------------------------------------------------

        st.header("👀 Data Preview")

        st.dataframe(
            df.head(10),
            use_container_width=True
        )

        # --------------------------------------------------
        # COLUMN INFORMATION
        # --------------------------------------------------

        st.header("🔤 Column Information")

        column_info = pd.DataFrame({
            "Column": df.columns,
            "Data Type": df.dtypes.astype(str).values,
            "Missing Values": df.isnull().sum().values,
            "Unique Values": df.nunique().values
        })

        st.dataframe(
            column_info,
            use_container_width=True
        )

        # --------------------------------------------------
        # MISSING VALUES
        # --------------------------------------------------

        st.header("❌ Missing Values")

        missing_values = pd.DataFrame({
            "Column": df.columns,
            "Missing Values": df.isnull().sum().values,
            "Missing %": (
                df.isnull().mean().values * 100
            ).round(2)
        })

        st.dataframe(
            missing_values,
            use_container_width=True
        )

        # --------------------------------------------------
        # DATA QUALITY ANALYSIS
        # --------------------------------------------------

        st.header("🧪 Data Quality Analysis")

        # Total cells
        total_cells = df.shape[0] * df.shape[1]

        # Missing cells
        missing_cells = int(
            df.isnull().sum().sum()
        )

        # Missing percentage
        if total_cells > 0:

            missing_percentage = (
                missing_cells / total_cells
            ) * 100

        else:

            missing_percentage = 0

        # Duplicate rows
        duplicate_rows = int(
            df.duplicated().sum()
        )

        # Duplicate percentage
        if len(df) > 0:

            duplicate_percentage = (
                duplicate_rows / len(df)
            ) * 100

        else:

            duplicate_percentage = 0

        # Empty columns
        empty_columns = [
            column
            for column in df.columns
            if df[column].isnull().all()
        ]

        # --------------------------------------------------
        # QUALITY SCORE
        # --------------------------------------------------

        quality_score = 100

        # Missing value penalty
        quality_score -= min(
            missing_percentage * 2,
            30
        )

        # Duplicate penalty
        quality_score -= min(
            duplicate_percentage,
            20
        )

        # Empty column penalty
        quality_score -= min(
            len(empty_columns) * 5,
            20
        )

        quality_score = max(
            round(quality_score),
            0
        )

        # --------------------------------------------------
        # QUALITY STATUS
        # --------------------------------------------------

        if quality_score >= 90:

            quality_status = "Excellent"

        elif quality_score >= 75:

            quality_status = "Good"

        elif quality_score >= 50:

            quality_status = "Needs Improvement"

        else:

            quality_status = "Poor"

        # --------------------------------------------------
        # QUALITY METRICS
        # --------------------------------------------------

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "Quality Score",
                f"{quality_score}/100"
            )

        with col2:

            st.metric(
                "Missing Cells",
                missing_cells
            )

        with col3:

            st.metric(
                "Duplicate Rows",
                duplicate_rows
            )

        with col4:

            st.metric(
                "Empty Columns",
                len(empty_columns)
            )

        # --------------------------------------------------
        # QUALITY STATUS
        # --------------------------------------------------

        st.info(
            f"Dataset Quality Status: **{quality_status}**"
        )

        # --------------------------------------------------
        # QUALITY CHECKS
        # --------------------------------------------------

        st.subheader("🔍 Quality Checks")

        quality_checks = pd.DataFrame({

            "Check": [
                "Missing Values",
                "Duplicate Rows",
                "Empty Columns"
            ],

            "Count": [
                missing_cells,
                duplicate_rows,
                len(empty_columns)
            ],

            "Status": [

                "⚠️ Issues Found"
                if missing_cells > 0
                else "✅ Passed",

                "⚠️ Issues Found"
                if duplicate_rows > 0
                else "✅ Passed",

                "⚠️ Issues Found"
                if len(empty_columns) > 0
                else "✅ Passed"
            ]
        })

        st.dataframe(
            quality_checks,
            use_container_width=True
        )

        # --------------------------------------------------
        # STATISTICAL SUMMARY
        # --------------------------------------------------

        st.header("📈 Statistical Summary")

        numeric_columns = df.select_dtypes(
            include="number"
        )

        if not numeric_columns.empty:

            st.dataframe(
                numeric_columns.describe().T,
                use_container_width=True
            )

        else:

            st.info(
                "No numeric columns were found in this dataset."
            )

        # --------------------------------------------------
        # COMPLETE DATASET
        # --------------------------------------------------

        st.header("📋 Complete Dataset")

        st.dataframe(
            df,
            use_container_width=True
        )

    except Exception as e:

        st.error(
            f"An error occurred while processing the dataset: {e}"
        )

        # --------------------------------------------------
# AUTOMATIC EXPLORATORY DATA ANALYSIS
# --------------------------------------------------

st.header("📊 Automatic Exploratory Data Analysis")

st.write(
    "The system automatically identifies column types "
    "and generates appropriate visualizations."
)

# --------------------------------------------------
# INTELLIGENT COLUMN TYPE DETECTION
# --------------------------------------------------

# Lists for different column types
id_columns = []
numeric_columns = []
categorical_columns = []
date_columns = []


# --------------------------------------------------
# IDENTIFY COLUMNS
# --------------------------------------------------

for column in df.columns:

    column_name = column.lower().strip()

    # ----------------------------------------------
    # 1. Detect ID columns
    # ----------------------------------------------

    id_keywords = [
        "id",
        "_id",
        "code",
        "number",
        "no",
        "number"
    ]

    is_id_column = any(
        keyword in column_name
        for keyword in id_keywords
    )

    # Give priority to explicit ID names
    if (
        column_name.endswith("id")
        or "_id" in column_name
        or column_name.startswith("id")
    ):

        id_columns.append(column)

        continue


    # ----------------------------------------------
    # 2. Detect Date columns
    # ----------------------------------------------

    converted_dates = pd.to_datetime(
        df[column],
        errors="coerce",
        dayfirst=True
    )

    date_success_rate = (
        converted_dates.notna().mean()
    )

    if (
        date_success_rate >= 0.8
        and df[column].nunique() > 1
    ):

        date_columns.append(column)

        continue


    # ----------------------------------------------
    # 3. Detect Numeric columns
    # ----------------------------------------------

    if pd.api.types.is_numeric_dtype(
        df[column]
    ):

        numeric_columns.append(column)

        continue


    # ----------------------------------------------
    # 4. Everything else = Categorical
    # ----------------------------------------------

    categorical_columns.append(column)


# --------------------------------------------------
# COLUMN TYPE SUMMARY
# --------------------------------------------------

st.subheader("🔍 Detected Column Types")

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.write("**🆔 Identifier Columns**")

    if id_columns:

        for column in id_columns:

            st.write(f"• {column}")

    else:

        st.write("None detected")


with col2:

    st.write("**🔢 Numeric Columns**")

    if numeric_columns:

        for column in numeric_columns:

            st.write(f"• {column}")

    else:

        st.write("None detected")


with col3:

    st.write("**🔤 Categorical Columns**")

    if categorical_columns:

        for column in categorical_columns:

            st.write(f"• {column}")

    else:

        st.write("None detected")


with col4:

    st.write("**📅 Date Columns**")

    if date_columns:

        for column in date_columns:

            st.write(f"• {column}")

    else:

        st.write("None detected")
# --------------------------------------------------
# IDENTIFY COLUMN TYPES
# --------------------------------------------------

# numeric_columns = df.select_dtypes(
#     include="number"
# ).columns.tolist()

# categorical_columns = df.select_dtypes(
#     include=["object", "category"]
# ).columns.tolist()

# # Try to identify date columns
# date_columns = []

# for column in df.columns:

#     if column not in numeric_columns:

#         converted_dates = pd.to_datetime(
#             df[column],
#             errors="coerce"
#         )

#         # Consider it a date column if most values
#         # can be converted successfully
#         if (
#             converted_dates.notna().mean() >= 0.8
#             and df[column].nunique() > 1
#         ):

#             date_columns.append(column)


# --------------------------------------------------
# COLUMN TYPE SUMMARY
# --------------------------------------------------

st.subheader("🔍 Detected Column Types")

col1, col2, col3 = st.columns(3)

with col1:

    st.write("**🔢 Numeric Columns**")

    if numeric_columns:

        for column in numeric_columns:
            st.write(f"• {column}")

    else:

        st.write("None detected")


with col2:

    st.write("**🔤 Categorical Columns**")

    if categorical_columns:

        for column in categorical_columns:
            st.write(f"• {column}")

    else:

        st.write("None detected")


with col3:

    st.write("**📅 Date Columns**")

    if date_columns:

        for column in date_columns:
            st.write(f"• {column}")

    else:

        st.write("None detected")


# --------------------------------------------------
# NUMERIC DISTRIBUTIONS
# --------------------------------------------------

if numeric_columns:

    st.subheader("📈 Numeric Variable Distributions")

    for column in numeric_columns:

        fig = px.histogram(
            df,
            x=column,
            title=f"Distribution of {column}",
            nbins=20
        )

        fig.update_layout(
            xaxis_title=column,
            yaxis_title="Frequency"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# --------------------------------------------------
# CATEGORICAL ANALYSIS
# --------------------------------------------------

if categorical_columns:

    st.subheader("📊 Categorical Variable Analysis")

    for column in categorical_columns:

        value_counts = (
            df[column]
            .value_counts()
            .reset_index()
        )

        value_counts.columns = [
            column,
            "Count"
        ]

        fig = px.bar(
            value_counts,
            x=column,
            y="Count",
            title=f"{column} Distribution",
            text="Count"
        )

        fig.update_layout(
            xaxis_title=column,
            yaxis_title="Count"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# --------------------------------------------------
# DATE TREND ANALYSIS
# --------------------------------------------------

if date_columns and numeric_columns:

    st.subheader("📅 Time-Series Analysis")

    for date_column in date_columns:

        temp_df = df.copy()

        temp_df[date_column] = pd.to_datetime(
            temp_df[date_column],
            errors="coerce"
        )

        temp_df = temp_df.dropna(
            subset=[date_column]
        )

        for numeric_column in numeric_columns:

            trend_df = (
                temp_df
                .groupby(date_column)[numeric_column]
                .sum()
                .reset_index()
                .sort_values(date_column)
            )

            fig = px.line(
                trend_df,
                x=date_column,
                y=numeric_column,
                markers=True,
                title=(
                    f"{numeric_column} Trend Over Time"
                )
            )

            fig.update_layout(
                xaxis_title=date_column,
                yaxis_title=numeric_column
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


# --------------------------------------------------
# CORRELATION ANALYSIS
# --------------------------------------------------

if len(numeric_columns) >= 2:

    st.subheader("🔗 Correlation Analysis")

    correlation_matrix = df[
        numeric_columns
    ].corr()

    fig = px.imshow(
        correlation_matrix,
        text_auto=True,
        title="Numeric Variable Correlation Matrix",
        aspect="auto"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------------------------------
# OUTLIER DETECTION
# --------------------------------------------------

st.header("🚨 Outlier Detection")

st.write(
    "The system uses the Interquartile Range (IQR) "
    "method to identify potential outliers."
)

outlier_results = []

for column in numeric_columns:

    # Calculate Q1 and Q3
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)

    # Calculate IQR
    IQR = Q3 - Q1

    # Calculate boundaries
    lower_bound = Q1 - (1.5 * IQR)
    upper_bound = Q3 + (1.5 * IQR)

    # Find outliers
    outliers = df[
        (df[column] < lower_bound) |
        (df[column] > upper_bound)
    ]

    outlier_count = len(outliers)

    outlier_results.append({
        "Column": column,
        "Q1": round(Q1, 2),
        "Q3": round(Q3, 2),
        "Lower Bound": round(lower_bound, 2),
        "Upper Bound": round(upper_bound, 2),
        "Outlier Count": outlier_count
    })


# Convert results to DataFrame
outlier_summary = pd.DataFrame(
    outlier_results
)

# Display results
st.dataframe(
    outlier_summary,
    use_container_width=True
)


# --------------------------------------------------
# OUTLIER DETAILS
# --------------------------------------------------

st.subheader("🔍 Outlier Details")

found_outliers = False

for column in numeric_columns:

    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)

    IQR = Q3 - Q1

    lower_bound = Q1 - (1.5 * IQR)
    upper_bound = Q3 + (1.5 * IQR)

    outliers = df[
        (df[column] < lower_bound) |
        (df[column] > upper_bound)
    ]

    if not outliers.empty:

        found_outliers = True

        st.warning(
            f"⚠️ {column}: "
            f"{len(outliers)} potential outlier(s) detected."
        )

        st.dataframe(
            outliers,
            use_container_width=True
        )


if not found_outliers:

    st.success(
        "✅ No significant statistical outliers "
        "were detected in the numeric columns."
    )

    # --------------------------------------------------
# SQL ANALYTICS
# --------------------------------------------------

st.header("🗄️ SQL Analytics")

st.write(
    "The uploaded dataset is converted into a temporary "
    "SQLite database so that SQL queries can be executed."
)

# --------------------------------------------------
# CREATE SQLITE DATABASE
# --------------------------------------------------

connection = sqlite3.connect(":memory:")

# Store dataframe as a SQL table
df.to_sql(
    "sales_data",
    connection,
    index=False,
    if_exists="replace"
)

st.success(
    "Dataset successfully loaded into SQLite database."
)

# --------------------------------------------------
# SHOW TABLE INFORMATION
# --------------------------------------------------

st.subheader("📋 Database Table")

st.write(
    "Table name: `sales_data`"
)

st.write(
    f"Number of records: **{len(df)}**"
)

# --------------------------------------------------
# SAMPLE SQL QUERIES
# --------------------------------------------------

st.subheader("🔎 Example SQL Queries")

example_queries = {
    "Total Sales": """
SELECT SUM(Sales) AS Total_Sales
FROM sales_data;
""",

    "Total Profit": """
SELECT SUM(Profit) AS Total_Profit
FROM sales_data;
""",

    "Sales by Region": """
SELECT
    Region,
    SUM(Sales) AS Total_Sales
FROM sales_data
GROUP BY Region
ORDER BY Total_Sales DESC;
""",

    "Profit by Region": """
SELECT
    Region,
    SUM(Profit) AS Total_Profit
FROM sales_data
GROUP BY Region
ORDER BY Total_Profit DESC;
""",

    "Sales by Category": """
SELECT
    Category,
    SUM(Sales) AS Total_Sales
FROM sales_data
GROUP BY Category
ORDER BY Total_Sales DESC;
""",

    "Top Products": """
SELECT
    Product,
    SUM(Sales) AS Total_Sales
FROM sales_data
GROUP BY Product
ORDER BY Total_Sales DESC
LIMIT 5;
"""
}

selected_query = st.selectbox(
    "Choose a SQL analysis:",
    list(example_queries.keys())
)

query = example_queries[selected_query]

st.code(
    query,
    language="sql"
)

# --------------------------------------------------
# EXECUTE SQL QUERY
# --------------------------------------------------

if st.button("▶ Run SQL Query"):

    try:

        result = pd.read_sql_query(
            query,
            connection
        )

        st.subheader("📊 Query Result")

        st.dataframe(
            result,
            use_container_width=True
        )

    except Exception as e:

        st.error(
            f"SQL Error: {e}"
        )

# --------------------------------------------------
# CUSTOM SQL QUERY
# --------------------------------------------------

st.subheader("⌨️ Run Your Own SQL Query")

custom_query = st.text_area(
    "Enter SQL query:",
    placeholder=(
        "Example: SELECT Region, SUM(Sales) "
        "FROM sales_data GROUP BY Region;"
    ),
    height=120
)

if st.button("🚀 Execute Custom SQL"):

    if custom_query.strip():

        try:

            result = pd.read_sql_query(
                custom_query,
                connection
            )

            st.success(
                "SQL query executed successfully!"
            )

            st.dataframe(
                result,
                use_container_width=True
            )

        except Exception as e:

            st.error(
                f"SQL Error: {e}"
            )

    else:

        st.warning(
            "Please enter a SQL query."
        )

# Close database connection
connection.close()
# --------------------------------------------------
# 📊 AUTOMATIC KPI DASHBOARD
# --------------------------------------------------

st.header("📊 Key Performance Indicators")

# Find possible sales and profit columns
sales_column = None
profit_column = None

for column in df.columns:

    column_lower = column.lower()

    if "sales" in column_lower or "revenue" in column_lower:
        sales_column = column

    if "profit" in column_lower:
        profit_column = column


# Calculate KPIs
total_records = len(df)

total_sales = (
    df[sales_column].sum()
    if sales_column is not None
    else None
)

total_profit = (
    df[profit_column].sum()
    if profit_column is not None
    else None
)

average_sales = (
    df[sales_column].mean()
    if sales_column is not None
    else None
)

if (
    total_sales is not None
    and total_sales != 0
    and total_profit is not None
):

    profit_margin = (
        total_profit / total_sales
    ) * 100

else:

    profit_margin = None


# Display KPIs
col1, col2, col3, col4, col5 = st.columns(5)


with col1:

    st.metric(
        "🧾 Records",
        f"{total_records:,}"
    )


with col2:

    if total_sales is not None:

        st.metric(
            "💰 Total Sales",
            f"{total_sales:,.2f}"
        )

    else:

        st.metric(
            "💰 Total Sales",
            "N/A"
        )


with col3:

    if total_profit is not None:

        st.metric(
            "📈 Total Profit",
            f"{total_profit:,.2f}"
        )

    else:

        st.metric(
            "📈 Total Profit",
            "N/A"
        )


with col4:

    if average_sales is not None:

        st.metric(
            "📊 Average Sales",
            f"{average_sales:,.2f}"
        )

    else:

        st.metric(
            "📊 Average Sales",
            "N/A"
        )


with col5:

    if profit_margin is not None:

        st.metric(
            "💹 Profit Margin",
            f"{profit_margin:.2f}%"
        )

    else:

        st.metric(
            "💹 Profit Margin",
            "N/A"
        )
        # --------------------------------------------------
# 🔎 AUTOMATIC OUTLIER DETECTION
# --------------------------------------------------

st.header("🔎 Outlier Detection")

numeric_columns = df.select_dtypes(
    include="number"
).columns.tolist()

if numeric_columns:

    outlier_summary = []

    for column in numeric_columns:

        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)

        IQR = Q3 - Q1

        lower_bound = Q1 - (1.5 * IQR)
        upper_bound = Q3 + (1.5 * IQR)

        outliers = df[
            (df[column] < lower_bound)
            | (df[column] > upper_bound)
        ]

        outlier_count = len(outliers)

        outlier_percentage = (
            outlier_count / len(df) * 100
            if len(df) > 0
            else 0
        )

        if outlier_count == 0:
            status = "✅ No Outliers"

        elif outlier_percentage < 5:
            status = "⚠️ Few Outliers"

        else:
            status = "🔴 High Outliers"

        outlier_summary.append({
            "Column": column,
            "Outlier Count": outlier_count,
            "Outlier %": round(
                outlier_percentage,
                2
            ),
            "Lower Bound": round(
                lower_bound,
                2
            ),
            "Upper Bound": round(
                upper_bound,
                2
            ),
            "Status": status
        })

    outlier_df = pd.DataFrame(
        outlier_summary
    )

    st.dataframe(
        outlier_df,
        use_container_width=True
    )

else:

    st.info(
        "No numeric columns were found for "
        "outlier detection."
    )
    # --------------------------------------------------
# 📥 DOWNLOAD ANALYSIS REPORT
# --------------------------------------------------

st.header("📥 Download Analysis Report")

# Create report information
report_data = {
    "Metric": [
        "Total Rows",
        "Total Columns",
        "Duplicate Rows",
        "Missing Cells",
        "Quality Score",
        "Quality Status"
    ],
    "Value": [
        df.shape[0],
        df.shape[1],
        int(df.duplicated().sum()),
        int(df.isnull().sum().sum()),
        f"{quality_score}/100",
        quality_status
    ]
}

# Add KPI information if available

if total_sales is not None:

    report_data["Metric"].append(
        "Total Sales"
    )

    report_data["Value"].append(
        round(total_sales, 2)
    )


if total_profit is not None:

    report_data["Metric"].append(
        "Total Profit"
    )

    report_data["Value"].append(
        round(total_profit, 2)
    )


if average_sales is not None:

    report_data["Metric"].append(
        "Average Sales"
    )

    report_data["Value"].append(
        round(average_sales, 2)
    )


if profit_margin is not None:

    report_data["Metric"].append(
        "Profit Margin"
    )

    report_data["Value"].append(
        f"{profit_margin:.2f}%"
    )


report_df = pd.DataFrame(
    report_data
)

# Display report preview

st.dataframe(
    report_df,
    use_container_width=True
)

# Convert to CSV

report_csv = report_df.to_csv(
    index=False
).encode("utf-8")

# Download button

st.download_button(
    label="📥 Download Analysis Report",
    data=report_csv,
    file_name="data_analysis_report.csv",
    mime="text/csv"
)
#####################################################
# --------------------------------------------------
# 📊 AUTOMATIC ANALYTICS DASHBOARD
# --------------------------------------------------
# Can create through Ask Your Data no need Seperately
# st.header("📊 Analytics Dashboard")

# # Detect important columns

# sales_col = None
# profit_col = None
# region_col = None
# category_col = None
# product_col = None
# date_col = None

# for column in df.columns:

#     column_lower = column.lower()

#     if (
#         sales_col is None
#         and (
#             "sales" in column_lower
#             or "revenue" in column_lower
#         )
#     ):
#         sales_col = column

#     if (
#         profit_col is None
#         and "profit" in column_lower
#     ):
#         profit_col = column

#     if (
#         region_col is None
#         and "region" in column_lower
#     ):
#         region_col = column

#     if (
#         category_col is None
#         and "category" in column_lower
#     ):
#         category_col = column

#     if (
#         product_col is None
#         and "product" in column_lower
#     ):
#         product_col = column

#     if (
#         date_col is None
#         and (
#             "date" in column_lower
#             or "month" in column_lower
#             or "year" in column_lower
#         )
#     ):
#         date_col = column


# # --------------------------------------------------
# # SALES BY REGION
# # --------------------------------------------------

# if (
#     region_col is not None
#     and sales_col is not None
# ):

#     st.subheader("🌎 Sales by Region")

#     region_sales = (
#         df.groupby(region_col)[sales_col]
#         .sum()
#         .sort_values(ascending=False)
#     )

#     st.bar_chart(
#         region_sales
#     )


# # --------------------------------------------------
# # PROFIT BY CATEGORY
# # --------------------------------------------------

# if (
#     category_col is not None
#     and profit_col is not None
# ):

#     st.subheader("📦 Profit by Category")

#     category_profit = (
#         df.groupby(category_col)[profit_col]
#         .sum()
#         .sort_values(ascending=False)
#     )

#     st.bar_chart(
#         category_profit
#     )


# # --------------------------------------------------
# # TOP 10 PRODUCTS
# # --------------------------------------------------

# if (
#     product_col is not None
#     and sales_col is not None
# ):

#     st.subheader("🏆 Top 10 Products by Sales")

#     product_sales = (
#         df.groupby(product_col)[sales_col]
#         .sum()
#         .sort_values(ascending=False)
#         .head(10)
#     )

#     st.bar_chart(
#         product_sales
#     )


# # --------------------------------------------------
# # SALES VS PROFIT
# # --------------------------------------------------

# if (
#     sales_col is not None
#     and profit_col is not None
# ):

#     st.subheader("💰 Sales vs Profit")

#     comparison_data = df[
#         [sales_col, profit_col]
#     ].copy()

#     st.line_chart(
#         comparison_data
#     )


# # --------------------------------------------------
# # DATASET DATE TREND
# # --------------------------------------------------

# if date_col is not None:

#     try:

#         date_data = df.copy()

#         date_data[date_col] = pd.to_datetime(
#             date_data[date_col],
#             errors="coerce"
#         )

#         date_data = date_data.dropna(
#             subset=[date_col]
#         )

#         if sales_col is not None:

#             trend = (
#                 date_data
#                 .groupby(date_col)[sales_col]
#                 .sum()
#                 .sort_index()
#             )

#             st.subheader(
#                 "📈 Sales Trend Over Time"
#             )

#             st.line_chart(
#                 trend
#             )

#     except Exception:

#         pass
####################################################

# --------------------------------------------------
# 🧹 NATURAL LANGUAGE DATA CLEANING
# --------------------------------------------------

st.header("🧹 Natural Language Data Cleaning")

st.write(
    "Describe the cleaning operation you want "
    "to perform using natural language."
)

cleaning_instruction = st.text_input(
    "💬 What would you like to clean?",
    placeholder=(
        "Example: Fill missing values in Sales "
        "with the median"
    )
)

if st.button("🧹 Preview Cleaning"):

    if cleaning_instruction.strip():

        try:

            from ai_agent import generate_cleaning_action

            schema = "\n".join(
                [
                    f"{column}: {dtype}"
                    for column, dtype
                    in zip(
                        df.columns,
                        df.dtypes
                    )
                ]
            )

            with st.spinner(
                "🤖 Understanding your cleaning request..."
            ):

                action = asyncio.run(
                    generate_cleaning_action(
                        cleaning_instruction,
                        schema
                    )
                )

            st.session_state.pending_action = action

        except Exception as e:

            st.error(
                f"Unable to understand request: {e}"
            )


# --------------------------------------------------
# SHOW PENDING ACTION
# --------------------------------------------------

action = st.session_state.pending_action

if action:

    st.subheader("🔍 Cleaning Action")

    st.code(
        action
    )

    cleaned_preview = df.copy()

    preview_message = None

    # ----------------------------------------------
    # REMOVE DUPLICATES
    # ----------------------------------------------

    if action == "REMOVE_DUPLICATES":

        before = len(cleaned_preview)

        cleaned_preview = (
            cleaned_preview
            .drop_duplicates()
        )

        after = len(cleaned_preview)

        preview_message = (
            f"{before - after} duplicate rows "
            "will be removed."
        )

    # ----------------------------------------------
    # FILL MEDIAN
    # ----------------------------------------------

    elif action.startswith("FILL_MEDIAN|"):

        column = action.split("|", 1)[1]

        if column in cleaned_preview.columns:

            missing = (
                cleaned_preview[column]
                .isnull()
                .sum()
            )

            if pd.api.types.is_numeric_dtype(
                cleaned_preview[column]
            ):

                cleaned_preview[column] = (
                    cleaned_preview[column]
                    .fillna(
                        cleaned_preview[column]
                        .median()
                    )
                )

                preview_message = (
                    f"{missing} missing values in "
                    f"'{column}' will be filled "
                    "using the median."
                )

            else:

                st.error(
                    f"'{column}' is not numeric. "
                    "Median filling cannot be used."
                )

        else:

            st.error(
                f"Column '{column}' was not found."
            )

    # ----------------------------------------------
    # FILL MEAN
    # ----------------------------------------------

    elif action.startswith("FILL_MEAN|"):

        column = action.split("|", 1)[1]

        if column in cleaned_preview.columns:

            missing = (
                cleaned_preview[column]
                .isnull()
                .sum()
            )

            if pd.api.types.is_numeric_dtype(
                cleaned_preview[column]
            ):

                cleaned_preview[column] = (
                    cleaned_preview[column]
                    .fillna(
                        cleaned_preview[column]
                        .mean()
                    )
                )

                preview_message = (
                    f"{missing} missing values in "
                    f"'{column}' will be filled "
                    "using the mean."
                )

            else:

                st.error(
                    f"'{column}' is not numeric."
                )

        else:

            st.error(
                f"Column '{column}' was not found."
            )

    # ----------------------------------------------
    # FILL MODE
    # ----------------------------------------------

    elif action.startswith("FILL_MODE|"):

        column = action.split("|", 1)[1]

        if column in cleaned_preview.columns:

            missing = (
                cleaned_preview[column]
                .isnull()
                .sum()
            )

            mode_values = (
                cleaned_preview[column]
                .mode()
            )

            if not mode_values.empty:

                cleaned_preview[column] = (
                    cleaned_preview[column]
                    .fillna(
                        mode_values.iloc[0]
                    )
                )

                preview_message = (
                    f"{missing} missing values in "
                    f"'{column}' will be filled "
                    "using the mode."
                )

        else:

            st.error(
                f"Column '{column}' was not found."
            )

    # ----------------------------------------------
    # DROP MISSING
    # ----------------------------------------------

    elif action.startswith("DROP_MISSING|"):

        column = action.split("|", 1)[1]

        if column in cleaned_preview.columns:

            before = len(cleaned_preview)

            cleaned_preview = (
                cleaned_preview
                .dropna(
                    subset=[column]
                )
            )

            after = len(cleaned_preview)

            preview_message = (
                f"{before - after} rows containing "
                f"missing '{column}' values "
                "will be removed."
            )

        else:

            st.error(
                f"Column '{column}' was not found."
            )

    # ----------------------------------------------
    # DROP NEGATIVE
    # ----------------------------------------------

    elif action.startswith("DROP_NEGATIVE|"):

        column = action.split("|", 1)[1]

        if column in cleaned_preview.columns:

            before = len(cleaned_preview)

            cleaned_preview = cleaned_preview[
                cleaned_preview[column] >= 0
            ]

            after = len(cleaned_preview)

            preview_message = (
                f"{before - after} rows with "
                f"negative '{column}' values "
                "will be removed."
            )

        else:

            st.error(
                f"Column '{column}' was not found."
            )

    # ----------------------------------------------
    # CONVERT DATE
    # ----------------------------------------------

    elif action.startswith("CONVERT_DATE|"):

        column = action.split("|", 1)[1]

        if column in cleaned_preview.columns:

            cleaned_preview[column] = (
                pd.to_datetime(
                    cleaned_preview[column],
                    errors="coerce"
                )
            )

            preview_message = (
                f"'{column}' will be converted "
                "to datetime."
            )

        else:

            st.error(
                f"Column '{column}' was not found."
            )

    # ----------------------------------------------
    # REMOVE OUTLIERS
    # ----------------------------------------------

    elif action.startswith("REMOVE_OUTLIERS|"):

        column = action.split("|", 1)[1]

        if column in cleaned_preview.columns:

            if pd.api.types.is_numeric_dtype(
                cleaned_preview[column]
            ):

                Q1 = cleaned_preview[column].quantile(
                    0.25
                )

                Q3 = cleaned_preview[column].quantile(
                    0.75
                )

                IQR = Q3 - Q1

                lower = Q1 - 1.5 * IQR
                upper = Q3 + 1.5 * IQR

                before = len(cleaned_preview)

                cleaned_preview = cleaned_preview[
                    (
                        cleaned_preview[column]
                        >= lower
                    )
                    &
                    (
                        cleaned_preview[column]
                        <= upper
                    )
                ]

                after = len(cleaned_preview)

                preview_message = (
                    f"{before - after} potential "
                    f"outlier rows in '{column}' "
                    "will be removed."
                )

            else:

                st.error(
                    f"'{column}' is not numeric."
                )

        else:

            st.error(
                f"Column '{column}' was not found."
            )

    elif action == "INVALID":

        st.warning(
            "The requested operation could not "
            "be safely interpreted."
        )

    else:

        st.warning(
            "Unsupported cleaning operation."
        )


    # ----------------------------------------------
    # PREVIEW MESSAGE
    # ----------------------------------------------

    if preview_message:

        st.info(
            f"🔍 Preview: {preview_message}"
        )

        st.subheader(
            "👀 Preview of Cleaned Dataset"
        )

        st.dataframe(
            cleaned_preview.head(10),
            use_container_width=True
        )

        # ------------------------------------------
        # APPLY BUTTON
        # ------------------------------------------

        if st.button(
            "✅ Apply Cleaning",
            type="primary"
        ):

            st.session_state.cleaned_df = (
                cleaned_preview.copy()
            )

            st.session_state.pending_action = None

            st.success(
                "✅ Cleaning operation applied successfully!"
            )

            st.rerun()


# --------------------------------------------------
# SHOW CURRENT DATASET
# --------------------------------------------------

if st.session_state.cleaned_df is not None:

    st.subheader(
        "📋 Current Dataset After Cleaning"
    )

    st.dataframe(
        st.session_state.cleaned_df.head(10),
        use_container_width=True
    )

    # ----------------------------------------------
    # DOWNLOAD CLEANED DATASET
    # ----------------------------------------------

    cleaned_csv = (
        st.session_state.cleaned_df
        .to_csv(index=False)
        .encode("utf-8")
    )

    st.download_button(
        label="📥 Download Cleaned Dataset",
        data=cleaned_csv,
        file_name="cleaned_dataset.csv",
        mime="text/csv"
    )

    # ----------------------------------------------
    # RESTORE ORIGINAL
    # ----------------------------------------------

    if st.button(
        "↩️ Restore Original Dataset"
    ):

        st.session_state.cleaned_df = (
            st.session_state.original_df.copy()
        )

        st.session_state.pending_action = None

        st.success(
            "↩️ Original dataset restored."
        )

        st.rerun()
# --------------------------------------------------
# 🤖 AI DATA ANALYST
# --------------------------------------------------

st.header("🤖 Ask Your Data")

st.write(
    "Ask a question about your uploaded dataset "
    "using natural language."
)

user_question = st.text_input(
    "💬 What would you like to know?",
    placeholder="Example: Which region has the highest profit?"
)

if st.button("🧠 Analyze My Data"):

    if user_question.strip():

        try:

            # ------------------------------------------
            # CREATE SQLITE DATABASE
            # ------------------------------------------

            connection = sqlite3.connect(":memory:")

            df.to_sql(
                "sales_data",
                connection,
                index=False,
                if_exists="replace"
            )

            # ------------------------------------------
            # CREATE DATASET SCHEMA
            # ------------------------------------------

            schema = "\n".join(
                [
                    f"{column}: {dtype}"
                    for column, dtype
                    in zip(df.columns, df.dtypes)
                ]
            )

            # ------------------------------------------
            # GENERATE SQL USING AI
            # ------------------------------------------

            with st.spinner(
                "🤖 AI is analyzing your question..."
            ):

                from ai_agent import generate_sql

                sql_query = asyncio.run(
                    generate_sql(
                        user_question,
                        schema
                    )
                )

            # ------------------------------------------
            # DISPLAY GENERATED SQL
            # ------------------------------------------

            st.subheader("🧠 Generated SQL")

            st.code(
                sql_query,
                language="sql"
            )

            # ------------------------------------------
            # EXECUTE SQL
            # ------------------------------------------

            result = pd.read_sql_query(
                sql_query,
                connection
            )

            # ------------------------------------------
            # DISPLAY RESULT
            # ------------------------------------------

            st.subheader("📊 Analysis Result")

            st.dataframe(
                result,
                use_container_width=True
            )
            # ------------------------------------------
            # AI BUSINESS INSIGHT
            # ------------------------------------------

            st.subheader("💡 AI Business Insight")

            try:

                from ai_agent import generate_insight

                with st.spinner(
                    "🧠 Generating business insight..."
                ):

                    insight = asyncio.run(
                        generate_insight(
                            user_question,
                            sql_query,
                            result.to_string(index=False)
                        )
                    )

                st.info(insight)

            except Exception as e:

                st.warning(
                    f"Unable to generate business insight: {e}"
                )

            # ------------------------------------------
            # AUTOMATIC VISUALIZATION
            # ------------------------------------------

            st.subheader("📈 Visualization")

            if not result.empty:

                numeric_columns = result.select_dtypes(
                include="number"
            ).columns.tolist()

            categorical_columns = result.select_dtypes(
                exclude="number"
            ).columns.tolist()

            if (
                len(categorical_columns) >= 1
                and len(numeric_columns) >= 1
            ):

                x_column = categorical_columns[0]
                y_column = numeric_columns[0]

                chart_data = result[
                    [x_column, y_column]
                ].copy()

                chart_data = chart_data.set_index(
                    x_column
                )

                st.bar_chart(
                    chart_data
                )

            elif len(numeric_columns) >= 2:

                st.line_chart(
                    result[numeric_columns]
                )

            elif len(numeric_columns) == 1:

                st.line_chart(
                    result[numeric_columns]
                )

            else:

                st.info(
                    "No suitable numeric data was found "
                    "for automatic visualization."
                )

            # ------------------------------------------
            # CLOSE DATABASE
            # ------------------------------------------

            connection.close()

        except Exception as e:

            st.error(
                f"❌ Unable to analyze the question: {e}"
            )

    else:

        st.warning(
            "Please enter a question first."
        )