import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import openpyxl
from os import listdir
import requests
import re
from os.path import isfile, join
import os

relevant_keywords_total = {"green transition", "green economy", "twin transition", "green jobs", "digitalisation", "green skills","labour market",  "skill needs", "skills forecast",  "digital skills", "labour market information", "skills", "skill needs"}

relevant_keywords_transition = {"green transition", "green economy", "twin transition", "green jobs", "digitalisation", "digital", "digital transition" }

relevant_keywords_skills ={"green skills","labour market",  "skill needs", "skills forecast", "skills", "digital skills", "labour market information", "skill needs", "market", "labour", "skill", "skills forecast"}

folder_to_save= "C:/Users/Evangelia/Documents/ΕΥΑΓΓΕΛΙΑ ΕΓΓΡΑΦΑ/UoCrete/tasks/task 5.1 files/europa/url_try/"

existing_files = [f for f in listdir(folder_to_save) if isfile(join(folder_to_save, f))]

all_links = []

# for word in ['green', 'twin', 'digital']:

#     for year in range (2025, 2019, -1):
        
    # for page in range(0,20):
for page in range(0,2000, 50):  # adjust range as needed

    #2025
    # url = f"https://op.europa.eu/en/search-results?p_p_id=eu_europa_publications_portlet_pagination_PaginationPortlet_INSTANCE_gDBsAazqs5X2&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&queryText=green%20transition&facet.collection=EUPub&facet.documentFormat=PDF&facet.documentYear=2025&facet.language=ENG&sortBy=RELEVANCE-DESC&SEARCH_TYPE=SIMPLE&QUERY_ID=409156915&&facet.language=ENG&facet.language=ENG&facet.language=ENG&resultsPerPage=50&startRow={page}"

    #2024 & 2023
    # url = f"https://op.europa.eu/en/search-results?p_p_id=eu_europa_publications_portlet_pagination_PaginationPortlet_INSTANCE_gDBsAazqs5X2&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&queryText=green%20transition&facet.collection=EUPub&facet.language=ENG&facet.documentFormat=PDF&facet.documentYear=2024,2023&sortBy=RELEVANCE-DESC&SEARCH_TYPE=SIMPLE&QUERY_ID=409304349&&facet.language=ENG&resultsPerPage=50&startRow={page}"

    #2022
    # url = f"https://op.europa.eu/en/search-results?p_p_id=eu_europa_publications_portlet_pagination_PaginationPortlet_INSTANCE_gDBsAazqs5X2&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&queryText={word}%20transition&facet.collection=EUPub&facet.documentFormat=PDF&facet.documentYear={year}&facet.language=ENG&sortBy=RELEVANCE-DESC&SEARCH_TYPE=SIMPLE&QUERY_ID=409156915&&facet.language=ENG&facet.language=ENG&facet.language=ENG&resultsPerPage=50&startRow={page}"

    #digital
    # url = f"https://op.europa.eu/en/search-results?p_p_id=eu_europa_publications_portlet_pagination_PaginationPortlet_INSTANCE_gDBsAazqs5X2&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&queryText=digital%20transition&facet.collection=EUPub&facet.documentYear=2020&facet.language=ENG&facet.documentFormat=PDF&sortBy=RELEVANCE-DESC&SEARCH_TYPE=SIMPLE&QUERY_ID=409334003&&facet.language=ENG&resultsPerPage=50&startRow={page}"

    #twin
    url = f"https://op.europa.eu/en/search-results?p_p_id=eu_europa_publications_portlet_pagination_PaginationPortlet_INSTANCE_gDBsAazqs5X2&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&queryText=twin%20transition&facet.collection=EUPub&facet.documentFormat=PDF&facet.documentYear=2022&facet.language=ENG&sortBy=RELEVANCE-DESC&SEARCH_TYPE=SIMPLE&QUERY_ID=409378404&&facet.language=ENG&facet.language=ENG&facet.language=ENG&resultsPerPage=50&startRow={page}"

    print(url)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    # print(soup)
    links = (soup.select("a.documentDetailLink"))
    if not links:
        print("No results found on this page — stopping.")
        break
    for a in links:
        href = a.get("href")
        if not href:
            continue
        full_url = urljoin("https://op.europa.eu", href)
        title = a.get_text(strip=True).replace("\n", " ")
        all_links.append({"title": title, "url": full_url})

    print(f"→ Found {len(links)} links on page {page}")

counter = 0

for item in all_links:
    link = item["url"]
    title = item["title"]
    print(f"\n🔗 Fetching: {title}\n{link}")
    r = requests.get(link)
    soup = BeautifulSoup(r.text, "html.parser")
    desc_tag = soup.select_one('meta[name="dc.description"]')
    title_tag = soup.select_one('meta[name="dc.title"]')

    description = desc_tag.get("content", "").strip() if desc_tag else ""
    title = title_tag.get("content", "").strip() if title_tag else ""

    print("Title found:", title[:150], "..." if len(title) > 150 else "<it's too big to print>")
    print("Description found:", description[:150], "..." if len(description) > 150 else "<it's too big to print>")

    download_link = None
    for a in soup.select("a.download[data-uri]"):
        data_uri = a.get("data-uri")
        if data_uri and "format=pdf" in data_uri.lower():
            download_link = urljoin("https://op.europa.eu", data_uri)
            break

    for k in relevant_keywords_skills:
        for l in relevant_keywords_transition:
            if k in description and l in description:
                print("yes", k, l)
                print("Downloading file now...", title, "\n")
                
                safe_title = re.sub(r'[\\/*?:"<>|]', "_", title)
                safe_title = safe_title.strip().replace("\n", " ")[:150]

                file_name = os.path.join(folder_to_save, safe_title + ".pdf")

                if os.path.exists(file_name):
                    print("File already exists, skipping:", file_name)
                    break

    
                try:
                    headers = {
                        "User-Agent": "Mozilla/5.0",
                        "Accept": "application/pdf"
                    }
                    r = requests.get(download_link, headers=headers, allow_redirects=True)
                    r.raise_for_status()

                    with open(file_name, "wb") as f:
                        f.write(r.content)

                    print("Downloaded:", file_name, "\n")
                    counter +=1
                except Exception as e:
                    print("Error downloading", download_link, e, "\n")     
        else: 
            continue
        break

print(counter, " new files downloaded")
