import requests
import re  # pour les regex

from bs4 import BeautifulSoup





url = 'http://www.barreaudenice.com/annuaire/avocats/?fwp_paged=5'

def get_all_pages():

    urls = [] # on initialise une liste vide qui va contenir les urls
    page_number = 1

    for i in range(104):
        i = f"http://www.barreaudenice.com/annuaire/avocats/?fwp_paged={page_number}"
        page_number +=1
        urls.append(i)
    # la boucle nous permet de lister ttes les 104 pages

    return urls


def parse_attorney(url):
    source = requests.get(url).content

    soup = BeautifulSoup(source, 'html.parser')

    avocats = soup.find_all('div', class_= 'callout secondary annuaire-single')

    for avocat in avocats:

        try:
            nom = avocat.find('h3').text.strip() # la methode strip() permet de supprimer les espaces avant et apres les textes
        except AttributeError as e:
            nom =""

        try:
            adresse = avocat.find('span', class_='adresse').text.strip()
        except AttributeError as e:
            adresse =""

        try:   
            adresse_finale = re.sub(r"\s+", " ", adresse)
        except AttributeError as e:
            adresse_finale =""
        # le 1er argument de la fonction re.sub()  - r"\s+" veut dire remplacer 1 ou plusieurs élmts
        # le 2e argument de la fonction re.sub()  - "" indique qu'on veut remplacer par un espace 
        # le 3e argument de la fonction re.sub()  - indique sur quelle elmt (varaible) on va apporter les modifs 

        try:
            telephone = avocat.find('span', class_='telephone').text.strip()
        except AttributeError as e:
            telephone =""

        try:

            email = avocat.find('span', class_='email').a.text.strip()
        except AttributeError as e:
            email = ""

        chemin = r"C:\Users\Serge Demanou\Desktop\data scraping\annuaire_avocats.txt" # ici c'est le chemin où on va stocker les données recupéré
        # r" " permet ici de ne pas prendre en compte les caractères spéciaux tels que (\ et _)

        with open (chemin, "a") as f:   # ici on ajoute des données au doc donc on choisi la fonction append() symbolisé par "a"
            f.write(f"{nom}\n")        # le (\n) permet de separer chaque bloc de données sur le fichier .txt
            f.write(f"{adresse_finale}\n")
            f.write(f"{telephone}\n")
            f.write(f"{email}\n\n")

    # penser aussi à tjr suppr le fichier brouillon .txt qu'on a crée parce que chaque fois on ajoute des données avec "a"

def parse_all_attorney():  # fonction pour recupérer tous les avocats des 104 pages
    
    pages = get_all_pages() # on initialise une variable pour recupérer tous les urls

    for page in pages:
        parse_attorney(url=page)



parse_all_attorney()