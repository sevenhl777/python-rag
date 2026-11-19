from pypdf import PdfReader
from docx import Document

def parser(content: bytes, filetype: str) -> str:
    text = ""
    if filetype == "pdf":
        # 以二进制写入模式打开，覆盖写入bytes
        with open("temp.pdf", "wb") as f:
            f.write(content)
        reader = PdfReader("temp.pdf")
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text == None:
                page_text = ""
            text = text + "\n" + page_text
    elif filetype == "docx":
        with open("temp.docx", "wb") as f:
            f.write(content)
        doc = Document("temp.docx")
        for para in doc.paragraphs:
            text = text + "\n" + para.text
    elif filetype in ["txt", "md"]:
        text = content.decode("utf-8")
    else:
        raise Exception("无法解析该类型文件")
    
    return text
 