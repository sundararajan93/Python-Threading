import time
import requests
from bs4 import BeautifulSoup

img_url = []

def get_urls(URL):
    resp = requests.get(URL)
    soup = BeautifulSoup(resp.content, 'html.parser')
    anchor_tag = soup.findAll("a", {"title" : "Download photo"})

    for i in anchor_tag:
        get_link = i["href"]
        img_url.append(get_link)

def download_images(URL):
    file_name = "Images/"+URL.split('/')[4]+".jpg"
    resp = requests.get(URL)
    
    file = open(file_name, "wb")
    file.write(resp.content)
    file.close()

def main():
    start = time.perf_counter() 
    print(f"Grabbing the URLs...")
    get_urls('https://unsplash.com/t/nature')
    print("Downloading the Images")

    for link in img_url:
        download_images(link)
    
    finish = time.perf_counter()
    print(f"{len(img_url)} Images Downloaded in {round(finish - start, 2)} second(s)")

if __name__ == '__main__':
    main()
