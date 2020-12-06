# AISC-GNN-Tox
### Ryan Cohn, Julio Soldevilla

GNN-Tox is our capstone project for the 2020 Aggregate Intellect Graph Neural Network workshop. This project utilizes GNN technologies to predict the interaction of a given molecule with the various biological pathways of interest in the Tox21 Challenge. More information on the challenge can be found on the [Tox21 website.](https://tripod.nih.gov/tox21/challenge/index.jsp)

The input to the model is the [SMILES](https://en.wikipedia.org/wiki/Simplified_molecular-input_line-entry_system) representation of molecular structures. GNN-Tox uses the open-source tools in [DeepChem](https://deepchem.io/) for feature extraction of each model.

# Running the app

The model lives in a Flask app, which is accessed through Port 5000. Once the app is running, it will be accessible by navigating to (http://localhost:5000/)[http://localhost:5000/] There are multiple ways to run the application.

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
http://localhost:5000/ will only display some app metadata. To run model inference and generate predictions, 
