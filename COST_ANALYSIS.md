# Cost Analysis & Assumptions

**Assumptions:**
- Average document size: 2,500 tokens (~5 chunks of 500 tokens).
- Average query: 500 input tokens (context + question), 150 output tokens.
- Embedding cost: $0.02 per 1M tokens (using `all-MiniLM-L6-v2` hosted locally).
- LLM cost: $0.20 per 1M input tokens, $0.60 per 1M output tokens (Mistral Small API pricing).
- Vector DB cost: Self-hosted ChromaDB on a $20/month VPS (handles up to 1M vectors).

| Scale | Documents | Questions/mo | Embedding Cost (One-time) | LLM Cost (Monthly) | Vector DB Hosting | Total Est. Monthly Cost |
|---|---|---|---|---|---|---|
| **Small** | 100 | 1,000 | $0.01 | $0.19 | $0 (Local) | **~$0.20** |
| **Medium**| 10,000 | 10,000 | $0.50 | $1.90 | $20 | **~$22.40** |
| **Large** | 100,000 | 100,000 | $5.00 | $19.00 | $200 | **~$224.00** |

**LLM Math (Large Scale):**
Input: 100,000 queries * 500 tokens = 50M tokens. (50 * $0.20) = $10.00
Output: 100,000 queries * 150 tokens = 15M tokens. (15 * $0.60) = $9.00
Total LLM = $19.00