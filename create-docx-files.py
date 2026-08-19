import os 
from docx import Document

i = 4

# 1. Use 'os' to define and ensure the output directory exists
folder_path = "D:\\novel\\arcs\\arc-1\\"
os.makedirs(folder_path, exist_ok=True)

# 2. Define the full file path using os.path.join
for i in range(i, 101):
    file_name = f"chapter {i}.docx"
    full_path = os.path.join(folder_path, file_name)

    doc = Document()
    doc.add_heading(f"Chapter {i}", level=1)
    doc.save(full_path)


    print(f"Document successfully created at: {os.path.abspath(full_path)}")
    
        