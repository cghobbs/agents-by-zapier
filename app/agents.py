from langchain.llms import OpenAI
from langchain.agents import initialize_agent


def run_agent(prompt,
              tools,
              temperature=0,
              agent="zero-shot-react-description"):
  llm = OpenAI(temperature=temperature)
  agent = initialize_agent(tools, llm, agent=agent, verbose=True)
  return agent.run(prompt)
