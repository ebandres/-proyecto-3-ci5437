import sys, json
import cnf
import saveload

def get_var(kd, value):
    v = kd[value].split()
    return int(v[0]), int(v[1]), int(v[2]), int(v[3])

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print("Missing Argument")
        exit(1)

    #cnf.convert(sys.argv[1])

    # Glucose stuff

    value_dict = saveload.load_obj('keys')

    keys_dict = dict(zip(value_dict.values(), value_dict.keys()))

    with open('r.txt', 'r') as result:
        read_data = result.read()

    if read_data[0:5] == "UNSAT":
        print("Unsatisfiable")
        exit(2)
    
    match_ids = [int(i) for i in read_data.split() if int(i) > 0]
    matches = []
    for k in match_ids:
        d, h, i, j = get_var(keys_dict, k)
        matches += [[d, h, i, j]]

    print(matches)