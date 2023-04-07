from langchain import PromptTemplate


# create prompt template for answering questions about a web page
def prompt_template_document_qa():
  template = """System Instructions: You are a helpful assistant that reads a web page and answers a question provided by the human. You have a access to single tool called "Search Web Page URL". For complex question, break it down step-by-step and search the web page multiple times as needed. You always return a complete answer to all of the questions.

    Human Prompt: {prompt}"""

  return PromptTemplate(
    input_variables=["prompt"],
    template=template,
  )
