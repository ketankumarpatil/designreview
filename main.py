from langchain_openai import AzureChatOpenAI

from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph


# Define review result class for each reviewer
# class review_result(BaseModel):
#    result: bool = Field(description="result of the review")
#    comments: list[str] = Field(description="comments on the review")


# Define langgraph state class
class State(BaseModel):
    query: str = Field(description="online processing document")
    current_role: str = Field(description="current role which is selected")
    current_review_result: bool = Field(description="current judge result")


model = AzureChatOpenAI(azure_deployment="gpt-4o", api_version="2024-08-01-preview")

workflow = StateGraph(State)


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant。"),
        ("human", "{input}"),
    ]
)

output_parser = StrOutputParser()
chain = prompt | model | output_parser
output = chain.invoke({"input": "hello"})
print(output)
