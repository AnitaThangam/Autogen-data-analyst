import asyncio

from ai_agent import create_ai_agent


async def main():

    agent, model_client = create_ai_agent()

    print("🤖 AI Data Analyst is ready!")

    result = await agent.run(
        task="""
You are analyzing a sales dataset.

The table is called sales_data.

Some columns are:
Region
Category
Sales
Profit
Product

User question:

Which region has the highest profit?

Write an SQL query that can answer this question.
"""
    )

    print("\nAI Response:")
    print(result.messages[-1].content)

    await model_client.close()


asyncio.run(main())