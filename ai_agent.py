import os

from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient


load_dotenv()


def create_ai_agent():

    groq_api_key = os.getenv("GROQ_API_KEY")

    if not groq_api_key:
        raise ValueError(
            "GROQ_API_KEY was not found in the .env file."
        )

    model_client = OpenAIChatCompletionClient(

        model="llama-3.3-70b-versatile",

        base_url="https://api.groq.com/openai/v1",

        api_key=groq_api_key,

        model_info={
            "vision": False,
            "function_calling": False,
            "json_output": False,
            "family": "unknown",
            "structured_output": False,
        },
    )

    agent = AssistantAgent(

        name="data_analyst",

        model_client=model_client,

        system_message="""
You are an expert Data Analyst.

Your job is to convert business questions into SQLite SQL queries.

The database contains one table:

sales_data

Only use columns that are provided in the dataset schema.

Return ONLY the SQL query.

Do not explain the query.

Do not use markdown code blocks.

Do not invent columns.
"""
    )

    return agent, model_client


async def generate_sql(question, schema):

    agent, model_client = create_ai_agent()

    prompt = f"""

Database table:

sales_data


Available columns:

{schema}


User question:

{question}


Generate a SQLite SQL query that answers the user's question.

Return ONLY the SQL query.

"""

    result = await agent.run(
        task=prompt
    )

    response = result.messages[-1].content

    await model_client.close()

    response = response.replace(
        "```sql",
        ""
    )

    response = response.replace(
        "```",
        ""
    )

    return response.strip()

async def generate_insight(question, sql_query, result):

    agent, model_client = create_ai_agent()

    prompt = f"""
You are a professional business data analyst.

A user asked:

{question}

The SQL query used was:

{sql_query}

The SQL result was:

{result}

Analyze the result and provide a concise business insight.

Your response should:

1. Clearly state the main finding.
2. Mention important numbers when available.
3. Explain what the finding could mean for the business.
4. Avoid making unsupported assumptions.
5. Keep the answer within 3-5 sentences.

Do not provide SQL code.
"""

    response = await agent.run(
        task=prompt
    )

    insight = response.messages[-1].content

    await model_client.close()

    return insight.strip()

async def generate_cleaning_action(
    instruction,
    schema
):

    agent, model_client = create_ai_agent()

    prompt = f"""
You are an expert data-cleaning assistant.

The user has uploaded a dataset called sales_data.

Dataset schema:

{schema}

The user wants to perform this cleaning operation:

{instruction}

Determine the appropriate pandas operation.

Return ONLY ONE of these action formats:

REMOVE_DUPLICATES

FILL_MEDIAN|COLUMN_NAME

FILL_MEAN|COLUMN_NAME

FILL_MODE|COLUMN_NAME

DROP_MISSING|COLUMN_NAME

DROP_NEGATIVE|COLUMN_NAME

CONVERT_DATE|COLUMN_NAME

REMOVE_OUTLIERS|COLUMN_NAME

If the requested operation is not possible,
return:

INVALID

Do not provide explanations.
Do not use markdown.
"""

    result = await agent.run(
        task=prompt
    )

    response = result.messages[-1].content

    await model_client.close()

    return response.strip()