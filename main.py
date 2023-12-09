from flask import Flask, render_template,request,flash
from werkzeug.utils import secure_filename
import os
import cv2
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'webp', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
# Set a secret key for the Flask app
app.config['SECRET_KEY'] = 'It_is_my_secreat_key_i_am_viresh_i_creating_app_to_edit_image_onlin'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def procesImage(filename,operation):
    print(f"teh opration is {operation} and the file anme{filename}")
    img=cv2.imread(f"uploads/{filename}")
    match operation:
        case "cgray":
            imgProcessed=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            newFilename = f"static/{filename}"
            cv2.imwrite(f"static/{filename}",imgProcessed)
            return newFilename
        case "cwebp":
               newFilename = f"static/{filename.split('.') [0]}.webp"
               cv2.imwrite(newFilename , img)
               return newFilename
 
        case "cjpg":
               newFilename=f"static/{filename.split('.')[0]}.jpg"
               cv2.imwrite(newFilename, img)
               return newFilename
 
        case "cpng":
                newFilename=f"static/{filename.split('.') [0]}.png"
                cv2.imwrite(newFilename, img)
                return newFilename

                 

   

@app.route("/")
def home():
    return  render_template("index.html")

@app.route("/about")
def about():
    return  render_template("about.html")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/edit",methods=["GET","POST"])
def edit():
    if request.method == 'POST':
        operation = request.form.get("operation")
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return "error"
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return " Error"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new =procesImage(filename,operation)
            flash(f"your image has been processed and is availabek <a href='/{new}' target='_blank'>Here</a>")
            return render_template("index.html",operation=operation)


    return   render_template("index.html")


if __name__=="__main__":
    
    app.run(debug=True,port=8000)