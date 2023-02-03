
import requests
from bs4 import BeautifulSoup
from uuid import uuid1
from lib.db.db_manager import DBManager
from models.db.anime import Anime_DB

def init_anime():
    anime_name_list = []
    for year in range(2015, 2023):
        rsp = requests.get(f"https://en.wikipedia.org/wiki/{year}_in_anime")
        soup = BeautifulSoup(rsp.text, "html.parser")
        table_list = soup.find_all("table", border="1")
        for table in table_list: 
            i_list = table.find_all("i")
            for i in i_list:
                try:
                    anime_name = i.find("a").text
                    if len(anime_name) < 32:
                        anime_name_list.append(anime_name)
                except:
                    pass
    
    with DBManager().session_ctx() as session:
        for anime_name in list(set(anime_name_list)):
            print(anime_name)
            anime_db = Anime_DB(
                anime_id = str(uuid1()),
                anime_name = anime_name
            )
            session.add(anime_db)