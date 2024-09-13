from haystack.pipelines import Pipeline
from haystack.nodes import BaseComponent
from groq import Groq
import os
from chainlit.message import Message

class GroqConversationalAgent(BaseComponent):
    outgoing_edges = 1

    def __init__(self, api_key: str):
        super().__init__()
        self.client = Groq(api_key=api_key)

    def run(self, query, **kwargs):
        print(type(query))
        if isinstance(query, Message):
            queryContent = query.content
        else:
            queryContent = query
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": """You are an knowledgeable chat assistant named 'Maximus.01' designed to assist users in learning and studies. Your responses should be related to studies. If the user qurey is not related to studies please respond "Ask anything related to learning.".Donot respond to quries that is harmful and appropriate for a student. 
                                                     Start the conversation by asking question and give ideas related to there answers.
                                                     Always answer in short but it should be simple to understand and try to understand the user needs. Provide a clear and concise conclusion based on the answers to the five questions we've covered.
                                                     """},
                    {"role": "user", "content": queryContent},
                ],
                model="llama3-70b-8192",
            )
            answer = response.choices[0].message.content
        except Exception as e:
            answer = f"Error: {str(e)}"
        return {"answer": answer}, "output_1"

    def run_batch(self, queries, **kwargs):
        pass

# initilize the key    
groq_agent = GroqConversationalAgent(api_key="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")

#haystack pipeline
pipeline = Pipeline()
pipeline.add_node(component=groq_agent, name="GroqAgent", inputs=["Query"])
