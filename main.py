import os
from dotenv import load_dotenv

def main():
    # Load environment variables from .env file
    load_dotenv()
    
    # Example of using environment variable
    secret_key = os.getenv('SECRET_KEY', 'default_secret')
    print(f"Hello from github-copilot-thought-diary-app!")
    print(f"Secret key loaded: {secret_key}")


if __name__ == "__main__":
    main()
