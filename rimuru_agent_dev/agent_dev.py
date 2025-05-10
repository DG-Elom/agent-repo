from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI
from langchain.chains.conversation.memory import ConversationBufferMemory
import os

llm = OpenAI(temperature=0)
memory = ConversationBufferMemory(memory_key="chat_history")

def run_test(code: str):
    with open("temp_test.py", "w") as f:
        f.write(code)
    result = os.popen("pytest temp_test.py").read()
    return result

tools = [
    Tool(
        name="PyTest Runner",
        func=run_test,
        description="Exécute des tests Pytest depuis une string Python"
    )
]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent="chat-conversational-react-description",
    memory=memory
)

if __name__ == "__main__":
    question = "Voici un test Pytest à exécuter : ..."
    print(agent.run(question))