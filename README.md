# Cyber Career RAG Assistant

## Overview

Cyber Career RAG Assistant is a Retrieval-Augmented Generation system designed to help entry-level IT and cybersecurity candidates search across career, certification, workforce, and portfolio documents.

The system answers plain-language questions such as:

* What skills are important for entry-level cybersecurity roles?
* What topics does Security+ cover?
* What does CCNA focus on?
* What portfolio projects should a beginner build?
* What is the difference between information security analyst and computer support specialist roles?

Instead of relying only on the language model’s general knowledge, the system retrieves relevant passages from collected documents first, then generates a grounded response using that context.

---

## Problem Statement

Cybersecurity career guidance is spread across many different sources: certification objectives, workforce frameworks, labor statistics, cyber career pathway tools, and practical portfolio advice. For someone trying to break into IT or cybersecurity, it can be difficult to understand what to prioritize.

This project makes that information searchable by combining document ingestion, chunking, embeddings, semantic search, and grounded LLM response generation.

---

## Domain

The domain for this project is cybersecurity and IT career guidance for entry-level candidates transitioning into roles such as:

* Help Desk Technician
* IT Support Specialist
* SOC Analyst
* Cybersecurity Analyst
* Vulnerability Analyst
* Incident Response Analyst

This knowledge is valuable because official documents often exist separately and are not easy to compare side by side. A RAG assistant can retrieve relevant information from multiple sources and provide a grounded answer with citations.

---

## Document Sources

This project uses 10 source documents stored in the `docs/` folder:

1. `security_plus_objectives.txt`
2. `ccna_exam_topics.txt`
3. `nice_framework_overview.txt`
4. `nice_incident_response_role.txt`
5. `nice_vulnerability_analysis_role.txt`
6. `cyberseek_career_pathways.txt`
7. `bls_information_security_analysts.txt`
8. `bls_computer_support_specialists.txt`
9. `portfolio_lab_guide.txt`
10. `resume_keywords_and_skill_map.txt`

The documents cover certification topics, cybersecurity workforce roles, labor market guidance, beginner portfolio projects, and resume keywords.

A `SOURCE_LIST.md` file is included with the project to document where the collected source documents came from.

---

## Required Features Implemented

* Document ingestion pipeline
* Text cleaning and preprocessing
* Chunking with overlap
* Embeddings using `sentence-transformers`
* Vector storage with ChromaDB
* Semantic retrieval with distance scores
* Grounded response generation using Groq LLM
* Source attribution in responses
* Basic query interface
* Evaluation report with 5 test questions
* Failure case analysis

---

## Tech Stack

| Component             | Tool                           |
| --------------------- | ------------------------------ |
| Language              | Python                         |
| Embeddings            | `sentence-transformers`        |
| Embedding Model       | `all-MiniLM-L6-v2`             |
| Vector Store          | ChromaDB                       |
| LLM                   | Groq `llama-3.3-70b-versatile` |
| Interface             | Gradio                         |
| Environment Variables | `.env`                         |

---

## Architecture

```text
User Documents
     ↓
Document Ingestion
(load .txt files from docs/)
     ↓
Cleaning
(remove extra whitespace, formatting noise, and non-content text)
     ↓
Chunking
(character-based chunks with overlap)
     ↓
Embedding
(sentence-transformers: all-MiniLM-L6-v2)
     ↓
Vector Store
(ChromaDB with source metadata)
     ↓
Retrieval
(top-k semantic search with distance scores)
     ↓
Generation
(Groq LLM with grounded prompt)
     ↓
User Interface
(Gradio app with answer and source attribution)
```

---

## Document Ingestion Pipeline

The ingestion pipeline loads all `.txt` files from the `docs/` folder. Each document is read into memory, cleaned, and stored with metadata such as the source filename.

The pipeline keeps the actual career, certification, skill, and portfolio content while avoiding unnecessary text such as navigation menus, ads, repeated boilerplate, or unrelated formatting artifacts.

Each loaded document is represented with:

```python
{
    "source": "security_plus_objectives.txt",
    "text": "cleaned document text..."
}
```

---

## Chunking Strategy

The project uses a deliberate chunking strategy instead of blindly splitting every document without reasoning.

Current chunking approach:

```text
Chunk size: 500 characters
Overlap: 100 characters
Minimum chunk length: 50 characters
```

This chunk size was chosen because the documents include certification objectives, workforce role descriptions, career guidance, and skill lists. A 500-character chunk is large enough to preserve a complete idea, such as a certification domain or job skill explanation, but small enough to support targeted retrieval.

The 100-character overlap helps preserve context when an important idea spans across two adjacent chunks.

### Why not smaller chunks?

If chunks are too small, they may lose important context. For example, a chunk might mention “incident response” but omit the explanation of what tasks are involved.

### Why not larger chunks?

If chunks are too large, they may contain too many unrelated topics. This can make retrieval less precise because a single chunk may discuss certifications, job titles, skills, and portfolio projects all at once.

---

## Sample Chunks

Below are representative examples of the types of chunks this system creates.

### Sample Chunk 1

Source: `security_plus_objectives.txt`

```text
Security+ covers foundational cybersecurity concepts including threats, vulnerabilities, architecture, operations, and security program management. These topics help entry-level candidates understand how organizations protect systems and respond to risks.
```

### Sample Chunk 2

Source: `ccna_exam_topics.txt`

```text
CCNA focuses on networking fundamentals, IP connectivity, network access, IP services, security fundamentals, automation, and programmability. These skills are useful for IT support, network administration, and cybersecurity roles.
```

### Sample Chunk 3

Source: `nice_incident_response_role.txt`

```text
Incident response work involves identifying, analyzing, and responding to cybersecurity events. Tasks may include reviewing logs, documenting incidents, escalating findings, and supporting recovery actions.
```

### Sample Chunk 4

Source: `portfolio_lab_guide.txt`

```text
Useful beginner cybersecurity portfolio projects include Nmap scanning, Wireshark packet analysis, vulnerability analysis, SOC alert triage, SIEM log analysis, and incident response writeups.
```

### Sample Chunk 5

Source: `resume_keywords_and_skill_map.txt`

```text
Common entry-level cybersecurity resume keywords include ticketing systems, troubleshooting, Active Directory, networking, TCP/IP, DNS, DHCP, VPN, SIEM, log analysis, vulnerability scanning, and incident response.
```

---

## Embedding Model

This project uses:

```text
sentence-transformers/all-MiniLM-L6-v2
```

This model was selected because it runs locally, is lightweight, and does not require a paid embedding API. It provides a practical balance between performance and accessibility for a student project.

For a production system, I would compare embedding models based on:

* Retrieval accuracy
* Cost
* Latency
* Context length
* Multilingual support
* Performance on cybersecurity and career-specific language
* Local model vs. API-based model tradeoffs

---

## Vector Store and Retrieval

The project uses ChromaDB as a local vector database.

Each chunk is stored with:

* Chunk text
* Source filename
* Chunk ID
* Embedding vector

When a user asks a question, the system embeds the query and compares it against the stored document embeddings. It retrieves the top matching chunks using semantic similarity search.

The retrieval function returns:

```python
{
    "text": "retrieved chunk text",
    "source": "source_document.txt",
    "distance": 0.32
}
```

Lower distance scores indicate stronger semantic similarity.

---

## Retrieval Test Results

### Retrieval Test 1

Question:

```text
What topics does Security+ cover?
```

Expected relevant source:

```text
security_plus_objectives.txt
```

Top retrieved chunks should mention cybersecurity concepts, threats, vulnerabilities, security architecture, operations, and program management.

Relevance judgment: Accurate if the top chunks come from the Security+ document and describe Security+ domains.

---

### Retrieval Test 2

Question:

```text
What does CCNA focus on?
```

Expected relevant source:

```text
ccna_exam_topics.txt
```

Top retrieved chunks should mention networking fundamentals, IP connectivity, network access, IP services, security fundamentals, and automation.

Relevance judgment: Accurate if the retrieved chunks are from the CCNA document and explain networking topics.

---

### Retrieval Test 3

Question:

```text
What portfolio projects are useful for beginner cybersecurity candidates?
```

Expected relevant source:

```text
portfolio_lab_guide.txt
```

Top retrieved chunks should mention Nmap, Wireshark, SIEM/log analysis, vulnerability scanning, SOC alert triage, or incident response reports.

Relevance judgment: Accurate if retrieved chunks directly support beginner portfolio project recommendations.

---

## Grounded Generation

The system uses a grounding prompt to prevent the LLM from answering from general knowledge.

The prompt instructs the model to:

* Answer only using retrieved document context
* Avoid outside knowledge or assumptions
* Cite the source document used
* Refuse to answer if the collected documents do not contain enough information

Example grounding instruction:

```text
You are Cyber Career RAG Assistant. Answer the user's question using only the retrieved document context. Do not use outside knowledge, assumptions, or general career advice. If the answer is not clearly supported by the provided context, say: "I do not have enough information in the collected documents to answer that." Cite the source document used for your answer.
```

This helps reduce hallucinations and makes the response easier to verify.

---

## Query Interface

The project includes a basic query interface built with Gradio.

The interface allows a user to:

1. Enter a career-related cybersecurity question.
2. Submit the query.
3. View a grounded answer.
4. See which source documents were used.

Example interaction:

Question:

```text
What skills are important for entry-level cybersecurity roles?
```

Response:

```text
According to resume_keywords_and_skill_map.txt and nice_framework_overview.txt, entry-level cybersecurity roles commonly require networking fundamentals, troubleshooting, documentation, security concepts, vulnerability awareness, incident response basics, and log analysis.
```

Sources:

```text
resume_keywords_and_skill_map.txt
nice_framework_overview.txt
```

---

## Example Responses

### Example 1

Question:

```text
What topics does Security+ cover?
```

Answer:

```text
According to security_plus_objectives.txt, Security+ covers general security concepts, threats and vulnerabilities, security architecture, security operations, and security program management.
```

Sources:

```text
security_plus_objectives.txt
```

---

### Example 2

Question:

```text
What portfolio projects should a beginner cybersecurity candidate build?
```

Answer:

```text
According to portfolio_lab_guide.txt, useful beginner cybersecurity portfolio projects include Nmap scanning, Wireshark packet analysis, vulnerability analysis, SOC alert triage, SIEM log analysis, and incident response writeups.
```

Sources:

```text
portfolio_lab_guide.txt
```

---

### Out-of-Scope Example

Question:

```text
What certification is personally best for me based on my exact background?
```

Answer:

```text
I do not have enough information in the collected documents to answer that.
```

Reason:

The documents contain general career guidance, but they do not contain enough personal background information to make an individualized recommendation.

---

## Evaluation Report

### Evaluation Question 1

Question:

```text
What topics does Security+ cover?
```

Expected answer:

```text
Security+ covers security concepts, threats, vulnerabilities, architecture, operations, and security program management.
```

System response:

```text
According to security_plus_objectives.txt, Security+ covers general security concepts, threats and vulnerabilities, security architecture, security operations, and security program management.
```

Retrieved chunks:

```text
security_plus_objectives.txt
```

Accuracy:

```text
Accurate
```

Explanation:

The system retrieved the correct Security+ source document and generated an answer supported by the retrieved context.

---

### Evaluation Question 2

Question:

```text
What does CCNA focus on?
```

Expected answer:

```text
CCNA focuses on networking fundamentals, IP connectivity, network access, IP services, security fundamentals, and automation.
```

System response:

```text
According to ccna_exam_topics.txt, CCNA focuses on networking fundamentals, network access, IP connectivity, IP services, security fundamentals, and automation.
```

Retrieved chunks:

```text
ccna_exam_topics.txt
```

Accuracy:

```text
Accurate
```

Explanation:

The retrieved chunk directly matched the expected CCNA topic areas.

---

### Evaluation Question 3

Question:

```text
What portfolio projects are useful for beginner cybersecurity candidates?
```

Expected answer:

```text
Useful beginner projects include Nmap scanning, Wireshark packet analysis, vulnerability analysis, SOC alert triage, SIEM/log analysis, and incident response writeups.
```

System response:

```text
According to portfolio_lab_guide.txt, beginner cybersecurity candidates can build projects involving Nmap scanning, Wireshark packet analysis, vulnerability analysis, SOC alert triage, SIEM log analysis, and incident response reporting.
```

Retrieved chunks:

```text
portfolio_lab_guide.txt
```

Accuracy:

```text
Accurate
```

Explanation:

The system retrieved the correct portfolio guide and summarized the project recommendations accurately.

---

### Evaluation Question 4

Question:

```text
What is the difference between information security analysts and computer support specialists?
```

Expected answer:

```text
Information security analysts focus on protecting systems and responding to cyber threats, while computer support specialists focus on helping users and troubleshooting technical problems.
```

System response:

```text
According to bls_information_security_analysts.txt and bls_computer_support_specialists.txt, information security analysts focus on protecting computer systems and networks, while computer support specialists help users and organizations solve technical problems.
```

Retrieved chunks:

```text
bls_information_security_analysts.txt
bls_computer_support_specialists.txt
```

Accuracy:

```text
Accurate
```

Explanation:

The answer correctly used both BLS-related documents and clearly compared the two roles.

---

### Evaluation Question 5

Question:

```text
What skills are important for entry-level cybersecurity roles?
```

Expected answer:

```text
Important skills include networking fundamentals, troubleshooting, documentation, security concepts, vulnerability analysis, incident response basics, and log or SIEM analysis.
```

System response:

```text
According to resume_keywords_and_skill_map.txt and nice_framework_overview.txt, entry-level cybersecurity roles often require networking, troubleshooting, documentation, security fundamentals, vulnerability awareness, incident response basics, and log analysis.
```

Retrieved chunks:

```text
resume_keywords_and_skill_map.txt
nice_framework_overview.txt
```

Accuracy:

```text
Accurate
```

Explanation:

The response matches the expected skill areas and cites relevant source documents.

---

## Failure Case

Failure question:

```text
What is the best certification for me personally?
```

Expected behavior:

```text
The system should avoid giving a personalized recommendation unless the collected documents provide enough personal context.
```

System response:

```text
I do not have enough information in the collected documents to answer that.
```

Accuracy:

```text
Accurate refusal
```

Why this happened:

The system’s documents contain general career guidance, certification topics, and role descriptions, but they do not contain enough personal information about the user’s background, goals, budget, timeline, or experience level to make a fully personalized recommendation.

How to improve:

A future version could add a user profile intake form or allow the user to provide personal constraints such as current experience, certifications, target roles, timeline, and preferred learning style.

---

## Spec Reflection

One way the spec helped guide implementation was by forcing the project to define the domain, documents, chunking strategy, retrieval approach, and evaluation plan before writing code. This made the pipeline easier to build because each implementation step had a clear purpose.

One way the implementation diverged from the original plan was that the chunking approach remained relatively simple and character-based. A more advanced version could use paragraph-aware or heading-aware chunking to better preserve document structure, especially for certification objectives and role descriptions.

---

## AI Usage

AI tools were used to support implementation and documentation, but the system design decisions were reviewed and adjusted manually.

### AI Usage Example 1

I used AI assistance to help adapt a previous RAG lab structure into a cybersecurity career-focused RAG assistant. The AI helped identify which files needed to change, such as `ingest.py`, `retriever.py`, `generator.py`, and `app.py`.

I reviewed the output and adjusted the wording from board-game rule language to cybersecurity career document language.

### AI Usage Example 2

I used AI assistance to draft the grounded generation prompt. The AI suggested instructions to prevent the model from using outside knowledge. I kept the core grounding requirement but made sure the final prompt required source attribution and an explicit refusal when the documents did not support an answer.

---

## How to Run the Project

### 1. Clone the repository

```bash
git clone https://github.com/Jose-CyberSec/cyber-career-rag-assistant.git
cd cyber-career-rag-assistant
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Mac/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create `.env`

Copy `.env.example` to `.env`.

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Mac/Linux:

```bash
cp .env.example .env
```

Then add your Groq API key:

```text
GROQ_API_KEY=your_key_here
```

Do not commit `.env`.

### 5. Run the app

```bash
python app.py
```

Open the local URL shown in the terminal, usually:

```text
http://127.0.0.1:7860
```

---

## Security Note

This project uses a `.env` file for the Groq API key. The `.env` file should never be committed to GitHub.

The repo should include `.env.example` only.

---

## Future Improvements

Potential improvements include:

* Add metadata filtering by source type, such as certification, job outlook, workforce framework, or portfolio guide
* Compare semantic search against hybrid search with BM25
* Add a user profile form for more personalized career recommendations
* Add a larger evaluation set
* Improve chunking with heading-aware or paragraph-aware splitting
* Add source links directly in the UI
* Add confidence indicators based on retrieval distance scores

---

## Demo Video

Demo video link will be added after recording.

The demo will show:

* At least three different questions
* Source citations visible in the response
* One successful retrieval example
* One out-of-scope refusal
* A walkthrough of the evaluation report
