from . import labels

def predict(X, model):
    """
    Pre-process input and generate model predictions

    Parameters
    ----------
    X: ndarray
        [n-inputs x 1024] array of inputs in SMILES format (1024 element vectors describing the structure of each molecule)

    model: deepchem.models.SklearnModel object
        model to process inputs. must be able to call y = model.predict(X)

    Returns
    -------
    y: list
        [n-input x 12] list of multi-class labels (as human readable strings).  # TODO make code for this cleaner

    """
    # TODO do we need any pre-processing steps for x?
    print('mlflow predict X')
    print(X)
    y = model.predict(X)
    y = labels.inverse_transform(y)
    return y

if __name__ == "__main__":
    # test for debugging
    import pickle

    # load model
    with open('../models/2020-11-15-RF-model.pickle', 'rb') as f:
        model = pickle.load(f)

    # load data
    with open('../test_data.pickle', 'rb') as f:
        data = pickle.load(f)

    Xval = data['valid']['X']
    yval = data['valid']['y']

    y_pred = predict(Xval, model)
    from sklearn.metrics import accuracy_score
    print(accuracy_score(yval, y_pred))
