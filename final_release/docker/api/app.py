from flask import Flask, request, jsonify, render_template, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import mlflow.pyfunc
import pandas as pd
import json
import src 
from pathlib import Path
import os

app = Flask(__name__, template_folder='.')


UPLOAD_FOLDER = str(Path(Path(__file__).parent / 'uploads/').resolve())
DOWNLOAD_FOLDER = str(Path(Path(__file__).parent / 'downloads/').resolve())
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

# max file size, MB
app.config['MAX_CONTENT_LENGTH'] = 24 * 1024 * 1024


ALLOWED_EXTENSIONS = {'csv', 'txt'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Name of the apps module package

mlflow_path = Path(__file__).parent / 'mlflow_root_final/model'

# Load in the model at app startup
model = mlflow.pyfunc.load_model(str(mlflow_path.resolve()))

# Load in our meta_data

with open(str((mlflow_path / "artifacts/metadata.txt").resolve()),
         "r") as f:
    load_meta_data = json.loads(f.read())

# Meta data endpoint
@app.route('/', methods=['GET'])
def meta_data():

    return jsonify(load_meta_data)


# Prediction endpoint
@app.route('/predict', methods=['POST'])
def predict():

    req = request.get_json(force=True)

    # Log the request
    print({'request': req})
    
    # request can either be a list of strings, or arrays for graph 
    # representation. 

    if type(req['data']) == list:
        print('processing input molecule list')
        inf_df = pd.DataFrame({'molecules': req['data']}) 
    else:
        print('processing featurized deepchem graph')
        # convert dict values from lists to ndarrays
        req = src.dc_utils.json_dict_to_dict(req['data'])

        # Format the request data in a DataFrame
        inf_df = src.dc_utils.dict_to_dataframe(req['df'])
    
   
    # Get model prediction - convert from np to list
    pred = model.predict(inf_df)

    # Log the prediction
    #print({'response': pred})

    # Return prediction as reponse
    return jsonify(pred)


@app.route('/upload/', methods=['GET','POST'])
def index():
   if request.method == 'POST':
       if 'file' not in request.files:
           print('No file attached in request')
           return redirect(request.url)
       file = request.files['file']
       if file.filename == '':
           print('No file selected')
           return redirect(request.url)
       if file and allowed_file(file.filename):
           print('yes!!!')
           filename = secure_filename(file.filename)
           file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
           process_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))
           return redirect(url_for('uploaded_file', filename=filename))
       else:
           print(file.filename)
           print(file.filename.rsplit('.', 1)[1].lower())
           print(allowed_file(file.filename))
   return render_template('index.html')


@app.route('/upload/<filename>')
def uploaded_file(filename):
   return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename, as_attachment=True)

def process_file(inpath):
    inpath = Path(inpath)
    with open(inpath, 'r') as f:
        lines = [x for x in f.read().split('\n') if len(x)]
    inf_df = pd.DataFrame({'molecules': lines})
    pred = json.dumps(model.predict(inf_df))
    outpath = Path(app.config['DOWNLOAD_FOLDER'], inpath.name)
    src.dc_utils.response_to_csv(pred, lines, outpath)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
