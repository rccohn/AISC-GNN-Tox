import requests
import json
import src

host1 = 'http://localhost:5000/'
print("home:")
print(requests.get(host1).text)

import pickle
with open('../test_data_gnn.pickle', 'rb') as f:
    test_data = pickle.load(f)

test_x = {'data': test_data}
data = json.dumps(test_x)


host2 = 'http://localhost:5000/predict'
response = requests.post(host2, data=data)
print(response.text)

