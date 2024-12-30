from dotenv import load_dotenv
import os
load_dotenv()
print(f"env key value{os.environ['API_KEY']}")