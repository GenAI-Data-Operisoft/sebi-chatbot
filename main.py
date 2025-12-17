# import boto3
# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from langchain_community.embeddings import BedrockEmbeddings
# from langchain_community.vectorstores import FAISS
# from langchain_community.chat_models import BedrockChat

# VECTOR_DIR = "vectorstore"

# # ---------- AWS Clients ----------
# bedrock_runtime = boto3.client(
#     "bedrock-runtime",
#     region_name="ap-south-1"
# )

# # ---------- FastAPI App ----------
# app = FastAPI(
#     title="FAISS + Bedrock QA API",
#     version="1.0.0"
# )

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ---------- Request / Response ----------
# class QuestionRequest(BaseModel):
#     question: str
#     top_k: int = 4


# class AnswerResponse(BaseModel):
#     answer: str


# # ---------- Load FAISS ONCE ----------
# embeddings = BedrockEmbeddings(
#     client=bedrock_runtime,
#     model_id="amazon.titan-embed-text-v2:0"
# )

# try:
#     vectorstore = FAISS.load_local(
#         VECTOR_DIR,
#         embeddings,
#         allow_dangerous_deserialization=True
#     )
# except Exception as e:
#     raise RuntimeError(f"Failed to load FAISS index: {e}")


# # ---------- LLM ----------
# llm = BedrockChat(
#     client=bedrock_runtime,
#     model_id="anthropic.claude-3-haiku-20240307-v1:0",
#     model_kwargs={"temperature": 0}
# )


# # ---------- API Endpoint ----------
# @app.post("/ask", response_model=AnswerResponse)
# def ask_question(req: QuestionRequest):
#     docs = vectorstore.similarity_search(
#         req.question,
#         k=req.top_k
#     )

#     if not docs:
#         return {"answer": "Not found in document"}

#     context = "\n\n".join(
#         f"Source {i+1}:\n{doc.page_content}"
#         for i, doc in enumerate(docs)
#     )

#     prompt = f"""
# You are a helpful assistant.
# Answer the question strictly using the context below.
# If the answer is not present, say "Not found in document".

# Context:
# {context}

# Question:
# {req.question}

# Answer:
# """.strip()

#     try:
#         response = llm.invoke(prompt)
#         return {"answer": response.content}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))



import boto3
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_community.embeddings import BedrockEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_aws import ChatBedrock

VECTOR_DIR = "vectorstore"

# ---------- AWS Clients ----------
bedrock_runtime = boto3.client(
    "bedrock-runtime",
    region_name="ap-south-1"
)

# ---------- FastAPI App ----------
app = FastAPI(
    title="FAISS + Bedrock QA API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Request / Response ----------
class QuestionRequest(BaseModel):
    question: str
    top_k: int = 4


class AnswerResponse(BaseModel):
    answer: str


# ---------- Load FAISS ONCE ----------
embeddings = BedrockEmbeddings(
    client=bedrock_runtime,
    model_id="amazon.titan-embed-text-v2:0"
)

vectorstore = FAISS.load_local(
    VECTOR_DIR,
    embeddings,
    allow_dangerous_deserialization=True
)

# ---------- LLM ----------
llm = ChatBedrock(
    client=bedrock_runtime,
    model_id="global.anthropic.claude-opus-4-5-20251101-v1:0",
    model_kwargs={"temperature": 0}
)
print("It's claude-opus")
# ---------- Classifier Prompt ----------
CLASSIFIER_PROMPT = """
You are a classifier.

Decide whether the user question is:
- GENERAL: greetings, small talk, courtesy, casual conversation
- DOCUMENT: requires information from documents or policies

Reply with ONLY one word:
GENERAL or DOCUMENT

Question:
{question}

Answer:
""".strip()

# ---------- General Answer Prompt ----------
GENERAL_PROMPT = """
You are a helpful and friendly assistant.
Answer the user's question naturally.

Question:
{question}

Answer:
""".strip()


# ---------- API Endpoint ----------
@app.post("/ask", response_model=AnswerResponse)
def ask_question(req: QuestionRequest):
    try:
        # 1️⃣ Ask LLM: general or document?
        classification = llm.invoke(
            CLASSIFIER_PROMPT.format(question=req.question)
        ).content.strip().upper()

        # 2️⃣ If GENERAL → answer directly (NO FAISS)
        if classification == "GENERAL":
            response = llm.invoke(
                GENERAL_PROMPT.format(question=req.question)
            )
            return {"answer": response.content}

        # 3️⃣ DOCUMENT → FAISS search
        docs = vectorstore.similarity_search(
            req.question,
            k=req.top_k
        )

        if not docs:
            return {"answer": "Not found in document"}

        context = "\n\n".join(
            f"Source {i+1}:\n{doc.page_content}"
            for i, doc in enumerate(docs)
        )

        prompt = f"""
You are a helpful assistant.
Answer the question strictly using the context below.
If the answer is not present, say "Not found in document".

Context:
{context}

Question:
{req.question}

Answer:
""".strip()

        response = llm.invoke(prompt)
        return {"answer": response.content}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
