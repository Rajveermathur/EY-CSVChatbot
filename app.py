from langchain_groq import ChatGroq
from langchain.document_loaders import CSVLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chains import RetrievalQA
from langchain_community.embeddings import HuggingFaceEmbeddings

llm = ChatGroq(
    temperature=0,
    model="mixtral-8x7b-32768",
    api_key="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" # Optional if not set as an environment variable
)

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

loader = CSVLoader(file_path='ai4i2020.csv')
index_creator = VectorstoreIndexCreator(embedding=embedding_model)
docsearch = index_creator.from_loaders([loader])

chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=docsearch.vectorstore.as_retriever(), input_key="question", verbose=True)

query = "Number of rows?"
response = chain.invoke(query)
print(response['result'])