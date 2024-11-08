from flask import Flask, send_file, jsonify, render_template_string
import os
import socket
import datetime
import tarfile

app = Flask(__name__)

def get_hostname():
        return os.getenv('HOSTNAME', 'default-hostname')

def create_archive():
    hostname = get_hostname()
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    archive_name = f"{hostname}_{date_str}.tar.gz"
    
    files_to_backup = os.getenv('FILES_TO_BACKUP', '').split(',')
    inaccessible_files = []
    
    with tarfile.open(archive_name, 'w:gz') as archive:
        for file_path in files_to_backup:
            container_file_path = file_path.replace('/etc', '/host_machine/etc')
            if os.path.exists(container_file_path):
                archive.add(container_file_path, arcname=file_path)
            else:
                inaccessible_files.append(file_path)
    
    return archive_name, inaccessible_files, files_to_backup

@app.route('/')
def index():
    _, _, files_to_backup = create_archive()
    html_content = """
    <h1>Files to be Backed Up</h1>
    <ul>
    {% for file in files %}
        <li>{{ file }}</li>
    {% endfor %}
    </ul>
    <a href="/download">Download Archive</a>
    """
    return render_template_string(html_content, files=files_to_backup)

@app.route('/download')
def download():
    archive_name, inaccessible_files, _ = create_archive()
    if inaccessible_files:
        return jsonify({"error": "Some files are not accessible", "files": inaccessible_files}), 400
    return send_file(archive_name, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)

