import os
import shutil
import threading
import time
import zipfile
import uuid
from flask import Flask, redirect, render_template
from PIL import Image
from komgaAPI import KomgaApi

app = Flask(__name__)
komga = KomgaApi('https://reading.solidbooru.online', 'Dionyssioss@gmail.com', '')

def delete_files_after_delay(directory, delay):
    time.sleep(delay)
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            delete_files_after_delay(file_path, 0)
    os.rmdir(directory)

def unpack_cbz(content, session_id):
	temp_dir = 'temp/' + session_id
	os.makedirs(temp_dir, exist_ok=True)
	temp_file = os.path.join(temp_dir, f'{uuid.uuid4()}.cbz')

	with open(temp_file, 'wb') as file:
		file.write(content)

	with zipfile.ZipFile(temp_file, 'r') as zip_ref:
		zip_ref.extractall(temp_dir)

	os.remove(temp_file)
def convert_images(directory, session_id):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            if filename.endswith('.jpg') or filename.endswith('.png'):
                img = Image.open(file_path)
                # create in static folder with session_id as subfolder
                os.makedirs(f'static/{session_id}', exist_ok=True)
                img.save(f'static/{session_id}/{filename}', 'JPEG')
        elif os.path.isdir(file_path):
            convert_images(file_path, session_id)

@app.route('/generate/<series_id>')
def generate_series(series_id):
    session_id = str(uuid.uuid4())
    # Create a unique directory for this user
    user_dir = f'temp/{session_id}'
    os.makedirs(user_dir, exist_ok=True)

    # Download the file
    content = komga.get_file(series_id)

    # Unpack and convert the images
    unpack_cbz(content, session_id)
    convert_images(user_dir, session_id)
    
    static_path = f'static/{session_id}'
    
	# Clear the temp folder after moving to static
    shutil.rmtree(user_dir)
    
	# Start a new thread that will delete the files after 1 minute
    threading.Thread(target=delete_files_after_delay, args=(static_path, 3600)).start()

    # redirect to the view page on point /view/<session_id>
    return redirect(f'/view/{session_id}')

@app.route('/view/<session_id>')
def view_series(session_id):
    static_path = f'static/{session_id}'
    if not os.path.exists(static_path):
        return render_template('error.html', message='Session Expired!')
    images = sorted(os.listdir(static_path))
    return render_template('view.html', images=images, user_dir=session_id)

if __name__ == '__main__':
    app.run(port=5000)