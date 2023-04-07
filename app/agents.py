from langchain import LLMChain, OpenAI, PromptTemplate
from langchain.agents import initialize_agent


def run_agent(prompt,
              tools,
              temperature=0,
              agent="zero-shot-react-description"):
  llm = OpenAI(temperature=temperature)
  agent = initialize_agent(tools, llm, agent=agent, verbose=True)
  return agent.run(prompt)


def run_custom_agent(prompt, tools, temperature=0):
  llm = OpenAI(temperature=temperature)

  template = """You are an expert in Zapier automation. 
  
Step 1: Break the following workflow down into the fewest possible discrete actions required. Workflow Description: 

{workflow}

Step 2: In addition to your own reasoning and the context provided in the workflow description, you also have access to these tools. 

- Google Calendar: Create Detailed Event
- Gmail: Send Email
- Todoist: Create a Task

Do you have have everything you need to complete the workflow? If yes, then print out the workflow. If no, then don't share the workflow but instead describe the missing tools. Begin!
"""

  prompt_template = PromptTemplate(template=template,
                                   input_variables=["workflow"])

  llm_chain = LLMChain(prompt=prompt_template, llm=llm, verbose=True)

  return llm_chain.predict(workflow=prompt)
