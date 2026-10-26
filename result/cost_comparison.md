# Cost Comparison & Scalability Analysis

This document estimates the monthly operational costs of running the RAG application across three different scales (Small, Medium, Large). It compares a self-hosted ChromaDB setup against managed vector database alternatives (like Pinecone or Qdrant Cloud).

## Assumptions & Pricing (As of 2024)
- **Average Document Size:** 2,500 tokens (~5 chunks of 500 tokens).
- **Average Query:** 500 input tokens (context + question), 150 output tokens.
- **Embedding Cost:** $0.02 per 1M tokens (using `all-MiniLM-L6-v2` hosted locally).
- **LLM Cost:** Mistral Small API pricing - $0.20 per 1M input tokens, $0.60 per 1M output tokens.
- **Self-Hosted Vector DB:** A basic $20/month VPS (e.g., DigitalOcean, AWS Lightsail) can comfortably handle up to 1 million vectors using ChromaDB.
- **Managed Vector DB (Estimate):** Pinecone Serverless or Qdrant Cloud pricing scales with storage and read/write units (estimated at ~$0.10 per 100k vectors/month).

---

## Cost Calculations by Scale

### 1. Small Scale (100 Documents, 1,000 Questions/month)
- **Vector DB Size:** 100 docs * 5 chunks = 500 vectors.
- **Embedding Cost (One-time):** 250,000 tokens = **$0.01**
- **LLM Input Cost:** 1,000 queries * 500 tokens = 500k tokens = **$0.10**
- **LLM Output Cost:** 1,000 queries * 150 tokens = 150k tokens = **$0.09**
- **LLM Total:** **$0.19**
- **Vector DB Cost:** Self-hosted (Local) = **$0.00**
- **Total Estimated Monthly:** **~$0.20**

### 2. Medium Scale (10,000 Documents, 10,000 Questions/month)
- **Vector DB Size:** 10,000 docs * 5 chunks = 50,000 vectors.
- **Embedding Cost (One-time):** 25,000,000 tokens = **$0.50**
- **LLM Input Cost:** 10,000 queries * 500 tokens = 5M tokens = **$1.00**
- **LLM Output Cost:** 10,000 queries * 150 tokens = 1.5M tokens = **$0.90**
- **LLM Total:** **$1.90**
- **Vector DB Cost:** Self-hosted VPS = **$20.00**
- **Total Estimated Monthly:** **~$22.40**

### 3. Large Scale (100,000 Documents, 100,000 Questions/month)
- **Vector DB Size:** 100,000 docs * 5 chunks = 500,000 vectors.
- **Embedding Cost (One-time):** 250,000,000 tokens = **$5.00**
- **LLM Input Cost:** 100,000 queries * 500 tokens = 50M tokens = **$10.00**
- **LLM Output Cost:** 100,000 queries * 150 tokens = 15M tokens = **$9.00**
- **LLM Total:** **$19.00**
- **Vector DB Cost:** Larger VPS/Dedicated Server = **$200.00**
- **Total Estimated Monthly:** **~$224.00**

---

## Summary Table

| Scale | Documents | Questions/mo | Embedding Cost (One-time) | LLM Cost (Monthly) | Self-Hosted ChromaDB | Total Est. Monthly Cost |
|---|---|---|---|---|---|---|
| **Small** | 100 | 1,000 | $0.01 | $0.19 | $0 (Local) | **~$0.20** |
| **Medium**| 10,000 | 10,000 | $0.50 | $1.90 | $20 | **~$22.40** |
| **Large** | 100,000 | 100,000 | $5.00 | $19.00 | $200 | **~$224.00** |

---

## Managed Vector Database Comparison (At Large Scale)
At 500,000 vectors (Large Scale), a managed service like Pinecone Serverless would cost roughly **$50 - $100/month** for storage and queries. 
While this is cheaper than spinning up a dedicated $200/month VPS, the self-hosted option is chosen here because:
1. It offers complete data privacy (crucial for proprietary PDFs).
2. It avoids vendor lock-in.
3. The $20/month VPS easily handles the Medium scale with zero additional configuration.

## When to Switch Back to a Managed Database
You should switch from self-hosted ChromaDB to a managed database (like Pinecone, Qdrant, or Weaviate) if:
- **Scale exceeds 1 million vectors:** Self-hosting becomes expensive to maintain and requires manual sharding.
- **High Availability is required:** You need automated backups, multi-region replication, and a 99.9% uptime SLA.
- **Team lacks DevOps capacity:** If no engineer can manage the VPS, updates, and security patches, the engineering time cost outweighs the managed DB fee.