import requests
from bs4 import BeautifulSoup

def get_news(): 
    url = 'https://www.uol.com.br/'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    


    todos_os_links = soup.find_all('a', class_=['hyperlink', 'headlineMain__link'])
    if todos_os_links:
          print("\nManchetes e Links encontrados:")

          for link_individual in todos_os_links:
            url_manchete = "Link não encontrado"

            if 'href' in link_individual.attrs:
                    url_manchete = link_individual.get('href')

                    if url_manchete.startswith('/'):
                        url_manchete = f"https://www.uol.com.br{url_manchete}"

            Manchete_h3 = link_individual.find('h3', class_=['title__element', 'headlineMain_n_title'])
            manchete_text = "Texto da manchete não encontrado"

            if Manchete_h3:
                manchete_text = Manchete_h3.text.strip()

                if manchete_text != "Título não encontrado" and url_manchete != "Link não encontrado":
                    print(f"Manchete: {manchete_text} \n  Link: {url_manchete}\n") 
    else:
            print("Manchete não encontrada com a tag h3 e class 'title'. ")
    return todos_os_links
# get_news()