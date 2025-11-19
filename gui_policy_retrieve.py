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
from tkinter import *
from tkinter import messagebox



relevant_keywords_total = {"green transition", "green economy", "twin transition", "green jobs", "digitalisation", "green skills","labour market",  "skill needs", "skills forecast",  "digital skills", "labour market information", "skills", "skill needs"}

relevant_keywords_transition = {"green transition", "green economy", "twin transition", "green jobs", "digitalisation", "digital transition" }

relevant_keywords_skills ={"green skills","labour market",  "skill needs", "skills forecast", "skills", "digital skills", "labour market information", "skill needs", "market", "labour", "skills forecast"}

folder_to_save= "C:/Users/Evangelia/Documents/ΕΥΑΓΓΕΛΙΑ ΕΓΓΡΑΦΑ/UoCrete/tasks/task 5.1 files/europa/url_try/"

existing_files = [f for f in listdir(folder_to_save) if isfile(join(folder_to_save, f))]

all_links = []

# def File_Check(title, description, download_link):
    
#     def on_confirm():
        




# for word in ['green', 'twin', 'digital']:

#     for year in range (2025, 2019, -1):
        
    # for page in range(0,20):
for page in range(0,200, 50):  # adjust range as needed

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
        # all_links.append({"title": title, "url": full_url})
        all_links.append(full_url)

    print(f"→ Found {len(links)} links on page {page}")


counter = 0
# root = Tk()
# label = Label(root, text="Here you will see the descriptions and titles of the candidate papers")
# label.pack()
# button = Button(root, text = 'Download this!', width=25, command=on_confirm)
# button.pack()
# root.mainloop()


# for item in all_links:
#     link = item["url"]
#     # title = item["title"]
#     print(f"\n🔗 Fetching:\n{link}")
#     r = requests.get(link)
#     soup = BeautifulSoup(r.text, "html.parser")
#     desc_tag = soup.select_one('meta[name="dc.description"]')
#     title_tag = soup.select_one('meta[name="dc.title"]')

#     description = desc_tag.get("content", "").strip() if desc_tag else ""
#     title = title_tag.get("content", "").strip() if title_tag else ""

#     print("Title found:", title[:150], "..." if len(title) > 150 else "<it's too big to print>")
#     print("Description found:", description[:150], "..." if len(description) > 150 else "<it's too big to print>")

#     download_link = None
#     for a in soup.select("a.download[data-uri]"):
#         data_uri = a.get("data-uri")
#         if data_uri and "format=pdf" in data_uri.lower():
#             download_link = urljoin("https://op.europa.eu", data_uri)
#             break

#     for k in relevant_keywords_skills:
#         for l in relevant_keywords_transition:
#             if k in description and l in description:
#                 print("yes", k, l)
#                 print("Downloading file now...", title, "\n")
                
#                 safe_title = re.sub(r'[\\/*?:"<>|]', "_", title)
#                 safe_title = safe_title.strip().replace("\n", " ")[:150]

#                 file_name = os.path.join(folder_to_save, safe_title + ".pdf")

#                 if os.path.exists(file_name):
#                     print("File already exists, skipping:", file_name)
#                     break

    
#                 try:
#                     headers = {
#                         "User-Agent": "Mozilla/5.0",
#                         "Accept": "application/pdf"
#                     }
#                     r = requests.get(download_link, headers=headers, allow_redirects=True)
#                     r.raise_for_status()

#                     with open(file_name, "wb") as f:
#                         f.write(r.content)

#                     print("Downloaded:", file_name, "\n")
#                     counter +=1
#                 except Exception as e:
#                     print("Error downloading", download_link, e, "\n")     
#         else: 
#             continue
#         break

# print(counter, " new files downloaded")


def Correct_File(all_links):
    link_num = 0

    current = {"title": "", "description": "", "download_link": None}

    # download_link = None
    # title = None

    def load_link(i):
        nonlocal link_num
        link_num = i

        if not (0 <= link_num < len(all_links)):
            messagebox.showinfo("End", "No more links.")
            return

        url = all_links[link_num]
        title, description, download_link = fetch_publication_info(url)

        # Save to state
        current["title"] = title
        current["description"] = description
        current["download_link"] = download_link

        # Keyword filtering
        ok_transition = any(x in description for x in relevant_keywords_transition)
        ok_skills = any(x in description for x in relevant_keywords_skills)

        if ok_transition and ok_skills:
            title_var.set(title or "<no title>")
            text_desc.delete("1.0", END)
            text_desc.insert("1.0", description or "<no description>")
        else:
            on_next()

    def on_next():
        load_link(link_num + 1)

    def on_previous():
        load_link(link_num - 1)

    def on_confirm():
        title = current["title"]
        download_link = current["download_link"]
        if not download_link:
            messagebox.showerror("Error", "No PDF link found.")
            return

        # safe_title = re.sub(r'[\\/*?:"<>|]', "_", title)[:120]
        safe_title = re.sub(r'[\\/*?:"<>|]', "_", title)
        safe_title = safe_title.strip().replace("\n", " ")[:150]
        path = os.path.join(folder_to_save, safe_title + ".pdf")

        r = requests.get(download_link, headers={"User-Agent": "Mozilla/5.0"})
        with open(path, "wb") as f:
            f.write(r.content)

        messagebox.showinfo("Saved", f"Saved:\n{path}")
    
    def fetch_publication_info(url):
    # """Fetch title, description, and PDF link from a publication detail page."""
            

        # print("Title found:", title[:150], "..." if len(title) > 150 else "<it's too big to print>")
        # print("Description found:", description[:150], "..." if len(description) > 150 else "<it's too big to print>")
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")

        desc_tag = soup.select_one('meta[name="dc.description"]')
        title_tag = soup.select_one('meta[name="dc.title"]')

        description = desc_tag.get("content", "").strip() if desc_tag else ""
        title = title_tag.get("content", "").strip() if title_tag else ""

        # PDF link
        download_link = None
        for a in soup.select("a.download[data-uri]"):
            data_uri = a.get("data-uri")
            if data_uri and "format=pdf" in data_uri.lower():
                download_link = urljoin("https://op.europa.eu", data_uri)
                break

        return title, description, download_link

    root = Tk()
    root.title("EU Publications Review")

    title_var = StringVar()
    Label(root, textvariable=title_var, wraplength=800).pack()

    text_desc = Text(root, width=100, height=20, wrap="word")
    text_desc.pack()

    frame = Frame(root)
    frame.pack(pady=10)

    Button(frame, text="Previous", command=on_previous).pack(side=LEFT, padx=10)
    Button(frame, text="Download this!", command=on_confirm).pack(side=LEFT, padx=10)
    Button(frame, text="Next", command=on_next).pack(side=LEFT, padx=10)

    load_link(0)
    root.mainloop()

    # def on_confirm():

    #     print("Downloading file now...", title, "\n")
                
    #     safe_title = re.sub(r'[\\/*?:"<>|]', "_", title)
    #     safe_title = safe_title.strip().replace("\n", " ")[:150]

    #     file_name = os.path.join(folder_to_save, safe_title + ".pdf")

    #     # if os.path.exists(file_name):
    #     #     print("File already exists, skipping:", file_name)
    #     #     break


    #     try:
    #         headers = {
    #             "User-Agent": "Mozilla/5.0",
    #             "Accept": "application/pdf"
    #         }
    #         r = requests.get(download_link, headers=headers, allow_redirects=True)
    #         r.raise_for_status()

    #         with open(file_name, "wb") as f:
    #             f.write(r.content)

    #         print("Downloaded:", file_name, "\n")
    #         counter +=1
    #     except Exception as e:
    #         print("Error downloading", download_link, e, "\n")
    #     # nonlocal selected_path
    #     # selected_path = files[file_num]
    #     root.quit()
    #     root.destroy()

    # def on_next():
    #     nonlocal link_num
    #     nonlocal download_link
    #     nonlocal title
    #     link_num += 1
    #     if link_num < len(all_links):

    #         link = all_links[link_num]
    #         print(f"\n🔗 Fetching:\n{link}")
    #         r = requests.get(link)
    #         soup = BeautifulSoup(r.text, "html.parser")
    #         desc_tag = soup.select_one('meta[name="dc.description"]')
    #         title_tag = soup.select_one('meta[name="dc.title"]')

    #         description = desc_tag.get("content", "").strip() if desc_tag else ""
    #         title = title_tag.get("content", "").strip() if title_tag else ""

    #         # print("Title found:", title[:150], "..." if len(title) > 150 else "<it's too big to print>")
    #         # print("Description found:", description[:150], "..." if len(description) > 150 else "<it's too big to print>")

    #         download_link = None
    #         for a in soup.select("a.download[data-uri]"):
    #             data_uri = a.get("data-uri")
    #             if data_uri and "format=pdf" in data_uri.lower():
    #                 download_link = urljoin("https://op.europa.eu", data_uri)
    #                 break

    #         for k in relevant_keywords_skills:
    #             for l in relevant_keywords_transition:
    #                 if k in description and l in description:
    #                                 messagebox.showinfo("Title: %s \n Description: %s ", title, description)
    #                                 # messagebox.showinfo("Description", description)
    #                 else: 
    #                     on_next()


    #         # open_file_in_viewer(files[file_num])  # Open the next file in an external viewer
    #     else:
    #         messagebox.showinfo("Info", "No more files to check.")
    #         link = all_links[link_num-1]
    #         print(f"\n🔗 Fetching:\n{link}")
    #         r = requests.get(link)
    #         soup = BeautifulSoup(r.text, "html.parser")
    #         desc_tag = soup.select_one('meta[name="dc.description"]')
    #         title_tag = soup.select_one('meta[name="dc.title"]')

    #         description = desc_tag.get("content", "").strip() if desc_tag else ""
    #         title = title_tag.get("content", "").strip() if title_tag else ""

    #         # print("Title found:", title[:150], "..." if len(title) > 150 else "<it's too big to print>")
    #         # print("Description found:", description[:150], "..." if len(description) > 150 else "<it's too big to print>")

    #         download_link = None
    #         for a in soup.select("a.download[data-uri]"):
    #             data_uri = a.get("data-uri")
    #             if data_uri and "format=pdf" in data_uri.lower():
    #                 download_link = urljoin("https://op.europa.eu", data_uri)
    #                 break

    #         for k in relevant_keywords_skills:
    #             for l in relevant_keywords_transition:
    #                 if k in description and l in description:
    #                                 messagebox.showinfo("Title: %s \n Description: %s ", title, description)
    #                                 # messagebox.showinfo("Description", description)
    #                 else: 
    #                     on_previous()            
    #         # root.quit()
    #         # root.destroy()

    # def on_previous():
    #     nonlocal download_link
    #     nonlocal link_num
    #     nonlocal title
    #     if link_num > 0:
    #         link_num -= 1
    #         link = all_links[link_num]

    #         print(f"\n🔗 Fetching:\n{link}")
    #         r = requests.get(link)
    #         soup = BeautifulSoup(r.text, "html.parser")
    #         desc_tag = soup.select_one('meta[name="dc.description"]')
    #         title_tag = soup.select_one('meta[name="dc.title"]')

    #         description = desc_tag.get("content", "").strip() if desc_tag else ""
    #         title = title_tag.get("content", "").strip() if title_tag else ""

    #         # print("Title found:", title[:150], "..." if len(title) > 150 else "<it's too big to print>")
    #         # print("Description found:", description[:150], "..." if len(description) > 150 else "<it's too big to print>")

    #         download_link = None
    #         for a in soup.select("a.download[data-uri]"):
    #             data_uri = a.get("data-uri")
    #             if data_uri and "format=pdf" in data_uri.lower():
    #                 download_link = urljoin("https://op.europa.eu", data_uri)
    #                 break

    #         for k in relevant_keywords_skills:
    #             for l in relevant_keywords_transition:
    #                 if k in description and l in description:
    #                                 messagebox.showinfo("Title: %s \n Description: %s ", title, description)
    #                                 # messagebox.showinfo("Description", description)
    #                 else: 
    #                     on_previous()

    #         # open_file_in_viewer(files[file_num])  # Open the previous file in an external viewer
    #     else:

    #         messagebox.showinfo("Info", "No more files to check.")
    #         link = all_links[link_num-1]
    #         print(f"\n🔗 Fetching:\n{link}")
    #         r = requests.get(link)
    #         soup = BeautifulSoup(r.text, "html.parser")
    #         desc_tag = soup.select_one('meta[name="dc.description"]')
    #         title_tag = soup.select_one('meta[name="dc.title"]')

    #         description = desc_tag.get("content", "").strip() if desc_tag else ""
    #         title = title_tag.get("content", "").strip() if title_tag else ""

    #         # print("Title found:", title[:150], "..." if len(title) > 150 else "<it's too big to print>")
    #         # print("Description found:", description[:150], "..." if len(description) > 150 else "<it's too big to print>")

    #         download_link = None
    #         for a in soup.select("a.download[data-uri]"):
    #             data_uri = a.get("data-uri")
    #             if data_uri and "format=pdf" in data_uri.lower():
    #                 download_link = urljoin("https://op.europa.eu", data_uri)
    #                 break

    #         for k in relevant_keywords_skills:
    #             for l in relevant_keywords_transition:
    #                 if k in description and l in description:
    #                                 messagebox.showinfo("Title: %s \n Description: %s ", title, description)
    #                                 # messagebox.showinfo("Description", description)
    #                 else: 
    #                     on_next()
    #         # messagebox.showinfo("Info", "No more links to check.")
    #         # open_file_in_viewer(all_links[file_num])
    #         root.quit()
    #         root.destroy()


    # def open_file_in_viewer(path):
    #     try:
    #         # Use os.startfile (Windows) to open the file with the default associated DICOM viewer
    #         os.startfile(path)
    #     except Exception as e:
    #         messagebox.showerror("Error", f"Could not open file: {e}")

    # def on_print_metadata_and_next():
    #     nonlocal file_num
    #     # Print the metadata (surname, name, year, month, day)
    #     print(f" Do it later: Metadata: Surname: {surname}, Name: {name}, Year: {year}, Month: {month}, Day: {day}")
        
    #     # Move to the next file
    #     root.quit()
    #     root.destroy()
    root = Tk()
    label = Label(root, text="Here you will see the descriptions and titles of the candidate papers")
    label.pack()
    button = Button(root, text = 'Download this!', width=25, command=on_confirm)
    button.pack(side=TOP, pady=10)

    btn_next = Button(root, text="Next", command=(on_next))
    btn_next.pack(side=RIGHT)

    btn_previous = Button(root, text="Previous", command=(on_previous))
    btn_previous.pack(side=LEFT,padx=20, pady=10)

    link = all_links[0]

    print(f"\n🔗 Fetching:\n{link}")
    r = requests.get(link)
    soup = BeautifulSoup(r.text, "html.parser")
    desc_tag = soup.select_one('meta[name="dc.description"]')
    title_tag = soup.select_one('meta[name="dc.title"]')

    description = desc_tag.get("content", "").strip() if desc_tag else ""
    title = title_tag.get("content", "").strip() if title_tag else ""

    # print("Title found:", title[:150], "..." if len(title) > 150 else "<it's too big to print>")
    # print("Description found:", description[:150], "..." if len(description) > 150 else "<it's too big to print>")

    download_link = None
    for a in soup.select("a.download[data-uri]"):
        data_uri = a.get("data-uri")
        if data_uri and "format=pdf" in data_uri.lower():
            download_link = urljoin("https://op.europa.eu", data_uri)
            break

    for k in relevant_keywords_skills:
        for l in relevant_keywords_transition:
            if k in description and l in description:
                            messagebox.showinfo("Title", title)
                            messagebox.showinfo("Description", description)
            else: 
                on_next()



    root.mainloop()

Correct_File(all_links)