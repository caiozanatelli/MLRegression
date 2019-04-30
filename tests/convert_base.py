'''
########################################################
##         FEDERAL UNIVERSITY OF MINAS GERAIS         ##
##             COMPUTER SCIENCE DEPARTMENT            ##
##             WIRELESS NETWORKS LABORATORY           ##
##                                                    ##
##            Author: Caio Felipe Zanatelli           ##
##                                                    ##
########################################################
'''
import numpy as np
import argparse
import csv

RESOLUTIONS = ['240', '360', '480', '720']
LOAD = ['cc']
FPS  = [10, 30]

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
    # Get useful arguments
    parser = argparse.ArgumentParser(description='Database joiner')
    parser.add_argument('--base-path', '-b', type=str, action='store',
                        default='./real/ufmg/', help='Database path')
    parser.add_argument('--output', '-o', type=str, action='store',
                        default='./resbase.csv', help='Final database')
    parser.add_argument('--pool', '-p', type=str, action='store', default='ufmg', 
                        help='COPA Pool selection')
    parser.add_argument('--res', '-r', type=list, action='store', default=RESOLUTIONS,
                        help='Video resolution')
    parser.add_argument('--fps', '-f', type=list, action='store', default=FPS,
                        help='FPS selection')
    parser.add_argument('--load', '-l', type=list, action='store', default=LOAD,
                        help='Load selection')
    args = parser.parse_args()

    if args.base_path[-1] != '/': args.base_path += '/'

    bases = []
    trans_offset = []
    obs_offset = []
    for res in args.res:
        for fps in args.fps:
            for load in args.load:
                #name = '{}{}_{}_{}fps_{}_'.format(args.base_path, args.pool, res, fps, load)
                #name = '{}{}_{}_{}fps_{}_'.format(args.base_path, args.pool, fps, load, res)
                #######name = '{}_{}_{}_{}'.format(args.pool, fps, load, res)
                #bases.append(load_csv(name + 'database.csv'))
                #######print(args.base_path + str(fps) + '_' + str(load) + '_' + str(res) + '_database.csv')

                #######bases.append(load_csv(args.base_path + str(fps) + '_' + str(load) + '_' + str(res) + '_database.csv'))
                #######trans_offset.append(load_csv(args.base_path + 'transmission_capture_' + name + '.csv'))
                #######obs_offset.append(load_csv(args.base_path  + 'transmission_observer_' + name + '.csv'))
                
                name = '{}{}_{}_'.format(args.base_path, res, load)
                print(name + 'database.csv')
                bases.append(load_csv(name + 'database.csv'))
                trans_offset.append(load_csv(name + 'transmission_capture.csv'))
                obs_offset.append(load_csv(name + 'transmission_observer.csv'))

        #bases.append(load_csv('{}{}_{}_database.csv'.format(args.base_path, args.prefix, res)))
        #trans_offset.append(load_csv('{}{}_{}_transmission_capture.csv'.format(
        #                    args.base_path, args.prefix, res)))
        #obs_offset.append(load_csv('{}{}_{}_transmission_observer.csv'.format(
        #                    args.base_path, args.prefix, res)))

        #bases.append(load_csv(args.base_path + args.prefix + res + '.csv'))
        #trans_offset.append(load_csv(args.base_path + 'transmission_capture_' + res + '.csv'))
        #obs_offset.append(load_csv(args.base_path + 'transmission_observer_' + res + '.csv'))

    for i in range(len(bases)):
        for j in range(1, len(bases[i])):
            print(i, j)
            #print(bases[i][j])

            #print(bases[i][j][-1])
            bases[i][j][-1] += trans_offset[i][j][-1]
            bases[i][j][-1] += obs_offset[i][j][-1]

    with open(args.output, 'w') as final_csv:
        final_csv.write('cpu_percentage,cpu_time,cpu_count,m_percentage,m_available,\
                m_size,m_swap,net_traffic,frame_rate,resolution,PROCESSING_TIME\n')
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
    
