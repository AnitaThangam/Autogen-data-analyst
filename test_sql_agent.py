import asyncio
import sqlite3
import pandas as pd

from ai_agent import generate_sql


async def main():

    # -----------------------------------------
    # LOAD DATASET
    # -----------------------------------------

    df = pd.read_csv("sales_data.csv")

    # -----------------------------------------
    # CREATE SQLITE DATABASE
    # -----------------------------------------

    connection = sqlite3.connect(":memory:")

    df.to_sql(
        "sales_data",
        connection,
        index=False,
        if_exists="replace"
    )

    # -----------------------------------------
    # CREATE SCHEMA
    # -----------------------------------------

    schema = "\n".join(
        [
            f"{column}: {dtype}"
            for column, dtype
            in zip(df.columns, df.dtypes)
        ]
    )

    print("\n📋 Dataset Schema:")
    print(schema)

    # -----------------------------------------
    # USER QUESTION
    # -----------------------------------------

    question = input(
        "\n🤖 Ask your data analyst a question: "
    )

    # -----------------------------------------
    # GENERATE SQL
    # -----------------------------------------

    print("\n🧠 Generating SQL...")

    sql_query = await generate_sql(
        question,
        schema
    )

    print("\nGenerated SQL:")
    print(sql_query)

    # -----------------------------------------
    # EXECUTE SQL
    # -----------------------------------------

    try:

        result = pd.read_sql_query(
            sql_query,
            connection
        )

        print("\n📊 SQL Result:")
        print(result)

    except Exception as e:

        print("\n❌ SQL Error:")
        print(e)

    connection.close()


asyncio.run(main())