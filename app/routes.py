from flask import Flask, render_template, request, send_file, jsonify
from . import app
from splitter import *
import os

UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def splitter():
    if request.method == 'POST':
        try:
            # Check if file is uploaded
            uploaded_file = request.files.get('file')
            if not uploaded_file or uploaded_file.filename == '':
                return jsonify({"error": "No file uploaded"}), 400
            
            # Check if the uploaded file is a PDF
            if not uploaded_file.filename.lower().endswith('.pdf'):
                return jsonify({"error": "Invalid file format. Please upload a PDF file."}), 400

            # Save the uploaded file to the upload folder
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
            uploaded_file.save(file_path)

            # Process the PDF
            reader = get_file(file_path)
            if not reader:
                return jsonify({"error": "Failed to read the uploaded PDF"}), 400

            contents = find_index_page(reader)
            if contents is None:
                return jsonify({"error": "Contents page not found in the PDF"}), 400

            offset = get_page_offset(reader)
            if offset is None:
                return jsonify({"error": "Page offset could not be determined"}), 400

            chapters = find_chapter_pages(reader, contents, offset)
            if not chapters:
                return jsonify({"error": "No chapters found in the PDF"}), 400

            # Split and bundle into a ZIP file
            zip_buffer = split_by_chapter(reader, chapters)

            # Return the ZIP file for download
            return send_file(zip_buffer, as_attachment=True, download_name="split_chapters.zip", mimetype='application/zip')

        except Exception as e:
            # Handle unexpected errors gracefully
            return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

    # Render the upload form for GET requests
    return render_template('splitter.html')

if __name__ == '__main__':
    app.run(debug=True)