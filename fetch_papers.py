import argparse
import json
import os
from pathlib import Path
import requests

def fetch_arxiv(query, max_results=5):
    url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results={max_results}"
    resp = requests.get(url)
    results = []

    if resp.status_code == 200:
        import xml.etree.ElementTree as ET
        root = ET.fromstring(resp.text)
        ns = {"arxiv": "http://www.w3.org/2005/Atom"}

        for entry in root.findall("arxiv:entry", ns):
            title = entry.find("arxiv:title", ns).text.strip()
            abstract = entry.find("arxiv:summary", ns).text.strip()
            link = entry.find("arxiv:id", ns).text.strip()
            published = entry.find("arxiv:published", ns).text.strip()

            pdf_url = None
            for link_tag in entry.findall("arxiv:link", ns):
                if link_tag.attrib.get("title") == "pdf":
                    pdf_url = link_tag.attrib["href"]

            results.append({
                "title": title,
                "abstract": abstract,
                "link": link,
                "published": published,
                "pdf_url": pdf_url
            })
    return results

def fetch_semantic_scholar(query, limit=5):
    url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={query}&limit={limit}&fields=title,abstract,url,year,openAccessPdf"
    resp = requests.get(url)
    results = []

    if resp.status_code == 200:
        data = resp.json()
        for p in data.get("data", []):
            results.append({
                "title": p.get("title"),
                "abstract": p.get("abstract"),
                "link": p.get("url"),
                "published": str(p.get("year")),
                "pdf_url": p.get("openAccessPdf", {}).get("url")
            })
    return results

def fetch_crossref(query, rows=5):
    url = f"https://api.crossref.org/works?query={query}&rows={rows}"
    resp = requests.get(url)
    results = []

    if resp.status_code == 200:
        data = resp.json()
        for item in data.get("message", {}).get("items", []):
            title = item.get("title", [""])[0]
            abstract = item.get("abstract", "")
            link = item.get("URL", "")
            published = "-".join(str(x) for x in item.get("created", {}).get("date-parts", [[None]])[0])
            pdf_url = None
            for l in item.get("link", []):
                if l.get("content-type") == "application/pdf":
                    pdf_url = l.get("URL")

            results.append({
                "title": title,
                "abstract": abstract,
                "link": link,
                "published": published,
                "pdf_url": pdf_url
            })
    return results

def download_pdf(pdf_url, save_path):
    if not pdf_url:
        return False
    try:
        r = requests.get(pdf_url, stream=True, timeout=15)
        if r.status_code == 200:
            with open(save_path, "wb") as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
            return True
    except Exception:
        return False
    return False

def collect_papers(query, max_results, output_dir):
    Path(output_dir, "pdfs").mkdir(parents=True, exist_ok=True)

    metadata = []

    sources = [
        ("arxiv", fetch_arxiv(query, max_results)),
        ("semanticscholar", fetch_semantic_scholar(query, max_results)),
        ("crossref", fetch_crossref(query, max_results))
    ]

    paper_counter = 1
    for source, papers in sources:
        for paper in papers:
            pdf_filename = f"{query.replace(' ', '_')}_paper_{paper_counter}.pdf"
            pdf_path = Path(output_dir, "pdfs", pdf_filename)

            if download_pdf(paper["pdf_url"], pdf_path):
                paper["pdf_path"] = str(pdf_path)
            else:
                paper["pdf_path"] = None

            metadata.append(paper)
            paper_counter += 1

    with open(Path(output_dir, "metadata.json"), "w") as f:
        json.dump(metadata, f, indent=4)

    print(f"✅ Downloaded {len(metadata)} papers. Metadata saved to {output_dir}/metadata.json")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", type=str, required=True, help="Search query (e.g., 'machine learning')")
    parser.add_argument("--max_results", type=int, default=5, help="Max results per source")
    parser.add_argument("--output_dir", type=str, default="data", help="Where to save PDFs and metadata")
    args = parser.parse_args()

    collect_papers(args.query, args.max_results, args.output_dir)
