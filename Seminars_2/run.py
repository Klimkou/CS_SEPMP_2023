import os
import sys
import matplotlib.pyplot as plt


#filename = 'graphene_all_3351000..log'

#os.chdir('./Sem1_dimers_data/')
filenames = os.listdir('./Sem1_dimers_data/')[1:] #'./'
output_name = sys.argv[1]
os.remove(f'{output_name}')

for filename in filenames:
    os.system(f'python read.py {filename} {output_name}')

with open(f'{output_name}', 'r') as file:
    data = file.readlines()[:-1]

res_data = []
for num in data:
    if num != 'None\n':
        res_data.append(float(num))

#data = list(map(float,data))

plt.hist(res_data, bins = [-9000,-8950,-8900,-8850,-8800,-4600,-4475,-4450,-4425,-4400])
plt.show()
#print(filenames)