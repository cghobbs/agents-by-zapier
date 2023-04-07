import os, uuid

from flask import Flask, request, jsonify

from app.request_validator import validate_request
from app.prompts import prompt_template_document_qa
from app.tools import doc_search_tools, nla_tools
from app.agents import run_agent

open_api_key = os.environ['OPENAI_API_KEY']
zapier_nla_api_key = os.environ['ZAPIER_NLA_API_KEY']

app = Flask(__name__)


@app.route('/')
def home():
  return "Agents by Zapier"


@app.route('/actions', methods=['POST'])
def actions():
  """
  Handle POST requests to the '/actions' endpoint where a natural language prompt is provided. 
  An agent will be run to perform the necessary set of actions based on the natural language prompt.
  
  The request data must contain a 'prompt' key with the user input as its value. The endpoint 
  returns the agent's response along with a unique ID.

  :return: A JSON response containing a unique ID and the agent's response. If the request data is 
  invalid, an error message is returned with a 400 status code.
  """

  # Validate the request data
  success, data, error = validate_request(request=request,
                                          required_keys=['prompt'])
  if not success:
    return jsonify(error), 400

  # create the prompt directly from user input
  prompt = data['prompt']

  # create the tools
  tools = nla_tools()

  # run the agent
  response = run_agent(prompt, tools)

  # run the agent and return the response
  return jsonify({"id": f"actn-{uuid.uuid4()}", "response": response}), 200


@app.route('/document_qa', methods=['POST'])
def document_qa():
  """
  Handle POST requests to the '/document_qa' endpoint where URL and natural language prompt are 
  provided. An agent will use it's document search tool to aid it in answering any number of questions
  based on the natural language prompt.
  
  The request data must contain a 'url and 'prompt' key with a valid url. The endpoint returns the 
  agent's response along with a unique ID.

  :return: A JSON response containing a unique ID and the agent's response. If the request data is 
  invalid, an error message is returned with a 400 status code.
  """

  # Validate the request data
  success, data, error = validate_request(request=request,
                                          required_keys=['prompt', 'url'],
                                          url_keys=['url'])
  if not success:
    return jsonify(error), 400

  # create the prompt
  prompt_template = prompt_template_document_qa()
  prompt = prompt_template.format(prompt=data['prompt'])

  # create the tool
  tools = doc_search_tools(data['url'])

  # run agent
  response = run_agent(prompt, tools)

  return jsonify([{"id": f"dqa-{uuid.uuid4()}", "response": response}]), 200


@app.route('/tools')
def actions_list_tools():
  """
  Handle requests to the '/tools' endpoint. Provides a list of available actions when using the 
  '/actions' endpoint.

  :return: A JSON response containing a unique ID and the list of available tools.
  """

  tools = nla_tools()
  tool_names = [tool.name for tool in tools]

  return jsonify({"id": f"tls-{uuid.uuid4()}", "tool_names": tool_names}), 200


app.run(host='0.0.0.0', port=8080)
