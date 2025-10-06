import os
from browser_use import Agent, ChatOpenAI, ChatGoogle
agent = Agent(
	task='Find founders of browser-use',
    llm = ChatOpenAI(
	model='qwen3-coder-plus',
	base_url='https://dashscope.aliyuncs.com/compatible-mode/v1',
	api_key='sk-8508018f80764e6c94dba9fb77f51287'
)
    # llm=ChatGoogle(model='gemini-2.5-flash',api_key=os.getenv("GOOGLE_API_KEY")),
)

agent.run_sync()
