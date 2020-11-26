import deepchem as dc

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
    return {'df': dataset_to_df(ds),
            'tasks': ds.tasks}

def dataset_from_dict(d):
    return df_to_dataset(d['df'], d['tasks'])