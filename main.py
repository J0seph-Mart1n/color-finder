from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import cv2 as cv
import numpy as np
import PIL
import os

app = Flask(__name__)
app.config['UPLOAD_PATH'] = 'static/assets'
level = 1

@app.route('/')
def index():
    global level
    file = os.listdir(app.config['UPLOAD_PATH'])
    length = len(file)
    top_colors_list = []
    for image in file:
        image_url = url_for('upload', filename=image)
        image_url = image_url.replace('%20',' ')
        image_url = image_url[1:]
        img = cv.imread(image_url)
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)

        dim = (500, 500)
        img = cv.resize(img, dim, interpolation = cv.INTER_AREA)
        img_temp = img.copy()
        unique, count = np.unique(img_temp.reshape(-1, 3), axis=0, return_counts=True)
        top_colors = unique[np.argsort(count)[::-1][0:(level*100):(level*10)]]
        top_colors_list.append(top_colors)
    return render_template('index.html', files=file, length=length, colors = top_colors_list)

@app.route('/', methods=['POST'])
def upload_file():
    f = request.files['file']
    new_level = request.form.get('Level')
    global level
    level = int(new_level)
    filename = f.filename
    if filename != '':
        f.save(os.path.join(app.config["UPLOAD_PATH"],filename))
    return redirect(url_for('index'))

@app.route('/static/assets/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)

@app.route('/delete/<image_no>', methods=['GET','POST'])
def delete(image_no):
    file = os.listdir(app.config['UPLOAD_PATH'])
    file_path = 'static/assets/'
    os.remove(os.path.join(file_path, file[int(image_no)]))
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run()