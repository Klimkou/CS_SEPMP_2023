import sys


def read_log(filename) -> float: #graphene_all_3351000..log
    with open(f'./Sem1_dimers_data/{filename}', 'r') as file:
        finded = False
        lines = file.readlines()
        #print(lines)
        for line in lines:
            words = line.split()
            if len(words) > 1:
                if words[0] == 'Atoms' and words[1] == 'Step':
                    finded = True
                    continue
            else:
                continue
            if finded:
                return float(words[3])

log_name = sys.argv[1]
output_name = sys.argv[2]

data = read_log(log_name)

with open(f'./{output_name}', 'a') as file:
    file.write(str(data))
    file.write('\n')

