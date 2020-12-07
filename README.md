# AISC-GNN-Tox
### Ryan Cohn, Julio Soldevilla

GNN-Tox is our capstone project for the 2020 Aggregate Intellect Graph Neural Network workshop. This project utilizes GNN technologies to predict the interaction of a given molecule with the various biological pathways of interest in the Tox21 Challenge. More information on the challenge can be found on the [Tox21 website.](https://tripod.nih.gov/tox21/challenge/index.jsp)

The input to the model is the [SMILES](https://en.wikipedia.org/wiki/Simplified_molecular-input_line-entry_system) representation of molecular structures. GNN-Tox uses the open-source tools in [DeepChem](https://deepchem.io/) for feature extraction of each model.

# Running the app

The model lives in a Flask app, which is accessed through Port 5000. Once the app is running, it will be accessible by navigating to http://localhost:5000/ There are multiple ways to run the application.

## Docker
The easiest way to access the app is through our Docker container, published on DockerHub as [rccohn/aisc_2020_gnn-b_dc_container:latest](https://hub.docker.com/layers/126013843/rccohn/aisc_2020_gnn-b_dc_container/latest/images/sha256-af5402eb1d400125fcbfc54cebbdc145941cf61f58dbea145e918fa592007453?context=explore)

1. Pull the docker image: 
```bash
sudo docker pull rccohn/aisc_2020_gnn-b_dc_container:latest
```
2. Run the container: 
```bash
sudo docker run -it --name aisc-2020-gnn  -p 5000:5000 --rm rccohn/aisc_2020_gnn-b_dc_container:final
```
Note that in order to access the Flask app inside the container, port 5000 must be exposed and mapped to another port on the host machine by using  `-p <port_number>:5000`.

## Conda Environment
To run the app directly through python, first configure the environment using `conda.`
1. Install base environment located in 'final_release/docker/dc_env_docker.yml': 
```bash
conda env create --file <path/to/AISC-GNN-Tox>/dc_env_docker.yml
```
2. Activate environment
```bash
conda activate dc_env_docker
```
3. Install deepchem from source (latest version required for this project isn't yet available on PyPI)
```
pip install git+https://github.com/deepchem/deepchem
```

4. Run the app located in `/final_release/docker/api`:
```bash
python app.py
```


# Running model inference
http://localhost:5000/ will only display some app metadata. There are 2 different ways to access the model.

## Upload a csv of molecules and save the results in a separate file
This is the easiest way to interact with the app.

1. Create a csv or txt file where each line contains one SMILES encoded molecule (no commas or spaces.)
For example, the contents of a file called `test_input.csv` may be:
```
CC(C)(c1ccc(Oc2ccc3c(c2)C(=O)OC3=O)cc1)c1ccc(Oc2ccc3c(c2)C(=O)OC3=O)cc1
Cc1cc(C(C)(C)C)c(O)c(C)c1Cn1c(=O)n(Cc2c(C)cc(C(C)(C)C)c(O)c2C)c(=O)n(Cc2c(C)cc(C(C)(C)C)c(O)c2C)c1=O
Cc1nnc(-c2ccccc2)c(=O)n1N
```

2. In your browser, navigate to http://localhost:5000/upload
Here, you will be able to select and upload your file. Immediately after uploading, the file will be processed and you will be prompted to download the results, which will be available as a CSV. The first two columns of the CSV are the index (integer) and SMILES encoding of the molecule. The next 12 columns correspond to the 12 pathways of interest (labeled in the header.) An entry of 1 indicates that the molecule is predicted to be active in the pathway, and an entry of 0 indicates it is predicted to not be active.

## Access the model via POST request.
If you would like to automate the process, you can also access the app through http requests. POST requests can be sent to `localhost:5000/predict`. The request must be formatted as a JSON entry with the following format: {"data": ["<SMILES-molecule-1>","<SMILES-molecule-2>",etc]} A simple way to do this in Python is shown below.

```python3
import json
import requests

host1 = 'localhost:5000'    # app root
host2 = f'{host1}/predict'  # address for post request

# SMILES encodings
molecules = ['CC(C)(c1ccc(Oc2ccc3c(c2)C(=O)OC3=O)cc1)c1ccc(Oc2ccc3c(c2)C(=O)OC3=O)cc1',
       'Cc1cc(C(C)(C)C)c(O)c(C)c1Cn1c(=O)n(Cc2c(C)cc(C(C)(C)C)c(O)c2C)c(=O)n(Cc2c(C)cc(C(C)(C)C)c(O)c2C)c1=O',
       'Cc1nnc(-c2ccccc2)c(=O)n1N', 'N=C(N)NCC1COc2ccccc2O1',
       'Cc1cccc(C)c1NC(=O)NC1=CCCN1C', 'c1csc(C2(N3CCCCC3)CCCCC2)c1',]

# format as JSON
data_json = json.dumps({'data':molecules})

# post request
response = requests.post(host2, data=data_json)

# receive request and convert back to Python object
response_list = json.loads(response.text)

# print predictions
for i in range(3):
    print('{}: {}'.format(i, molecules))
    print(response_list[i])
    print('\n\n')
```
