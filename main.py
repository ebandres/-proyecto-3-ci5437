import sys, json, datetime, os, subprocess, threading
import cnf
import saveload
from ics import Calendar, Event

def get_var(kd, value):
    v = kd[value].split()
    return int(v[0]), int(v[1]), int(v[2]), int(v[3])

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print("Missing Argument")
        exit(1)

    thread = threading.Thread(target=cnf.convert(sys.argv[1]))
    thread.start()
    thread.join()

    # Glucose stuff
    proc = subprocess.Popen(["./glucose/simp/glucose_static", "cnf.txt", "r.txt"])
    proc.wait()

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

    with open(sys.argv[1], 'r') as file:
        t_json = json.loads(file.read())

    tournament_name = t_json["tournament_name"]
    start_date = datetime.date.fromisoformat(t_json["start_date"])
    end_date = datetime.date.fromisoformat(t_json["end_date"])
    start_time = datetime.time.fromisoformat(t_json["start_time"])
    end_time = datetime.time.fromisoformat(t_json["end_time"])
    participants = t_json["participants"]

    cal = Calendar()
    for m in matches:
        begin = datetime.datetime.combine(start_date + datetime.timedelta(days = m[0] - 1), start_time)
        begin += datetime.timedelta(hours = 2 * (m[1] - 1))
        end = begin + datetime.timedelta(hours = 2)

        e = Event()
        e.name = f"{participants[m[2] - 1]} vs. {participants[m[3] - 1]}"
        e.begin = str(begin)
        e.end = str(end)

        cal.events.add(e)

    print("Writing calendar file...")
    with open(f"{tournament_name}.ics", 'w') as ic:
        ic.write(str(cal))
    print("Done")