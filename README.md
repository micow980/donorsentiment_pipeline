# Donor Sentiment Enrichment Pipeline (AWS + OpenAI)

This project demonstrates a lightweight, cloud-native data pipeline that leverages OpenAI to extract sentiment, donation likelihood, and message themes from raw donor communications. It showcases how AI can be integrated into modern data workflows to unlock valuable engagement insights for nonprofit organizations.

---

## 🚀 Project Overview

With the increasing push to integrate AI across industries, this project simulates how a data engineer can enrich qualitative donor data using language models in a scalable and serverless AWS pipeline.

### ✨ Features
- Ingests raw donor messages from Amazon S3
- Uses the OpenAI API (GPT-4) to extract:
  - Sentiment (positive, neutral, negative)
  - Donation likelihood (0–100)
  - Message theme (e.g., gratitude, concern, opt-out)
- Writes enriched output to S3 for querying or loading into Redshift

---

## 🧱 Architecture

```text
Amazon S3 (raw CSV)
        ↓
AWS Lambda (Python + OpenAI)
        ↓
Amazon S3 (enriched CSV)
        ↓
(optional) AWS Glue
        ↓
Amazon Redshift (queryable table)
