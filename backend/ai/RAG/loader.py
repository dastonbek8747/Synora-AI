from langchain_community.document_loaders import PyPDFLoader, UnstructuredWordDocumentLoader, CSVLoader, \
    UnstructuredExcelLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=700,
    chunk_overlap=100
)


def document_loader(filename: str):
    file_type = filename.split(".")[-1]
    if file_type == "pdf":
        loader = PyPDFLoader(file_path=f"./Files/{filename}")
        return loader.load()
    elif file_type == "xlsx" or file_type == "xls":
        loader = UnstructuredExcelLoader(file_path=f"./Files/{filename}")
        return loader.load()
    elif file_type == "csv":
        loader = CSVLoader(file_path=f"./Files/{filename}")
        return loader.load()
    elif file_type == "txt":
        loader = TextLoader(file_path=f"./Files/{filename}")
        return loader.load()
    elif file_type == "doc" or file_type == "docx":
        loader = UnstructuredWordDocumentLoader(file_path=f"./Files/{filename}")
        return loader.load()
    else:
        return []


def get_split_docs(filename: str):
    docs = document_loader(filename)
    return splitter.split_documents(documents=docs)

