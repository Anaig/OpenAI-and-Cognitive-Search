"""Modules import."""
import os
import json
import logging
import openai
import azure.functions as func

# Prompt to be sent to Azure OpenAI
OPENAI_PROMPT = "Summarize the following text in 3 sentences:"

def main(req: func.HttpRequest) -> func.HttpResponse:
    """Get text from Cognitive Search and return OpenAI completion"""

    logging.info('Python HTTP trigger function processed a request.')

    # Extract text from request payload
    req_body = req.get_body().decode('utf-8')
    request = json.loads(req_body)
    text = request['values'][0]['data']['text']

    # Get OpenAI summary
    summary = get_summary(text)

    # Create the response object
    response_body = {
        "values": [
            {
                "recordId": request['values'][0]['recordId'],
                "data": {
                    "summary": summary
                },
                "errors": None,
                "warnings": None
            }
        ]
    }

    # Serialize the response object to JSON and return it
    response = func.HttpResponse(json.dumps(response_body))
    response.headers['Content-Type'] = 'application/json'
    return response


# Get an OpenAI summary
def get_summary(text):
    """Send a prompt to Azure OpenAI"""

    openai.api_type = "azure"
    openai.api_base = "https://anaigopenai.openai.azure.com/"
    openai.api_version = "2022-12-01"
    openai.api_key = os.environ["AZURE_OPENAI_SECRET"]

    response = openai.Completion.create(
    engine = os.environ["OPENAI_ENGINE"],
    prompt = f'{OPENAI_PROMPT} {text}',
    temperature = 0.5,
    max_tokens = 500,
    top_p = 1,
    frequency_penalty = 0,
    presence_penalty = 0,
    best_of = 1,
    stop = None)

    if response.object == 'text_completion':
        if response['choices'][0]['finish_reason'] == 'stop':
            category = response['choices'][0]['text']
        else:
            category = None
    else:
        category = None

    return category
