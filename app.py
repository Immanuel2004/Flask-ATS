from flask import Flask,render_template,request,jsonify
from werkzeug.utils import secure_filename
import os
import mysql.connector
import subprocess
import json
from db_config import get_db_connector
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf','docx'}

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload',methods=['POST'])
def upload():
    name = request.form['name']
    email = request.form['email']
    job = request.form['job']
    file = request.files['resume']

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'],filename)
        file.save(filepath)

        result = subprocess.run(
            ['python','nlp/process_resume.py',filepath,job],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return jsonify({'error': 'NLP script failed', 'details': result.stderr}), 500

        try:
            nlp_output = json.loads(result.stdout)
        except json.JSONDecodeError as e:
            return jsonify({'error': 'Invalid JSON from NLP script', 'details': str(e)}), 500

        conn = get_db_connector()
        cursor = conn.cursor()
        cursor.execute("""
                       INSERT INTO applicants(name , email, job_id,resume_path)
                       VALUES (%s,%s,%s,%s)
                       """,(name,email,job,filepath))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify(nlp_output)
        
    return jsonify({'error':'Invalid File Format'})
    
if __name__ == '__main__':
    app.run(debug=True)