"""
Simple try of the agent.

@dev You need to add OPENAI_API_KEY to your environment variables.
"""

import asyncio
import os

from dotenv import load_dotenv

from browser_use import Agent, ChatOpenAI

load_dotenv()

# All the models are type safe from OpenAI in case you need a list of supported models
llm = ChatOpenAI(
	model='deepseek/deepseek-chat-v3.1:free',
	base_url='https://openrouter.ai/api/v1',
	api_key='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',
)
agent = Agent(
	task='Go to example.com, click on the first link, and give me the title of the page',
	llm=llm,
)


async def main():
	await agent.run(max_steps=10)
	input('Press Enter to continue...')


asyncio.run(main())
