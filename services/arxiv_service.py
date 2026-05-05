# services/arxiv_service.py

import requests
import xml.etree.ElementTree as ET
import os
import urllib.parse

DOWNLOAD_FOLDER = "uploads"


def search_arxiv(query, max_results=3):
    import urllib.parse
    import requests
    import xml.etree.ElementTree as ET

    try:
        if not query or query.strip() == "":
            print("Empty query received")
            return []

        encoded_query = urllib.parse.quote(query.strip())

        url = f"https://export.arxiv.org/api/query?search_query=all:{encoded_query}&start=0&max_results={max_results}"

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        print("FINAL URL:", url)

        response = requests.get(url, headers=headers, timeout=10)

        print("Status:", response.status_code)

        if response.status_code != 200:
            print("arXiv API error:", response.text)
            return []

        root = ET.fromstring(response.content)

        ns = {'atom': 'http://www.w3.org/2005/Atom'}

        papers = []

        for entry in root.findall('atom:entry', ns):
            title_elem = entry.find('atom:title', ns)
            title = title_elem.text.strip() if title_elem is not None else "No Title"

            pdf_url = ""
            for link in entry.findall('atom:link', ns):
                if link.attrib.get('type') == 'application/pdf':
                    pdf_url = link.attrib.get('href')

            papers.append({
                "title": title,
                "pdf_url": pdf_url
            })

        print("PAPERS FOUND:", len(papers))

        return papers

    except Exception as e:
        print("arXiv ERROR:", e)
        return []

def download_pdf(pdf_url, filename):
    try:
        response = requests.get(pdf_url)

        if response.status_code != 200:
            print("PDF download failed:", response.status_code)
            return None

        filepath = os.path.join(DOWNLOAD_FOLDER, filename)

        with open(filepath, "wb") as f:
            f.write(response.content)

        return filepath

    except Exception as e:
        print("Download error:", e)
        return None