from pypdf import PdfReader
from docx import Document as DocxDocument
from langchain_core.documents import Document

import hashlib

# todo：解析产出Document列表，带metadata可查页码、来源文件

def get_file_hash(content: bytes) -> list[Document]:
    return hashlib.md5(content).hexdigest()

def parser(content: bytes, filename: str) -> str:
    text = ""
    documents = []
    filehash = get_file_hash(content)
    filetype = filename.split(".")[-1].lower()
    
    if filetype == "pdf":
        # 以二进制写入模式打开，覆盖写入bytes
        with open("temp.pdf", "wb") as f:
            f.write(content)
        reader = PdfReader("temp.pdf")
        for page_no, page in enumerate(reader.pages, start=1):
            page_text = page.extract_text() or ""
            documents.append(
                Document(
                    page_content = page_text,
                    metadata={
                        "source": filename,
                        "page": page_no,
                        "file_hash": filehash
                    }
                )
            )
    elif filetype == "docx":
        with open("temp.docx", "wb") as f:
            f.write(content)
        doc = DocxDocument("temp.docx")
        for para in doc.paragraphs:
            text = text + "\n" + para.text
        documents.append(Document(
            page_content = text,
            metadata = {
                "source": filename,
                "page": 1,
                "file_hash": filehash
            }
        ))
    elif filetype in ["txt", "md"]:
        text = content.decode("utf-8")
        documents.append(Document(
            page_content = text,
            metadata = {
                "source": filename,
                "page": 1,
                "file_hash": filehash
            }
        ))
    else:
        raise Exception("无法解析该类型文件")
    
    return documents
 