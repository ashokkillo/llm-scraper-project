# Apache Jira Scraper & LLM Corpus Generator

This project builds a **fault-tolerant**, **resume-capable**, and **scalable** data scraping pipeline that extracts publicly available issue data from Apache’s Jira instance and converts it into a **clean JSONL dataset** suitable for Large Language Model (LLM) training.

---

## 📌 Objective

- Scrape issues and metadata from 3 Apache public Jira projects:
  - **HDFS**
  - **KAFKA**
  - **SPARK**
- Handle **pagination**, **rate limits**, **HTTP failures**, and **resume state**
- Transform unstructured issue + comment text into structured **JSONL**
- Add **derived LLM tasks** (Summarization, Classification, QnA)

---

## 📁 Output Format (JSONL)

Each line = One issue document:

```json
{
  "id": "HDFS-12345",
  "project": "HDFS",
  "title": "...",
  "status": "Resolved",
  "priority": "Major",
  "description": "...plain text...",
  "comments": [
    {"author": "alice", "text": "...", "created": "..."}
  ],
  "combined_text": "...title + description + comments...",
  "derived": {
    "summary": null,
    "classification": {"type": "Bug"},
    "qa_pairs": []
  }
}

---

## Setup
- pip install -r requirements.txt
---
