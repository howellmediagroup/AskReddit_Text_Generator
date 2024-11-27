# main.py
from reddit import get_data_from_link
import logging
import json
import sys
import os

logging.basicConfig(filename='app.log', level=logging.INFO, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

def load_config():
    config_path = 'config.json'
    if not os.path.exists(config_path):
        raise FileNotFoundError("config.json file not found. Please ensure it is in the project root directory.")
    with open(config_path) as f:
        return json.load(f)

def save_to_txt(post_data):
    # Create a .txt file named after the Reddit post
    filename = f"{post_data['name']}.txt"
    output_path = os.path.join(os.getcwd(), filename)
    with open(output_path, 'w') as file:
        # Write the post title
        file.write(f"{post_data['content']}\n\n")
        # Write the top comments
        for i, comment in enumerate(post_data['comments'], start=1):
            file.write(f"{i}. {comment['content']}\n\n")
    print(f"Data saved to {output_path}")

def main():
    try:
        # Check if praw and dotenv are installed
        try:
            import praw
            from dotenv import load_dotenv
        except ModuleNotFoundError as e:
            missing_module = e.name
            print(f"The '{missing_module}' module is not installed. Please install it by running: pip install {missing_module}")
            sys.exit(1)
        
        # Ask user for Reddit post URL
        post_url = input("Please enter the Reddit post URL: ").strip()
        
        # Load other configuration parameters
        config = load_config()
        comment_limit = config.get("comment_limit", 20)
        max_char = config.get("max_char", 300)
        min_char = config.get("min_char", 45)

        # Fetch data from reddit
        post = get_data_from_link(post_url, comment_limit=comment_limit, max_char=max_char, min_char=min_char)

        # Save the data to a .txt file
        save_to_txt(post)
        
    except Exception as e:
        logging.error(f"Error fetching data from Reddit: {e}")
        print(f"Error fetching data from Reddit: {e}")

if __name__ == "__main__":
    main()
    print("COMPLETE")
