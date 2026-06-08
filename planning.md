# Cyber Career RAG Assistant Planning

## Domain

This project focuses on cybersecurity and IT career guidance for entry-level candidates transitioning into roles such as Help Desk Technician, IT Support Specialist, SOC Analyst, Cybersecurity Analyst, Incident Response Analyst, and Vulnerability Analyst.

This knowledge is valuable because cybersecurity career information is spread across certification guides, workforce frameworks, labor statistics, job role descriptions, and portfolio advice. Beginners often struggle to understand what skills, certifications, and projects to prioritize because the information is scattered across many sources.

## Documents

The project uses 10 source documents stored in the `docs/` folder:

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

These documents cover certification objectives, networking topics, cybersecurity workforce roles, labor market guidance, beginner portfolio projects, and resume keywords.

## Architecture

```text
User Documents
     ↓
Document Ingestion
(load .txt files from docs/)
     ↓
Cleaning
(remove extra whitespace and formatting noise)
     ↓
Chunking
(500-character chunks with 100-character overlap)
     ↓
Embedding
(sentence-transformers: all-MiniLM-L6-v2)
     ↓
Vector Store
(ChromaDB with source metadata)
     ↓
Retrieval
(top-4 semantic search with distance scores)
     ↓
Generation
(Groq llama-3.3-70b-versatile with grounded prompt)
     ↓
User Interface
(Gradio app with answer and source attribution)
```

## Chunking Strategy

I will use character-based chunking with a target size of 500 characters and 100 characters of overlap. The documents include certification objectives, job role descriptions, workforce frameworks, skill lists, and portfolio guidance, so chunks need to be large enough to preserve complete ideas but small enough to retrieve specific information.

The 100-character overlap helps preserve context when important information spans across two adjacent chunks. If chunks are too small, they may lose important context. If chunks are too large, they may include unrelated information and make retrieval less precise.

## Retrieval Approach

I will use `sentence-transformers` with the `all-MiniLM-L6-v2` embedding model and ChromaDB as the vector store. The system will retrieve the top 4 chunks for each query.

Retrieving too few chunks could miss important context. Retrieving too many chunks could add loosely related information and distract the LLM. Semantic search is useful because users may ask questions using different wording than the documents, but embeddings can still match related meanings.

For production, I would compare embedding models based on retrieval accuracy, cost, latency, context length, multilingual support, and performance on cybersecurity-specific language.

## Evaluation Plan

1. Question: What topics does Security+ cover?
   Expected answer: Security+ covers security concepts, threats, vulnerabilities, architecture, operations, and security program management.

2. Question: What does CCNA focus on?
   Expected answer: CCNA focuses on networking fundamentals, network access, IP connectivity, IP services, security fundamentals, and automation.

3. Question: What portfolio projects are useful for beginner cybersecurity candidates?
   Expected answer: Useful projects include Nmap scanning, Wireshark packet analysis, vulnerability analysis, SOC alert triage, SIEM/log analysis, and incident response writeups.

4. Question: What is the difference between information security analysts and computer support specialists?
   Expected answer: Information security analysts focus on protecting systems and responding to cyber threats, while computer support specialists help users and organizations solve technical problems.

5. Question: What skills are important for entry-level cybersecurity roles?
   Expected answer: Important skills include networking fundamentals, troubleshooting, documentation, security concepts, vulnerability analysis, incident response basics, and log or SIEM analysis.

## Anticipated Challenges

One challenge is that the documents come from different source types. Certification objectives, workforce frameworks, and resume keyword lists are structured differently, so chunking may not work equally well for every document.

Another challenge is source attribution. If metadata is not attached correctly to each chunk, the system may generate an answer without clearly showing which document supported it.

A third challenge is over-answering. The LLM may try to provide general career advice if the grounding prompt is weak, so the prompt must clearly instruct the model to answer only from retrieved context.

## AI Tool Plan

I will use AI tools to help implement specific parts of the pipeline after writing this plan. For ingestion, I will provide the Documents and Chunking Strategy sections and ask for help implementing a loader and chunking function. For retrieval, I will provide the Retrieval Approach section and ask for help implementing ChromaDB storage and semantic search. For generation, I will provide the grounding requirements and ask for help writing a prompt that forces the LLM to answer only from retrieved documents and cite sources.

I will review and modify any generated code to make sure it matches the project requirements.
