import PyPDF2
import re
import json

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text

def save_text_to_file(text, file_path):
    with open(file_path, 'w', encoding='utf-8') as text_file:
        text_file.write(text)

def save_text_to_json(text, file_path):
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump({"extracted_text": text}, json_file, ensure_ascii=False, indent=4)

def extract_information(text):
    extracted_info = {}

    # Extract PNR
    pnr_match = re.search(r'PNR\s*:\s*(\w+)', text, re.DOTALL)
    extracted_info['PNR'] = pnr_match.group(1) if pnr_match else 'N/A'
    
    # Extract names
    names = re.findall(r'(Mr|Ms)\s*([\w\s]+)', text, re.DOTALL)
    extracted_info['Names'] = [name[1].strip() for name in names] if names else []

    # Extract flight details
    flight_details = re.search(r'(\w+)\s*(Fri|Sat|Sun|Mon|Tue|Wed|Thu),\s*([\w\s]+)\s*Onward\s*\(Friends and Family\)\s*Operated by ([\w\s]+)', text, re.DOTALL)
    if flight_details:
        extracted_info['Flight Number'] = flight_details.group(1)
        extracted_info['Flight Date'] = flight_details.group(3)
        extracted_info['Airline'] = flight_details.group(4)
    else:
        extracted_info['Flight Number'] = 'N/A'
        extracted_info['Flight Date'] = 'N/A'
        extracted_info['Airline'] = 'N/A'

    # Extract origin and destination
    origin_dest = re.findall(r'(\w{3}),\s*([\w\s]+)', text, re.DOTALL)
    if len(origin_dest) >= 2:
        extracted_info['Origin'] = {
            "Code": origin_dest[0][0],
            "Name": origin_dest[0][1].strip()
        }
        extracted_info['Destination'] = {
            "Code": origin_dest[1][0],
            "Name": origin_dest[1][1].strip()
        }
    else:
        extracted_info['Origin'] = {
            "Code": 'N/A',
            "Name": 'N/A'
        }
        extracted_info['Destination'] = {
            "Code": 'N/A',
            "Name": 'N/A'
        }
    
    # Extract contact details
    contact_details = re.search(r'Contact No\.\s*([\+\d\-]+)\s*Email ID\s*([\w\.]+@[\w\.]+)', text, re.DOTALL)
    if contact_details:
        extracted_info['Contact Number'] = contact_details.group(1)
        extracted_info['Email ID'] = contact_details.group(2)
    else:
        extracted_info['Contact Number'] = 'N/A'
        extracted_info['Email ID'] = 'N/A'
    
    return extracted_info

def save_extracted_info_to_files(extracted_info, text_file_path, json_file_path):
    # Save extracted information to text file
    with open(text_file_path, 'w', encoding='utf-8') as text_file:
        for key, value in extracted_info.items():
            text_file.write(f"{key}: {value}\n")
    
    # Save extracted information to JSON file
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(extracted_info, json_file, ensure_ascii=False, indent=4)

pdf_path = "./stc.pdf"
text_file_path = "./extracted_text.txt"
json_file_path = "./extracted_text.json"
extracted_info_text_file_path = "./extracted_info.txt"
extracted_info_json_file_path = "./extracted_info.json"

# Extract text from PDF
extracted_text = extract_text_from_pdf(pdf_path)

# Save extracted text to text and JSON files
save_text_to_file(extracted_text, text_file_path)
save_text_to_json(extracted_text, json_file_path)

# Extract specific information from text
extracted_info = extract_information(extracted_text)

# Save extracted specific information to text and JSON files
save_extracted_info_to_files(extracted_info, extracted_info_text_file_path, extracted_info_json_file_path)

print(f"Extracted text has been saved to {text_file_path} and {json_file_path}")
print(f"Extracted information has been saved to {extracted_info_text_file_path} and {extracted_info_json_file_path}")
