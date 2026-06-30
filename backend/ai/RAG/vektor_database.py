from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from loader import get_split_docs

embedding = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-base")


def save_document_chroma(file_name, collection_name: str):
    docs = get_split_docs(file_name)
    db = Chroma.from_documents(
        documents=docs,
        collection_name=collection_name,
        embedding=embedding,
        persist_directory="./Chrome_db"
    )
    db.persist()
    return "Bazaga saqlandi"


def search_data_chroma(query: str, collection_name: str):
    db = Chroma(
        collection_name=collection_name,
        embedding_function=embedding,
        persist_directory="./Chrome_db"
    )
    reterviev = db.as_retriever(search_kwargs={"k": 5}, search_type="similarity")

    response_chroma = reterviev.invoke(query)

    return response_chroma


# save_document_chroma(collection_name="doston_sultonov", file_name="mexnat_kodeksi.pdf")
# print(search_data_chroma(query="1-modda", collection_name="doston_sultonov"))
