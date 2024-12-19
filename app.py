from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
import os
import subprocess

app = Flask(__name__)

# Yüklenen görsellerin kaydedileceği klasör
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
OUTPUT_FOLDER = os.path.join(os.getcwd(), 'output')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Yalnızca belirli uzantılara izin ver
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Dosya uzantısını kontrol et
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        # Yüklenen dosyanın kaydedilmesi
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # 3D model oluşturmak için TripoSR'yi çalıştır
        output_dir = 'static/0'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        tripo_sr_path = r'C:\\Users\\Serkan Öztürk\\Desktop\\MezuniyetProjesi\\TripoSR\\run.py'
        subprocess.run(['python', tripo_sr_path, file_path, '--output-dir', output_dir])

        # Model dosyasının adını belirleyin (örneğin: mesh.obj)
        model_filename = 'mesh.obj'  # Oluşturulan modelin adı

        return render_template('index.html', filename=model_filename, uploaded_image=url_for('static', filename=f'uploads/{file.filename}'))


@app.route('/download/<filename>')
def download_file(filename):
    # Dosyanın bulunduğu dizin
    directory = 'static/0/0'  # Dosyanın bulunduğu alt dizin
    return send_from_directory(directory, filename, as_attachment=True)



if __name__ == '__main__':
    app.run(debug=True)
