from dotenv import load_dotenv
import os


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



if __name__ == "__main__":


