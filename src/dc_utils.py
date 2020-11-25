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
    df['X'] = [dc.feat.mol_graphs.ConvMol(**x) for x in df['X']]
    dataset = dc.data.DiskDataset.from_dataframe(df)
    if tasks is not None:
        dataset.tasks = tasks
    return dataset

def dataset_to_dict(ds):
    return {'df': dataset_to_df(ds),
            'tasks': ds.tasks}