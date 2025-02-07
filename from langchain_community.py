from langchain_community.document_loaders import UnstructuredURLLoader

# List of URLs to scrape
urls = ["https://brainlox.com/courses/category/technical"]

# Load data from the URL
loader = UnstructuredURLLoader(urls=urls)
docs = loader.load()

# Save extracted data to a text file
with open("courses.txt", "w", encoding="utf-8") as f:
    for doc in docs:
        f.write(doc.page_content + "\n\n")

# Print success message
print("✅ Data saved to courses.txt")
# Print extracted text
# for doc in docs:
#     print(doc.page_content[:1000])  # Display only first 1000 characters

from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# Load the pre-trained sentence transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Extract the text content from the docs (assuming `docs` is already loaded from previous steps)
texts = [doc.page_content for doc in docs]

# Create embeddings using HuggingFaceEmbeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Create a vector store using FAISS
vector_store = FAISS.from_texts(texts, embeddings)

# Save the vector store to disk
vector_store.save_local("courses_vector_store")

# Print success message
print("✅ Embeddings created and saved in the vector store.")

from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# Load embeddings model
model_name = "sentence-transformers/all-MiniLM-L6-v2"
embeddings = HuggingFaceEmbeddings(model_name=model_name)

# Load FAISS vector store with safe deserialization
vector_store = FAISS.load_local(
    "courses_vector_store",
    embeddings=embeddings,
    allow_dangerous_deserialization=True  # FIXED ✅
)

app = Flask(__name__)
api = Api(app)

class Conversation(Resource):
    def post(self):
        user_query = request.json.get('query')
        
        if not user_query:
            return jsonify({"message": "Query is required"}), 400
        
        results = vector_store.similarity_search(user_query, k=3)
        
        return jsonify({"query": user_query, "results": [result.page_content for result in results]})

api.add_resource(Conversation, '/conversation')

if __name__ == '__main__':
    app.run(debug=True)

