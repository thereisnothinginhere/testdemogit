from bs4 import BeautifulSoup
from extensions import seedr_download
from time import time
from seedrcc import Login,Seedr
import requests

Username  = "herobenhero4@gmail.com" #@param {type:"string"}
Password  = "Ge^j)&amp;H&amp;VkpBYwNmP247R" #@param {type:"string"}

account = Login(Username, Password)
account.authorize()
seedr = Seedr(token=account.token)

def get_magnetic_urls(URL):
  # Send an HTTP request to the web server
  response = requests.get(URL)

  # Parse the HTML code of the web page
  soup = BeautifulSoup(response.text, 'html.parser')

  # Find all the <a> elements on the page that have a "magnet" href attribute
  magnetic_links = soup.find_all('a', href=lambda x: x and x.startswith('magnet:'))
  magnets=[]
  # Print the text of each magnetic link
  for link in magnetic_links:
    magnets.append(link['href'])
  return magnets

def get_mirrors():
    return ["https://eztvx.to", "https://eztv1.xyz", "https://eztv.wf", "https://eztv.tf", "https://eztv.yt"]

Site = "https://eztvx.to/home" #@param {type:"string"}
filename = "magnet_links_eztv.txt"

def scrape_links(site_url):
    response = requests.get(site_url+'/home')
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a', href=lambda x: x and x.startswith('/ep/') and x.endswith('/'))
    return links

existing_magnet_links = set()

for mirror_site in get_mirrors():
    links = scrape_links(mirror_site)
    
    if links:
        break  # If links are found, exit the loop
# print(mirror_site)
if not links:
    print("No links found on any mirror site. Exiting.")
else:
    try:
        with open(filename, "r") as file:
            existing_magnet_links = set(file.read().splitlines())
    except FileNotFoundError:
        pass  # No existing file, so the set remains empty
    try:
        with open(filename, "a") as file:
            # start_time = time()
            for link in links:
                magnets = get_magnetic_urls(mirror_site+link['href'])
                for magnet in magnets:
                    # print(magnet)
                    if magnet not in existing_magnet_links:
                        seedr_download(magnet,seedr)
                        file.write(magnet + "\n")
                        existing_magnet_links.add(magnet)
    
                # elapsed_time = time() - start_time
                # if elapsed_time > 0.2 * 60 * 60:  # 2.5 hours in seconds
                #     print("Stopping script after 2.5 hours.")
                #     break
    except Exception as e:
        print(e)