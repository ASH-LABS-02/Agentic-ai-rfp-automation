import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin

DOWNLOAD_DIR = "downloaded_tenders"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def fetch_pdfs_from_site(site_url: str):
    response = requests.get(site_url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    downloaded = []

    for link in soup.find_all("a"):
        href = link.get("href", "")
        if href.lower().endswith(".pdf"):
            pdf_url = urljoin(site_url, href)
            filename = os.path.basename(href)
            local_path = os.path.join(DOWNLOAD_DIR, filename)

            if not os.path.exists(local_path):
                pdf_data = requests.get(pdf_url).content
                with open(local_path, "wb") as f:
                    f.write(pdf_data)

                downloaded.append(filename)

    return downloaded
