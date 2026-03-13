import os
# import for newer LangChain versions
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 1. Path Configuration
# Using absolute paths for consistency
data_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
chunk_folder = os.path.join(data_folder, "chunks")

# 2. Create the output directory if it doesn't exist
if not os.path.exists(chunk_folder):
    os.makedirs(chunk_folder)
    print(f"Created folder: {chunk_folder}")

# 3. Text Splitting Function
def split_text(text, chunk_size=500, chunk_overlap=50):
    """
    Splits long text into manageable pieces with overlap to maintain context.
    'separators' helps keep paragraphs and sentences together.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    return splitter.split_text(text)

# 4. Main Processing Loop
print("Starting text chunking process...")

for filename in os.listdir(data_folder):
    # Process only .txt files and avoid re-processing existing chunks
    if filename.endswith(".txt") and "_chunk_" not in filename:
        file_path = os.path.join(data_folder, filename)
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

            # Generate chunks
            chunks = split_text(text)
            print(f"Processing '{filename}': Created {len(chunks)} chunks.")

            # Save each chunk as a unique file
            base_name = filename.replace('.txt', '')
            for i, chunk in enumerate(chunks):
                chunk_filename = f"{base_name}_chunk_{i+1}.txt"
                chunk_path = os.path.join(chunk_folder, chunk_filename)
                
                with open(chunk_path, "w", encoding="utf-8") as cf:
                    cf.write(chunk)
                    
        except Exception as e:
            print(f"Error processing {filename}: {e}")

print("\nChunking complete! You can now run your embedding script.")