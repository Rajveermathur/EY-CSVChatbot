from langchain_groq import ChatGroq
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chains import RetrievalQA
from langchain_huggingface import HuggingFaceEmbeddings
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)


# Initialize the LLM and embedding model
llm = ChatGroq(
    temperature=0.2,
    model="mixtral-8x7b-32768",
    api_key=os.environ['GROQ_API_KEY']
)
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

loader = CSVLoader(file_path=os.environ['FILE_NAME'])
index_creator = VectorstoreIndexCreator(embedding=embedding_model)
docsearch = index_creator.from_loaders([loader])
chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=docsearch.vectorstore.as_retriever(),
    input_key="question"
)

@app.route('/api/rag', methods=['POST'])
def answer_generation():
    try:
        data = request.get_json()
        question = data.get("question", "")
        
        # Generate response using the QA chain
        response = chain.invoke(question)
        answer = response['result']

        return jsonify({"answer": answer}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
