import numpy as np
import csv

RESOLUTIONS = ['240', '360', '480', '720', '1080']
PATH_PREFIX = './base/'
RES_BASE    = './resbase.csv'

def load_csv(path, skiprow=None):
    data = []
    with open(path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        count = 0
        for row in csv_reader:
            if skiprow and count == skiprow:
                pass
            elif count == 0:
                #data.append(list(str(x) for x in row))
                pass
            else:
                data.append(list(float(x) for x in row))
            count += 1
    return data

if __name__ == '__main__':
    bases = []
    trans_offset = []
    obs_offset = []
    for res in RESOLUTIONS:
        bases.append(load_csv(PATH_PREFIX + 'database_' + res + '.csv'))
        trans_offset.append(load_csv(PATH_PREFIX + 'transmission_capture_' + res + '.csv'))
        obs_offset.append(load_csv(PATH_PREFIX + 'transmission_observer_' + res + '.csv'))

    #for i in range(len(bases)):
    #    for j in range(1, len(bases[i])):
    #        if len(bases[i][j]) == 11:
    #            print("AAAAAAAAAAA 11: " + RESOLUTIONS[i])
    #        if len(bases[i][j]) == 13:
    #            print("AAAAAAAAAAA 13: " + RESOLUTIONS[i])
            #print(len(trans_offset[i][j]))
            #print(len(obs_offset[i][j]))



    for i in range(len(bases)):
        for j in range(1, len(bases[i])):
            #print(bases[i][j][-1])
            bases[i][j][-1] += trans_offset[i][j][-1]
            bases[i][j][-1] += obs_offset[i][j][-1]

    with open(RES_BASE, 'w') as final_csv:
        for row in bases:
            for elem in row:
                count = 1
                #print(len(elem))
                for x in elem:
                    final_csv.write(str(x))
                    if count < len(elem):
                        final_csv.write(',')
                    count += 1
                final_csv.write('\n')
