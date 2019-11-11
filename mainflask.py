import os
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
script_dir = os.path.dirname(__file__)
# @ signifies a decorator- way to wrap a fun and modify it
@app.route('/')
def index():
    return render_template("homepage.html")

#app.config['IMAGE_UPLOADS'] = "/c/Users/amitsparta/PycharmProjects/UserInterface/static/image/uploads"

upload_path = "/c/Users/amitsparta/PycharmProjects/UserInterface/static/image/uploads/"
@app.route('/upload', methods = ['GET','POST'])
def upload():
    if request.method == "POST":
        if request.files:
            image = request.files["image"]
            print(image.filename)
            image.save(image.filename)
            #image uploded messag
            return  redirect(request.url)
    return render_template("result.html")




if __name__ == "__main__":
    app.run(debug = True)

