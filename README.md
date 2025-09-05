# Automated-Research-Paper-Retrieval

A simple Python tool to **search, download, and organize research papers** from **ArXiv**, **Semantic Scholar**, and **CrossRef**.
It saves:

* **PDFs** of retrieved papers into a folder
* A single **metadata.json** file containing structured metadata for all papers

---

## Features

* Fetch papers by **search query** from:

  * [ArXiv API](https://arxiv.org/help/api/)
  * [Semantic Scholar API](https://api.semanticscholar.org/api-docs/graph)
  * [CrossRef API](https://api.crossref.org/)
* Download PDFs automatically (when available)
* Collect metadata in a **standard JSON schema**:

```json
{
    "title": "Lecture Notes: Optimization for Machine Learning",
    "abstract": "Lecture notes on optimization for machine learning, derived from a course...",
    "link": "http://arxiv.org/abs/1909.03550v1",
    "published": "2019-09-08T21:49:42Z",
    "pdf_url": "http://arxiv.org/pdf/1909.03550v1.pdf",
    "pdf_path": "data/pdfs/machine_learning_paper_1.pdf"
}
```

---

## Project Structure

```
.
├── fetch_papers.py       # Main script
├── requirements.txt      # Dependencies
├── README.md             # Documentation
└── data/
    ├── pdfs/             # Downloaded PDFs
    └── metadata.json     # Collected metadata
```

---

## Installation

1. Clone the repo:

```bash
git clone https://github.com/BhaveshBhakta/Automated-Research-Paper-Retrieval.git
cd Automated-Research-Paper-Retrieval
```

2. Create virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate   # On Mac/Linux
venv\Scripts\activate      # On Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

Run the script with your query:

```bash
python fetch_papers.py --query "machine learning" --max_results 30 --output_dir data
```

## Future Improvements

* Deduplicate papers across sources
* Add keyword filtering (e.g., year, author)

## Contributing

Contributions are welcome!

* Fork the repo
* Create a new branch (`git checkout -b feature-name`)
* Commit your changes (`git commit -m "Add new feature"`)
* Push to your branch and open a Pull Request
