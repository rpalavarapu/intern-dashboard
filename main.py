from dotenv import load_dotenv
import os

load_dotenv() 

# Configurations
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')  # access token
headers = {"PRIVATE-TOKEN": ACCESS_TOKEN} # headers

def main():
    # add methods based on case
    pass

if __name__ == "__main__":
    main()