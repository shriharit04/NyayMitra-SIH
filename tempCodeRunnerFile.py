def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"  # Extract text from each page
    return text

# Example usage
pdf_path = "/Users/sreyaskv/Documents/SIH_project/Source_material/Constitution.pdf"
pdf_text = extract_text_from_pdf(pdf_path)

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(pdf_text)