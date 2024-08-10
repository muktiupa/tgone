import pdfplumber

# PDF file path
pdf_path = './stc.pdf'
# Output text file path
output_path = './extracted_text.txt'

# Open the PDF
with pdfplumber.open(pdf_path) as pdf:
    with open(output_path, 'w', encoding='utf-8') as txt_file:
        # Loop through each page
        for page in pdf.pages:
            # Extract text from the page
            text = page.extract_text()
            # Check if text is not None
            if text:
                # Write the extracted text to the text file
                txt_file.write(text)
                txt_file.write("\n")
            else:
                txt_file.write("No text found on this page.\n")
