import asyncio
import base64
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from dotenv import load_dotenv

load_dotenv()
from browser_use import Agent, Browser, ChatGoogle, Tools
from browser_use.agent.views import ActionResult
from browser_use.llm import ChatOpenAI

# Initialize tools
tools = Tools()

PNG_IMAGE_PATH = "/Users/zhangyibo/vscodeProject/browser-use/examples/product.png"

@tools.action('Read a PNG file and return its base64 content wrapped in <content> tags.')
async def read_png_base64(path: str, available_file_paths: list[str]) -> ActionResult:
	if path not in available_file_paths:
		return ActionResult(error=f'File path {path} is not available.')
	if not os.path.exists(path):
		return ActionResult(error=f'File {path} does not exist.')
	if not path.lower().endswith('.png'):
		return ActionResult(error=f'File {path} is not a PNG image.')
	try:
		with open(path, 'rb') as file:
			encoded = base64.b64encode(file.read()).decode('ascii')
	except Exception as e:
		return ActionResult(error=f'Failed to read PNG file: {e}')
	content = f'Read from PNG {path}.\n<content>\n{encoded}\n</content>'
	return ActionResult(
		extracted_content=content,
		long_term_memory=content,
		include_extracted_content_only_once=True,
	)


browser = Browser(
	storage_state="/Users/zhangyibo/vscodeProject/browser-use/examples/state-store2.json",
	headless=True
)
llm = ChatOpenAI(
	model='qwen3-coder-plus',
	base_url='https://dashscope.aliyuncs.com/compatible-mode/v1',
	api_key='sk-8508018f80764e6c94dba9fb77f51287',
)


async def main():
	agent = Agent(
		save_conversation_path="./history.json",
		llm = llm,
		# llm = ChatGoogle(model='gemini-2.5-flash'),
		available_file_paths=[PNG_IMAGE_PATH],
		task = f"""
		你可以访问以下图片文件：{PNG_IMAGE_PATH}。
		1. 调用 read_png_base64 工具，参数 path='{PNG_IMAGE_PATH}'，获取图片的 base64 数据。
		2. 观察工具返回的 <content> 块，描述图片中包含的主要信息。
		如果有必要，可以提出进一步分析这张图片的建议。
    """,
		browser=browser,
	)
	await agent.run()
# 访问页面：https://item.upload.taobao.com/sell/v2/publish.htm?catId=121464023
# 		我需要你帮我操作。依照以下的步骤
# 		1.找到页面中的‘宝贝详情’位置，
# 		2.点击'图片'按钮，会弹出图片选择框
# 		3.在图片选择框中，搜索‘980346355‘文件夹，并选择该文件夹下的’desc‘文件夹
# 		4.按文件名升序排序
# 		5.依次选择文件夹内的全部图片，每次点击间隔0.5s
# 		6.勾选完成后会出现确认按钮，点击
# 		7.检查图片是否正确选择

if __name__ == '__main__':
	asyncio.run(main())
