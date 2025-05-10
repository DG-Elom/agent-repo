from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
import weaviate
import os
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

doc = """
Aujourd'hui j'ai appris à générer un PDF à partir d'un Markdown.
Je pense que ce sera utile pour automatiser les bilans hebdos.
Prochaine étape : connecter ça à un webhook Telegram pour envoi auto.
"""

splitter = RecursiveCharacterTextSplitter(chunk_size=512)
chunks = splitter.split_text(doc)

client = weaviate.Client("http://localhost:8080")
embedding = OpenAIEmbeddings(openai_api_key=openai_api_key)
for chunk in chunks:
    vector = embedding.embed_query(chunk)
    client.data_object.create(
        data_object={"text": chunk},
        class_name="Memo",
        vector=vector
    )