import requests
import json

host1 = 'http://localhost:5000/'
print("home:")
print(requests.get(host1).text)

import pickle
with open('../../test_data.pickle', 'rb') as f:
    test_data = pickle.load(f)

test_x = test_data['valid']['X'][:3]
data = json.dumps({"data": test_x.tolist()})

host2 = 'http://localhost:5000/predict'
response = requests.post(host2, data=data)
print(response.text)
#print(response.text)
