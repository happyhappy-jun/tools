import fire
import requests
from lxml import html
import re
import yaml
import json


def read_cookies_from_yaml(yaml_path):
    # Load cookies from a YAML file
    with open(yaml_path, 'r') as file:
        cookies = yaml.safe_load(file)
    return cookies


def process_urls(file_path, yaml_path):
    # Get cookies from the YAML file
    cookies = read_cookies_from_yaml(yaml_path)

    # Read URLs from the given file
    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file if line.strip()]

    results = []

    for url in urls:
        try:
            # Fetch the content of the URL with cookies
            response = requests.get(url, cookies=cookies)
            response.raise_for_status()  # Ensure the request was successful

            # Parse the HTML
            doc = html.fromstring(response.content)

            # Extract the content of the specific tag using XPath
            tag_content = doc.xpath('//*[@id="viewer"]/div[1]/h1/text()')
            title = tag_content[0] if tag_content else "No content found"

            # Find all m3u8 URLs in the document
            m3u8_urls = re.findall(r'https?://\S+\.m3u8', response.text)

            results.append({
                "title": title,
                "m3u8_urls": m3u8_urls
            })
        except requests.RequestException as e:
            results.append({
                "error": str(e)
            })

    return results


def main(input_path, cookie_path, output_path='results.json'):
    results = process_urls(input_path, cookie_path)
    # Export results to a JSON file
    with open(output_path, 'w') as json_file:
        json.dump(results, json_file, indent=4)

    print(f"Results have been saved to {output_path}")


if __name__ == '__main__':
    fire.Fire(main)
