import os
import gc
import boto3
from pdf2image import convert_from_path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import BedrockEmbeddings

PDF_DIR = "data"
IMAGE_DIR = "images"
TEXT_DIR = "textract_text"
VECTOR_DIR = "vectorstore"

os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(TEXT_DIR, exist_ok=True)

textract = boto3.client("textract", region_name="ap-south-1")
bedrock_runtime = boto3.client("bedrock-runtime", region_name="ap-south-1")


def process_pdf(pdf_path):
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]

    # LOWER DPI = BIG MEMORY WIN
    images = convert_from_path(pdf_path, dpi=200)

    for i, img in enumerate(images):
        img_path = f"{IMAGE_DIR}/{pdf_name}_page_{i}.png"
        txt_path = f"{TEXT_DIR}/{pdf_name}_page_{i}.txt"

        img.save(img_path, "PNG")

        with open(img_path, "rb") as f:
            response = textract.detect_document_text(
                Document={"Bytes": f.read()}
            )

        lines = [
            b["Text"]
            for b in response["Blocks"]
            if b["BlockType"] == "LINE"
        ]

        with open(txt_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        # 🔥 CRITICAL CLEANUP
        os.remove(img_path)
        del response, lines
        gc.collect()

    del images
    gc.collect()


def build_faiss():
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    embeddings = BedrockEmbeddings(
        client=bedrock_runtime,
        model_id="amazon.titan-embed-text-v2:0"
    )

    vectorstore = None

    for file in os.listdir(TEXT_DIR):
        if file.endswith(".txt"):
            with open(os.path.join(TEXT_DIR, file), "r", encoding="utf-8") as f:
                text = f.read().strip()

            if not text:
                continue

            docs = splitter.create_documents([text])

            if vectorstore is None:
                vectorstore = FAISS.from_documents(docs, embeddings)
            else:
                vectorstore.add_documents(docs)

            del docs, text
            gc.collect()

    vectorstore.save_local(VECTOR_DIR)
    print("✅ FAISS stored on disk (low memory)")


if __name__ == "__main__":
    for file in os.listdir(PDF_DIR):
        if file.endswith(".pdf"):
            process_pdf(os.path.join(PDF_DIR, file))

    build_faiss()
