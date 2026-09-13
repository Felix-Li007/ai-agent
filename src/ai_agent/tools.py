from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.tools import Tool
from datetime import datetime


def save_to_file(data: str, filename: str = "research_oputput.txt"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    formated_text=f"--- Research Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"
    with open(filename, "a", encoding="utf-8") as f:
        f.write(formated_text)
    return f"Data saved to {filename}"

save_tool = Tool(
    name="save_to_file",
    func=save_to_file,
    description="Save the research output to a text file. Input: a string of data to save.",
)

search = DuckDuckGoSearchRun()
search_tool = Tool(
    name="duckduckgo_search",
    func=lambda query: search.run(query),
    description="Search the web for current information. Input: a search query.",
)

api_wrapper = WikipediaAPIWrapper(top_k_results=1,doc_content_chars_max=10)
wiki_tool=WikipediaQueryRun(api_wrapper=api_wrapper)