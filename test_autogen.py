import os
import asyncio

from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv()


async def main():

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("❌ API key was not found.")
        return

    print("✅ API key found.")

    model_client = OpenAIChatCompletionClient(
        model="gpt-4.1-nano",
        api_key=api_key
    )

    agent = AssistantAgent(
        name="data_analyst",
        model_client=model_client,
        system_message=(
            "You are a professional data analyst. "
            "Give clear and concise answers."
        )
    )

    print("🤖 Sending test question to AI...")

    result = await agent.run(
        task="Explain what a data analyst does in one sentence."
    )

    print("\nAI Response:")
    print(result.messages[-1].content)

    await model_client.close()


asyncio.run(main())