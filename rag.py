import os
import json
from langchain.document_loaders import JSONLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import HuggingFaceHub
from langchain.schema import Document

# Step 1: Load JSON files as documents
def load_json_documents(file_paths):
    docs = []
    for path in file_paths:
        with open(path, 'r') as f:
            data = json.load(f)
            docs.append(Document(page_content=json.dumps(data)))
    return docs

file_paths = [
    "data/file1.json",
    "data/file2.json",
    "data/file3.json",
    "data/file4.json",
    "data/file5.json",
]

documents = load_json_documents(file_paths)

# Step 2: Create Embeddings using HuggingFace
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Step 3: Create FAISS vectorstore
vectorstore = FAISS.from_documents(documents, embedding_model)

# Step 4: Initialize HuggingFace LLM
llm = HuggingFaceHub(repo_id="google/flan-t5-base", model_kwargs={"temperature": 0.5, "max_length": 512})

# Step 5: Build RetrievalQA Chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
    return_source_documents=True
)

# Step 6: Ask Questions
query = "What is the key information present in these documents?"
result = qa_chain({"query": query})

print("Answer:", result["result"])
print("Sources:")
for doc in result["source_documents"]:
    print(doc.metadata)
