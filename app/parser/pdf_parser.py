import cv2
import os
import numpy as np
import pytesseract
import pandas as pd
from pdf2image import convert_from_path

# Step 1: Reading PDF Files
def read_pdf(pdf_file):
    if not os.path.exists(pdf_file):
        print(f"Error: File not found at {pdf_file}")
        return []
    pages = convert_from_path(pdf_file)
    return pages

# Step 2: Image Preprocessing - Deskewing the images
def deskew(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    coords = np.column_stack(np.where(gray > 0))
    angle = cv2.minAreaRect(coords)[-1]
    
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    return rotated

# Step 3: Running OCR using pytesseract
def extract_text_from_image(image):
    text = pytesseract.image_to_string(image)
    return text

# Step 4: Text Extraction with Additional Preprocessing
def process_page(page):
    try:
        # Convert PIL image to numpy array
        page_arr = np.array(page)
        
        # Deskew the page using the original color image
        page_deskew = deskew(page_arr)
        
        # Convert to grayscale after deskewing
        page_deskew_gray = cv2.cvtColor(page_deskew, cv2.COLOR_BGR2GRAY)
        
        # Extract text using pytesseract
        d = pytesseract.image_to_data(page_deskew_gray, output_type=pytesseract.Output.DICT)
        d_df = pd.DataFrame.from_dict(d)
        
        if d_df.empty:
            print("Warning: No text detected on the page.")
            return ""

        # Identify block numbers
        block_num = d_df.loc[d_df['level'] == 2, 'block_num'].max()
        
        # Identify header and footer
        header_index = d_df[d_df['block_num'] == 1].index.values
        footer_index = d_df[d_df['block_num'] == block_num].index.values
        
        # Extract relevant text excluding headers and footers
        text = ' '.join(d_df.loc[
            (d_df['level'] == 5) & 
            (~d_df.index.isin(header_index) & ~d_df.index.isin(footer_index)), 'text'
        ].values)
        
        return text.strip()
    except Exception as e:
        print(f"Error processing page: {e}")
        return ""

# Step 5: Extracting Text from Multiple Pages in a PDF
def extract_text_from_pdf_with_ocr(pdf_file):
    # Read the PDF and convert it to images
    pages = read_pdf(pdf_file)
    if not pages:
        return "Error: No pages found in the PDF."

    extracted_text = [process_page(page) for page in pages]
    
    return '\n'.join(filter(None, extracted_text))  # Remove empty text entries


