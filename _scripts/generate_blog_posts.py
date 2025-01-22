import requests
import yaml
import os
import time
from datetime import datetime

# Define the API endpoint
url = "https://api.mistral.ai/v1/agents/completions"

# Set up the headers with the API key
headers = {
    "Authorization": f"Bearer API_KEY",  # Replace with your API key
    "Content-Type": "application/json"
}

def generate_blog_post(title, lang):    
    # Define the JSON payload
    payload = {
        "messages": [
            {
                "role": "user",
                "content": f'Generate the blog post with this title "{title}"'
            }
        ],
        "response_format": {
            "type": "text"
        },
        "agent_id": "ag:cdcf0af0:20250108:researca-blog-post-generation:0bf202b5"
    }

    # Make the POST request
    response = requests.post(url, headers=headers, json=payload)
    # Output the response
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        print(f"Error: {response.status_code}, {response.text}, contact telary support, this is not normal")

def translate_title(title, lang):    
    # Define the JSON payload
    payload = {
        "messages": [
            {
                "role": "user",
                "content": f'Translate "{title}"'
            }
        ],
        "response_format": {
            "type": "text"
        },
        "agent_id": "ag:cdcf0af0:20250108:researca-generate-title:f290d77f"
    }

    # Make the POST request
    response = requests.post(url, headers=headers, json=payload)
    # Output the response
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        print(f"Error: {response.status_code}, {response.text}, contact telary support, this is not normal")

def translate_slug(title, lang):    
    # Define the JSON payload
    payload = {
        "messages": [
            {
                "role": "user",
                "content": f'Generate the slug for "{title}"'
            }
        ],
        "response_format": {
            "type": "text"
        },
        "agent_id": "ag:cdcf0af0:20250108:researca-generate-slug:852db32e"
    }

    # Make the POST request
    response = requests.post(url, headers=headers, json=payload)
    # Output the response
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        print(f"Error: {response.status_code}, {response.text}, contact telary support, this is not normal")

def __main__():
    # assign directory
    directory = '_posts_metadata'
 
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f) and f != ".gitkeep":
            with open(f, "r") as file:
                blog_metadata = yaml.safe_load(file)
                metadata_slug = blog_metadata['slug']
                metadata_title  = blog_metadata['title']
                metadata_langs  = blog_metadata['lang']
                metadata_image  = blog_metadata['image']
                print(f"------ processing -- {metadata_slug}")
                for lang in metadata_langs:
                    print(f"--- title --- in {lang}")
                    title = translate_title(metadata_title, lang)
                    time.sleep(5)
                    print(f"--- slug  --- in {lang}")
                    slug  = translate_slug(metadata_title, lang)
                    time.sleep(5)
                    print(f"--- body  --- in {lang}")
                    body  = generate_blog_post(metadata_title, lang)
                    time.sleep(5)

                    path = f'../_posts/{metadata_slug}' #replace with os.path.join
                    if not os.path.exists(path):
                        os.makedirs(path)
                    post_name = f"{path}/{datetime.today().strftime('%Y-%m-%d')}-{slug}.md"
                    if not os.path.exists(post_name):
                        with open(post_name, "w") as file:
                            file.write(
f"""---
layout: post
title: {title}
slug: {slug}
lang: {lang}
image: {metadata_image}
---
{body}
                                """
                            )
                    

__main__()

