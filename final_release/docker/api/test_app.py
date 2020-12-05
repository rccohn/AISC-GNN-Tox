import requests
import json
import src

host1 = 'http://localhost:5000/'
print("home:")
print(requests.get(host1).text)

import pickle
#with open('../test_data_gnn.pickle', 'rb') as f:
#    test_data = pickle.load(f)

#test_x = {'data': test_data}
#data = json.dumps(test_x)

molecules = ['CC(C)(c1ccc(Oc2ccc3c(c2)C(=O)OC3=O)cc1)c1ccc(Oc2ccc3c(c2)C(=O)OC3=O)cc1',
       'Cc1cc(C(C)(C)C)c(O)c(C)c1Cn1c(=O)n(Cc2c(C)cc(C(C)(C)C)c(O)c2C)c(=O)n(Cc2c(C)cc(C(C)(C)C)c(O)c2C)c1=O',
       'Cc1nnc(-c2ccccc2)c(=O)n1N', 'N=C(N)NCC1COc2ccccc2O1',
       'Cc1cccc(C)c1NC(=O)NC1=CCCN1C', 'c1csc(C2(N3CCCCC3)CCCCC2)c1',]
data2 = json.dumps({'data': molecules})

host2 = 'http://localhost:5000/predict'
response = requests.post(host2, data=data2)
print(response.text)

