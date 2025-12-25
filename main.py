from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI

def check_api_key():
    """Load and verify the OpenAI API key from environment variables."""
    load_dotenv()
    try:
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found")
        return api_key
    except Exception as e:
        print(f"Error: {e}")
        return None

def llm_instance(model="gpt-3.5-turbo", temperature=0, timeout=300):
    """Create and return a ChatOpenAI instance with custom parameters."""
    llm = ChatOpenAI(
        model=model,
        temperature=temperature,
        timeout=timeout,
    )
    return llm

def get_ai_response(user_message, model="gpt-3.5-turbo", temperature=0, timeout=300, 
                    system_prompt="You are a helpful assistant, answer and guide the user."):
    """
    Get AI response for a user message.
    
    Args:
        user_message (str): The user's question or input
        model (str): The OpenAI model to use
        temperature (float): Temperature setting for randomness
        timeout (int): Timeout in seconds
        system_prompt (str): The system prompt for the AI
        
    Returns:
        str: The AI's response or error message
    """
    try:
        llm = llm_instance(model=model, temperature=temperature, timeout=timeout)
        messages = [
            ("system", system_prompt),
            ("human", user_message),
        ]
        ai_msg = llm.invoke(messages)
        return ai_msg.content
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    # Test the functions
    api_key = check_api_key()
    if api_key:
        print("API Key successfully loaded.")
        response = get_ai_response("Who is the president of the United States?")
        print(response)