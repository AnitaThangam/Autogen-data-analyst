import asyncio

from ai_agent import create_ai_agent


async def main():

    agent, model_client = create_ai_agent()

    print("🤖 Testing Groq AI...")

    result = await agent.run(
        task="""
Explain what a data analyst does in one sentence.
"""
    )

    print("\nAI Response:")
    print(result.messages[-1].content)

    await model_client.close()


asyncio.run(main())