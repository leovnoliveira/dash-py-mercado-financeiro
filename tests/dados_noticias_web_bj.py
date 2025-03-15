from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def brazil_journal(tema):
    options = Options()
    options.headless = False

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    if tema == 'economia':
        url = 'https://braziljournal.com/categoria/economia/'
    elif tema == 'tech':
        url = 'https://braziljournal.com/categoria/tecnologia/'
    else:
        raise ValueError("Tema inválido. Escolha 'economia' ou 'tech'.")

    driver.get(url)

    # 1) Fechar pop-up se existir
    # try:
    #     WebDriverWait(driver, 5).until(
    #         EC.element_to_be_clickable((By.ID, "aceitar-cookies"))
    #     ).click()
    # except:
    #     pass

    # 2) Esperar explicitamente o carregamento do elemento
    wait = WebDriverWait(driver, 15)
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "figcaption.boxarticle-infos")))

    # 3) Pegar o HTML após o carregamento
    html_not = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html_not, 'html.parser')

    caixas_noticias = soup.find_all('figcaption', class_='boxarticle-infos')
    print("Quantidade de notícias encontradas:", len(caixas_noticias))

    df_noticias = pd.DataFrame(columns=['manchete', 'subtopico', 'link', 'topico', 'jornal'], index=range(6))

    for i, noticia in enumerate(caixas_noticias):
        if i > 5:
            break

        subtopico = noticia.find('p', class_='boxarticle-infos-tag')
        subtopico = subtopico.text.strip() if subtopico else "Sem subtópico"

        titulo = noticia.find("h2", class_='boxarticle-infos-title')
        if titulo and titulo.a:
            manchete = titulo.text.strip()
            link = titulo.a.get('href', 'Sem link')
        else:
            manchete = "Sem manchete"
            link = "Sem link"

        df_noticias.loc[i, 'subtopico'] = subtopico
        df_noticias.loc[i, 'manchete'] = manchete
        df_noticias.loc[i, 'link'] = link
        df_noticias.loc[i, 'topico'] = tema
        df_noticias.loc[i, 'jornal'] = 'brazil_journal'

    return df_noticias

if __name__ == "__main__":

    noticias_bj = brazil_journal(tema='economia')

    print(noticias_bj)