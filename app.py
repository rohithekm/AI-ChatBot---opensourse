import chainlit as cl
from model import pipeline


@cl.on_chat_start
async def main2():
    result = pipeline.run(query="hi")
    response = result["answer"]
    await cl.Message(content=response).send()

@cl.on_message
async def main(message: str):
    try:
        result = pipeline.run(query=message)
        response = result["answer"]
    except Exception as e:
        response = f"An error occurred: {str(e)}"

    await cl.Message(content=response).send()