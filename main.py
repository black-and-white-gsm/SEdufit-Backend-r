import requests
from langchain_community.chat_models import ChatPerplexity
from langchain_core.prompts import ChatPromptTemplate

api_key = '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'
model='llama-3.1-sonar-small-128k-online'
chat = ChatPerplexity(pplx_api_key=api_key, model=model)


def perplexity_chat(message):
    prompt = ChatPromptTemplate.from_messages([
        ('system', '한국어로 대답해줘'),
        ('human', message)
    ])

    chain = prompt | chat

    response = chain.invoke({'question': message})
    return response.content


def lambda_handler(event, context):
    text_input = event['text_input']
    callback_url = event['callback_url']

    result = perplexity_chat(text_input)
    print(result)
    requests.post(
        callback_url,
        json={
            'version': '2.0',
            'useCallback': False,
            'template': {'outputs': [{'simpleText': {'text': f'{result}'}}]}
        }
    )

    return True
