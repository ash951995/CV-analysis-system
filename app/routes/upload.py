from flask import Blueprint, request, jsonify,render_template,current_app
from werkzeug.utils import secure_filename
import os
import logging
import json

# Import the db instance directly from app.py
from app import db
from app.llm_operations.llm import get_resume_analysis
from app.llm_operations.llm_query import query_cv_data
from app.db_operations import save_candidate
from app.parser.pdf_parser import extract_text_from_pdf_with_ocr
from app.parser.docx_parser import extract_text_from_docx

upload_bp = Blueprint('upload', __name__)

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

UPLOAD_FOLDER = "uploads/"
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route("/", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'})
        if file and file.filename.lower().endswith('.pdf'):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            # Extract text based on file type
            text = ""
            if filename.endswith(".pdf"):
                text = extract_text_from_pdf_with_ocr(filepath)
                logger.info(f"Extracted text from PDF: {len(text)} characters")
            elif filename.endswith(".docx"):
                text = extract_text_from_docx(filepath)
                logger.info(f"Extracted text from DOCX: {len(text)} characters")
            else:
                return jsonify({"error": "Unsupported file format"}), 400           

            if text:
                # Process the extracted text synchronously
                try:
                    structured_data = get_resume_analysis(text)
                    # Ensure structured_data is a dictionary
                    if isinstance(structured_data, str):  
                        structured_data = json.loads(structured_data)  # Convert JSON string to dictionary

                    logger.info(f"Successfully analyzed resume data")                   
                    
                    # Create and save Resume object
                    if structured_data:
                        save_candidate(filename,text,structured_data)
                        # Debugging: Log template path
                        template_path = os.path.join(current_app.root_path, 'templates', 'index.html') # app.root_path gets the root of the app.
                        logger.info(f"Attempting to render template at: {template_path}")

                        # Debugging: Check if template file exists
                        if not os.path.exists(template_path):
                            logger.error(f"Template not found at: {template_path}")
                        return render_template('index.html')
                        
                    else:
                        return jsonify({'error': 'Failed to analyze CV'})                  
                    

                except Exception as e:
                    logger.error(f"Error in processing resume: {str(e)}")
                    return jsonify({"error": f"An error occurred while processing the resume: {str(e)}"}), 500

                
            else:
                return jsonify({'error': 'Failed to extract text from CV'})
        else:
            return jsonify({'error': 'Unsupported file type'})

    

@upload_bp.route('/query', methods=['POST'])
def query():
    """Handles user queries and returns the chatbot response."""
    data = request.get_json()
    query_text = data.get('query')
    if query_text:
        response = query_cv_data(query_text)
        return jsonify({'response': response})
    return jsonify({'error': 'No query provided'})



def upload_resume():
    """
    Uploads a resume, extracts text, and processes it synchronously.
    """
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]

        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            logger.info(f"Saving file to: {file_path}")
            file.save(file_path)

            # Extract text based on file type
            text = ""
            if filename.endswith(".pdf"):
                text = extract_text_from_pdf_with_ocr(file_path)
                logger.info(f"Extracted text from PDF: {len(text)} characters")
            elif filename.endswith(".docx"):
                text = extract_text_from_docx(file_path)
                logger.info(f"Extracted text from DOCX: {len(text)} characters")
            else:
                return jsonify({"error": "Unsupported file format"}), 400

            # Process the extracted text synchronously
            try:
                structured_data = get_resume_analysis(text)
                # Ensure structured_data is a dictionary
                if isinstance(structured_data, str):  
                    structured_data = json.loads(structured_data)  # Convert JSON string to dictionary

                logger.info(f"Successfully analyzed resume data")

                
                
                # Create and save Resume object
                save_candidate(filename,text,structured_data)
                
                

            except Exception as e:
                logger.error(f"Error in processing resume: {str(e)}")
                return jsonify({"error": f"An error occurred while processing the resume: {str(e)}"}), 500

            return jsonify({
                "message": "File uploaded and processed successfully",
                "filename": filename
            }), 200

        return jsonify({"error": "Invalid file format"}), 400
    
    except Exception as e:
        logger.error(f"Error in file upload: {str(e)}")
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500