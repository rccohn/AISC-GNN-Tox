from pathlib import Path
with open(Path(__file__).parent /'tox21_categories.txt', 'r') as f:
    data = [x.replace('\n', '') for x in f.readlines()[1:]]

labels = {0: 'inactive', 1: 'active'}


def inverse_transform(y, data=data, labels=labels):
    """
    Convert vector of predictions y into human readable labels

    Parameters
    ----------
    y: ndarray
        n-predict x 12 array of 0 (inactive) and 1 (active) labels
    data: list
        string labels of pathways in order of y_pred
    labels: dict
        maps numeric outputs to string (ie active vs inactive)

    Returns
    -------
    y_transform: list
        y translated to human readable form
    """
    y_transform = []
    for yi in y:  # for each prediction (12 labels)
        label_i = []
        for label, pathway in zip(yi, data): # for each element of the prediction
            label_i.append('{}: {}'.format(pathway, labels[label]))
        y_transform.append(label_i)
    return y_transform
