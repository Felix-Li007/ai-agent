from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openrouter import ChatOpenRouter
from pydantic import BaseModel
from ai_agent.tools import search_tool,wiki_tool,save_tool


class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]


load_dotenv()
llm = ChatOpenRouter(
    model="deepseek/deepseek-v4-flash", temperature=0.7, max_tokens=1000
)
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

system_prompt = (
    "You are a research assistant that provides summaries of topics with sources "
    "and tools used. Only list sources you can identify reliably. "
    "No tools are available, so return an empty list for tools_used. "
    "Return only JSON using this format:\n"
    + parser.get_format_instructions()
)

tools = [search_tool,wiki_tool,save_tool]  # Add any additional tools you want to include here
agent = create_agent(
    model=llm,
    system_prompt=system_prompt,
    tools=tools,
)

query=input("Enter your research query: ")
try:
    raw_response = agent.invoke({
        "messages": [{"role": "user", "content": query}]
    })
    structured_response = parser.invoke(raw_response["messages"][-1])
    print(structured_response.model_dump_json(indent=2))
except Exception as e:
    print("Error parsing response:", e,"Raw response:", raw_response)
