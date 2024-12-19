from flask import Flask, render_template, request, send_file, jsonify
from . import app
from splitter import *
import os

UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def splitter():
    if request.method == 'POST':
        try:
            uploaded_file = request.files.get('file')
            
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
            uploaded_file.save(file_path)

            reader = get_file(file_path)

            contents = find_index_page(reader)

            offset = get_page_offset(reader)

            chapters = find_chapter_pages(reader, contents, offset)

            zip_buffer = split_by_chapter(reader, chapters)

            # Return the ZIP file for download
            return send_file(zip_buffer, as_attachment=True, download_name="split_chapters.zip", mimetype='application/zip')

        except Exception as e:
            return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
        
        finally:
            if file_path and os.path.exists(file_path):
                os.remove(file_path)

    return render_template('splitter.html')

if __name__ == '__main__':
    app.run(debug=True)