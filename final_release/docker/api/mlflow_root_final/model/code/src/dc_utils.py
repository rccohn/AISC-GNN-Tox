import deepchem as dc
import pandas as pd
import numpy as np
import json


def convmol_to_dict(x):
    keys = ['atom_features', 'max_deg', 'min_deg']
    cmd = {k: x.__dict__[k] for k in keys}
    cmd['adj_list'] = x.get_adjacency_list()
    return cmd

def dataset_to_df(ds):
    df = ds.to_dataframe()
    df['X'] = [convmol_to_dict(x) for x in df['X']]
    return df


def df_to_dataset(df, tasks=None):
    cols = df.columns
    df['X'] = [dc.feat.mol_graphs.ConvMol(**x) for x in df['X']]
    ys = [x for x in cols if 'y' == x[0].lower()]
    ws = [x for x in cols if 'w' == x[0].lower()]

    dataset = dc.data.NumpyDataset(df['X'].to_numpy(),
                                   df[ys].to_numpy(),
                                   df[ws].to_numpy(),
                                   df['ids'])
    if tasks is not None:
        dataset.tasks = tasks
    return dataset

def dataset_to_dict(ds):
    return {'df': dataset_to_df(ds).to_dict(),
            'tasks': ds.tasks}

def json_dict(d):
    for k, v in d.items():
        if type(v) == np.ndarray:
            d[k] = v.tolist()
        elif type(v) == dict:
            d[k] = json_dict(v)
    return d


def dict_to_dataset(d):
    return df_to_dataset(pd.DataFrame(d['df']), d['tasks'])

def json_dict_to_dict(j):
    for k, v in j.items():
        if type(v) == list:
            j[k] = np.asarray(v)
        elif type(v) == dict:
            j[k] = json_dict_to_dict(v)
    return j

def dict_to_dataframe(d):
    return pd.DataFrame(d)


def data_to_json(ds):
    data_dict = dataset_to_dict(ds)
    jd = json_dict(data_dict)
    return jd

def format_request(data):
    return json.dumps({'data': data})


def response_to_csv(response, ids, outfile):
    """
    :param response: result from response from flask
    :param ids: list of string names of molecules (SMILES)
    :param outfile: path to file to write data
    :return:
    """
    try:
        response_list = json.loads(response.text)
    except:
        response_list = json.loads(response)
    tasks = [x.split(':')[0] for x in response_list[0]]

    decoder = {' inactive': 0, ' active': 1}
    responses = np.asarray([[decoder[x.split(':')[1]] for x in y]
                            for y in response_list])
    df = pd.DataFrame(dict(zip(tasks, responses.T)))

    cols = ['ids', *df.columns]
    df['ids'] = ids

    df = df[cols]
    df.set_index('ids')
    assert outfile.parent.exists()

    df.to_csv(outfile)

