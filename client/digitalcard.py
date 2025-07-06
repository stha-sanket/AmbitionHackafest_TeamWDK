import os
import json
from flask import Flask, request, jsonify, render_template_string, redirect, url_for, session
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
app = Flask(_name_)
app.secret_key = 'super-secret'

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

# Homepage: Upload Image Page
HTML_FORM = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Gemini Discharge Summary Extractor</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f4f8fb; }
        .container { max-width: 420px; margin: 40px auto; background: #fff; border-radius: 12px; box-shadow: 0 4px 24px rgba(44,62,80,0.08); padding: 32px 24px 24px 24px; }
        h1 { color: #2c3e50; text-align: center; margin-bottom: 24px; }
        .upload-area { border: 2px dashed #a3bffa; border-radius: 8px; padding: 32px 16px; text-align: center; background: #f0f4ff; cursor: pointer; transition: border-color 0.2s; }
        .preview { margin: 18px 0 0 0; text-align: center; }
        .preview img { max-width: 100%; max-height: 180px; border-radius: 8px; box-shadow: 0 2px 8px rgba(44,62,80,0.08); }
        button[type="submit"] { width: 100%; background: #4f8cff; color: #fff; border: none; border-radius: 6px; padding: 12px; font-size: 1.1em; font-weight: 600; margin-top: 18px; cursor: pointer; transition: background 0.2s; }
        button[type="submit"]:hover { background: #2c3e50; }
        #result { margin-top: 24px; min-height: 32px; text-align: center; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📷 Upload Discharge Summary</h1>
        <form id="uploadForm" enctype="multipart/form-data">
            <div class="upload-area" onclick="document.getElementById('fileInput').click();">
                <span style="font-size:2em;">⬆️</span><br>
                <span>Click to select an image</span>
                <input id="fileInput" type="file" name="image" accept="image/*" style="display:none;" required>
            </div>
            <div id="preview" class="preview"></div>
            <button type="submit">Extract Data</button>
        </form>
        <div id="result"></div>
    </div>
    <script>
        document.getElementById('fileInput').addEventListener('change', function(e) {
            const file = e.target.files[0];
            const previewDiv = document.getElementById('preview');
            if (file && file.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onload = function(ev) {
                    previewDiv.innerHTML = <img src="${ev.target.result}" alt="Preview">;
                };
                reader.readAsDataURL(file);
            } else {
                previewDiv.innerHTML = '';
            }
        });

        document.getElementById('uploadForm').onsubmit = async function(e) {
            e.preventDefault();
            const formData = new FormData(document.getElementById('uploadForm'));
            const resultDiv = document.getElementById('result');
            resultDiv.innerHTML = '🔄 Processing... please wait.';
            try {
                const response = await fetch('/extract', { method: 'POST', body: formData });
                if (response.redirected) {
                    window.location.href = response.url;
                    return;
                }
                const data = await response.json();
                resultDiv.innerHTML = data.success ? '✅ Extracted!' : '❌ Error occurred.';
            } catch (err) {
                resultDiv.innerHTML = <div class='error'>❌ ${err}</div>;
            }
        };
    </script>
</body>
</html>
'''

@app.route("/")
def index():
    return render_template_string(HTML_FORM)

@app.route("/extract", methods=["POST"])
def extract():
    if 'image' not in request.files:
        return jsonify({"success": False, "error": "No image uploaded"}), 400
    try:
        img = Image.open(request.files['image'])
        img.load()

        prompt = '''Extract medical details from this discharge summary and return STRICTLY as JSON:
        {
          "name": "Patient Name",
          "age": "Age",
          "phone": "Phone",
          "address": "Address",
          "blood_group": "Blood Type",
          "admission_date": "Admission Date",
          "discharge_date": "Discharge Date",
          "stay_duration": "Hospital Stay Duration",
          "diagnosis": ["Diagnosis 1", "Diagnosis 2"],
          "medications": [
            {
              "name": "Medicine Name",
              "dosage": "Dosage",
              "frequency": "Frequency",
              "purpose": "Purpose"
            }
          ],
          "clinical_summary": "Clinical summary text"
        }'''

        response = model.generate_content([prompt, img])
        response_text = response.text.strip()

        if response_text.startswith("json"):
            response_text = response_text[7:-3].strip()
        elif response_text.startswith(""):
            response_text = response_text[3:-3].strip()

        data = json.loads(response_text)
        session['extracted_data'] = data
        return redirect(url_for('form'))

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/form", methods=["GET"])
def form():
    data = session.get('extracted_data', {})
    form_html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Patient Intake Form</title>
        <style>
            body { font-family: 'Segoe UI', sans-serif; background: #f5f5f5; display: flex; justify-content: center; padding: 40px; }
            .form-container { background: white; padding: 30px 40px; width: 500px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
            h2 { margin-bottom: 20px; font-size: 24px; color: #333; }
            label { display: block; margin: 15px 0 5px; color: #444; }
            input, textarea { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 6px; font-size: 15px; }
            button { margin-top: 20px; padding: 12px 20px; background-color: #1a73e8; color: white; border: none; font-size: 16px; border-radius: 6px; cursor: pointer; }
            button:hover { background-color: #155bc3; }
        </style>
    </head>
    <body>
        <div class="form-container">
            <h2>Patient Intake Form</h2>
            <form method="POST" action="/submit">
                <label>Name</label>
                <input type="text" name="name" value="{{ name }}" required>

                <label>Age</label>
                <input type="text" name="age" value="{{ age }}">

                <label>Phone</label>
                <input type="text" name="phone" value="{{ phone }}">

                <label>Address</label>
                <input type="text" name="address" value="{{ address }}">

                <label>Blood Group</label>
                <input type="text" name="blood_group" value="{{ blood_group }}">

                <label>Diagnosis</label>
                <textarea name="diagnosis">{{ diagnosis }}</textarea>

                <label>Medications</label>
                <textarea name="medications">{{ medications }}</textarea>

                <label>Clinical Summary</label>
                <textarea name="clinical_summary">{{ clinical_summary }}</textarea>

                <button type="submit">Submit</button>
            </form>
        </div>
    </body>
    </html>
    '''
    return render_template_string(form_html,
        name=data.get('name', ''),
        age=data.get('age', ''),
        phone=data.get('phone', ''),
        address=data.get('address', ''),
        blood_group=data.get('blood_group', ''),
        diagnosis="\n".join(data.get('diagnosis', [])),
        medications="\n".join([
            f"{m.get('name', '')} - {m.get('dosage', '')} - {m.get('frequency', '')} - {m.get('purpose', '')}"
            for m in data.get('medications', [])
        ]),
        clinical_summary=data.get('clinical_summary', '')
    )

@app.route("/submit", methods=["POST"])
def submit():
    form_data = dict(request.form)
    with open("patient_data.json", "a") as f:
        f.write(json.dumps(form_data) + "\n")
    return "<h3>✅ Form submitted successfully!</h3><a href='/'>Upload another</a>"

if _name_ == "_main_":
    app.run(debug=True)