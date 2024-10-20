import os
import requests
from bs4 import BeautifulSoup
import urllib.parse

def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

def download_images(search_term, num_images=50):
    create_folder(search_term)
    search_url = f"https://www.google.com/search?hl=ko&tbm=isch&q={urllib.parse.quote(search_term)}"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    img_tags = soup.find_all('img')
    img_urls = [img['src'] for img in img_tags[1:num_images+1]]

    for start in range(0, num_images, 20):
        response = requests.get(f"{search_url}&start={start}")
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags = soup.find_all('img')
        img_urls += [img['src'] for img in img_tags[1:21]]

    img_urls = img_urls[:num_images]

    for i, img_url in enumerate(img_urls):
        img_data = requests.get(img_url).content
        with open(os.path.join(search_term, f"{search_term}_{i+1}.jpg"), 'wb') as img_file:
            img_file.write(img_data)

if __name__ == "__main__":
    search_term = input("검색어를 입력하세요: ")
    download_images(search_term)
