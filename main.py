from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI

def check_api_key():
    load_dotenv()
    try:
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found")
        return api_key
    except Exception as e:
        print(f"Error: {e}")
        return None

#Instantiation
def llm_instance():

    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0,
        # max_tokens=None,
        timeout=300,
    )
    return llm

if __name__ == "__main__":
    api_key = check_api_key()
    if api_key:
        print("API Key successfully loaded.")
        llm = llm_instance()
        print("LLM instance created.")

        #Invocation
        messages = [
            (
                "system",
                "You are a helpful assistant,answer and guide the user.",
            ),
            ("human", "who is the president of the united states?"),
        ]
        ai_msg = llm.invoke(messages)
        ai_msg
        print(ai_msg.text)