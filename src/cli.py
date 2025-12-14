import os
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from dotenv import load_dotenv, find_dotenv
from langgraph.prebuilt import create_react_agent
import asyncio
from langchain_sandbox import PyodideSandboxTool

# Load environment variables
load_dotenv(find_dotenv())

# Load model and sandbox tool
model_name = "Qwen/Qwen2.5-7B-Instruct"
llm = HuggingFaceEndpoint(
    repo_id=model_name,
    max_new_tokens=128,
    temperature=0.7,
    huggingfacehub_api_token=os.environ["HUGGINGFACEHUB_API_TOKEN"],
    provider="together"
)
chat_model = ChatHuggingFace(llm=llm, verbose=True)

sandbox_tool = PyodideSandboxTool(
    # Allow Pyodide to install python packages that
    # might be required.
    allow_net=True,
)

# Create ReAct agent with the chat model and sandbox tool
agent = create_react_agent(chat_model, [sandbox_tool])

async def main():
    user_input = input("Enter code to fix: ")
    while user_input != "exit":
        output = await agent.ainvoke(
            {"messages": [{"role": "user", "content": "Return just fixed code without any introductions and conclusions. Fix this code: " + user_input}]},
            config={"configurable": {"thread_id": "123"}},
        )
        print(output["messages"][-1].content)
        user_input = input("Enter: ")

if __name__ == "__main__":
    asyncio.run(main())