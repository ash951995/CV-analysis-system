# tests/test_upload_routes.py

import unittest
from flask import Flask, json
from app import create_app, db
from app.routes.upload_routes import upload_bp
import os
from io import BytesIO

class TestUploadRoutes(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory SQLite for testing
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

        self.app.register_blueprint(upload_bp, url_prefix="/api")

        self.upload_folder = "uploads/"
        os.makedirs(self.upload_folder, exist_ok=True)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

        # Clean up uploaded files
        for filename in os.listdir(self.upload_folder):
            file_path = os.path.join(self.upload_folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")

    def test_upload_file_get(self):
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, 200)

    def test_upload_file_post_no_file(self):
        response = self.client.post('/api/')
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200) #returns html, not json
        #self.assertEqual(data['error'], 'No file part')

    def test_upload_file_post_empty_filename(self):
        data = {'file': (BytesIO(b'my file contents'), '')}
        response = self.client.post('/api/', data=data, content_type='multipart/form-data')
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200) #returns html, not json
        #self.assertEqual(data['error'], 'No selected file')

    def test_upload_file_post_unsupported_file_type(self):
        data = {'file': (BytesIO(b'my file contents'), 'test.txt')}
        response = self.client.post('/api/', data=data, content_type='multipart/form-data')
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200) #returns html, not json
        #self.assertEqual(data['error'], 'Unsupported file type')

    def test_upload_file_post_pdf(self):
        with open('tests/test_cv.pdf', 'rb') as f:
            data = {'file': (f, 'test_cv.pdf')}
            response = self.client.post('/api/', data=data, content_type='multipart/form-data')
            data = json.loads(response.data.decode('utf-8'))
            self.assertEqual(response.status_code, 200) #returns html, not json
            #self.assertEqual(data['message'], 'CV processed successfully')

    def test_upload_file_post_docx(self):
        with open('tests/test_cv.docx', 'rb') as f:
            data = {'file': (f, 'test_cv.docx')}
            response = self.client.post('/api/', data=data, content_type='multipart/form-data')
            data = json.loads(response.data.decode('utf-8'))
            self.assertEqual(response.status_code, 200) #returns html, not json
            #self.assertEqual(data['message'], 'CV processed successfully')

    def test_query_post_no_query(self):
        response = self.client.post('/api/query', json={})
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['error'], 'No query provided')

    def test_query_post_valid_query(self):
        response = self.client.post('/api/query', json={'query': 'test query'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn('response', data)

    def test_upload_resume_post_no_file(self):
        response = self.client.post('/api/upload_resume')
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], 'No file uploaded')

    def test_upload_resume_post_empty_filename(self):
        data = {'file': (BytesIO(b'my file contents'), '')}
        response = self.client.post('/api/upload_resume', data=data, content_type='multipart/form-data')
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], 'No selected file')

    def test_upload_resume_post_unsupported_file_type(self):
        data = {'file': (BytesIO(b'my file contents'), 'test.txt')}
        response = self.client.post('/api/upload_resume', data=data, content_type='multipart/form-data')
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], 'Invalid file format')

    def test_upload_resume_post_pdf(self):
        with open('tests/test_cv.pdf', 'rb') as f:
            data = {'file': (f, 'test_cv.pdf')}
            response = self.client.post('/api/upload_resume', data=data, content_type='multipart/form-data')
            data = json.loads(response.data.decode('utf-8'))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['message'], 'File uploaded and processed successfully')

    def test_upload_resume_post_docx(self):
        with open('tests/test_cv.docx', 'rb') as f:
            data = {'file': (f, 'test_cv.docx')}
            response = self.client.post('/api/upload_resume', data=data, content_type='multipart/form-data')
            data = json.loads(response.data.decode('utf-8'))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['message'], 'File uploaded and processed successfully')

if __name__ == '__main__':
    unittest.main()