from flask import Flask, request, jsonify
import mlflow.pyfunc
import pandas as pd
import json
import src 

# Name of the apps module package
app = Flask(__name__)

# Load in the model at app startup
model = mlflow.pyfunc.load_model('../mlflow_root/model')

# Load in our meta_data
with open("../mlflow_root/model/artifacts/metadata.txt", "r") as f:
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
    
    # convert dict values from lists to ndarrays
    req = src.dc_utils.json_dict_to_dict(req['data']['df'])

    # Format the request data in a DataFrame
    inf_df = src.dc_utils.dict_to_dataframe(req)

    # Get model prediction - convert from np to list
    pred = model.predict(inf_df)

    # Log the prediction
    print({'response': pred})

    # Return prediction as reponse
    return jsonify(pred)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
