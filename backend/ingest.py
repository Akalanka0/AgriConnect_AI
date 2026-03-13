import os
from pypdf import PdfReader

# Step 1: Path to the data folder
# Using absolute path for consistency
data_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))

# Step 2: Iterate over all PDF files
documents = []

if not os.path.exists(data_folder):
    print(f"Error: The folder {data_folder} does not exist!")
else:
    for filename in os.listdir(data_folder):
        if filename.endswith(".pdf"):
            file_path = os.path.join(data_folder, filename)
            print(f"Reading {filename} ...")
            
            try:
                # Step 3 & 4: Open PDF and extract text
                pdf = PdfReader(file_path)
                text = ""
                for page in pdf.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
                
                # Step 5: Store in memory
                documents.append({"file": filename, "text": text})
            except Exception as e:
                print(f"Could not read {filename}: {e}")

    print("All documents converted to text!")
    print(f"Total documents processed: {len(documents)}")

    # Step 6: Save to .txt files
    for doc in documents:
        # Changes "report.pdf" to "report.txt"
        text_filename = doc["file"].replace(".pdf", ".txt")
        text_file_path = os.path.join(data_folder, text_filename)
        
        with open(text_file_path, "w", encoding="utf-8") as f:
            f.write(doc["text"])
        print(f"Saved: {text_filename}")