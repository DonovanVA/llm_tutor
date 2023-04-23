# > pip install -r requirements.txt
# install gpt4all binaries here:https://the-eye.eu/public/AI/models/nomic-ai/gpt4all/
# Import necessary packages
from flask import Flask, request, jsonify
import os
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.document_loaders import TextLoader
from langchain.llms import LlamaCpp
from langchain.embeddings import LlamaCppEmbeddings
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# Define the path to the GPT4ALL model file
GPT4ALL_MODEL_PATH = "gpt4all-lora-quantized-ggml.bin"

# Define the directories and file names for the text documents and vector database
persist_directory = './.chroma'
collection_name = 'data'
document_name = './test_import.txt'

# Initialize the LlamaCppEmbeddings object using the GPT4ALL model
llama_embeddings = LlamaCppEmbeddings(model_path=GPT4ALL_MODEL_PATH)

# If the vector database does not exist, create it and persist it to disk
if not os.path.isdir(persist_directory):
    # Load the text documents
    print('Parsing ' + document_name)
    loader = TextLoader(document_name)
    documents = loader.load()

    # Split the text into chunks and create a Chroma vector store from them
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)
    vectordb = Chroma.from_documents(
        documents=texts, embedding=llama_embeddings, collection_name=collection_name, persist_directory=persist_directory)
    vectordb.persist()
    print(vectordb)
    print('Saved to ' + persist_directory)

# If the vector database already exists, load it from disk
else:
    print('Loading ' + persist_directory)
    vectordb = Chroma(persist_directory=persist_directory,
                      embedding_function=llama_embeddings, collection_name=collection_name)
    print(vectordb)

# Initialize the LlamaCpp model object
llm = LlamaCpp(model_path=GPT4ALL_MODEL_PATH)

# Initialize the RetrievalQA object using the LlamaCpp model and the Chroma vector store
qa = RetrievalQA.from_chain_type(
    llm=llm, chain_type="stuff", retriever=vectordb.as_retriever(search_kwargs={"k": 1}))

@app.route('/ask', methods=['POST'])
def ask_endpoint():
    question = request.json['question']
    answer = qa.run(question)
    return jsonify(answer=answer)

if __name__ == '__main__':
    app.run(port=5000)
