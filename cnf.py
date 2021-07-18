import sys, json, datetime
import pickle

# Global variables to store all values for later retrieval during decoding
value_dict = {}
last_value = 1
        
def save_obj(obj, name):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

if __name__ == '__main__':

    file_name = sys.argv[1]

    f = open(file_name, 'r')
    data = json.loads(f.read())

    N = len(data["participants"])

    def var(d, h, i, j):
        assert(0<= i and i <= N and 0<= j and j <=N)
        #value = f"{d}00{h}00{i}00{j}"
        #return value
        global last_value

        if f"{d}{h}{i}{j}" not in value_dict:
            value_dict[f"{d}{h}{i}{j}"] = last_value
            last_value += 1
            return last_value - 1

        return value_dict[f"{d}{h}{i}{j}"]

    clauses = []
    
    
    init_date = datetime.date.fromisoformat(data["start_date"])
    end_date = datetime.date.fromisoformat(data["end_date"])
    dur_date = (end_date - init_date).days

    init_hour = datetime.time.fromisoformat(data["start_time"])
    end_hour = datetime.time.fromisoformat(data["end_time"])
    dur_hour = abs(end_hour.hour - init_hour.hour)

    temp = []
    count = 0

    # Número total de variables
    for i in range(1, N + 1):
        for j in range(1, N + 1):
            if i != j:
                for d in range(1, dur_date + 1):
                    for h in range(1, (dur_hour // 2) + 1):
                        count += 1
    
    # Los participantes deben jugar al menos una vez con cada uno de los otros participantes
    for i in range(1, N + 1): #Participante que juega como local
        for j in range(1, N + 1): #Participante que juega como visitante
            if i != j:
                for d in range(1, dur_date + 1):
                    temp += [f"{var(d,h,i,j)}" for h in range(1, (dur_hour // 2) + 1)]

                clauses.append(temp)
                temp = []
    
    # Los participantes máximo deben jugar una vez como local y una como visitante con otro participante
    for d in range(1, dur_date + 1):
        for i in range(1, N + 1):
            for j in range(1, N + 1):
                if i != j:
                    for h in range(1, (dur_hour // 2) + 1):
                        for w in range(1, dur_date + 1):
                            for k in range(1, (dur_hour // 2) + 1):
                                if w != d or k != h:
                                    clauses.append([f"-{var(d,h,i,j)}", f"-{var(w,k,i,j)}"])

    # Un participante puede jugar a lo sumo una vez por dia
    for d in range(1, dur_date + 1):
        for i in range(1, N + 1):
            for j in range(1, N + 1):
                if i != j:
                    for h in range(1, (dur_hour + 1) // 2):
                        for w in range(1, N + 1):
                            if w != i and w != j:
                                for k in range(1, (dur_hour + 1) // 2):
                                    clauses.append([f"{-var(d,h,i,j)}", f"{-var(d,k,i,w)}"])

    # Dos juegos no pueden ocurrir al mismo tiempo
    for d in range(1, dur_date + 1):
        for h in range(1, (dur_hour // 2) + 1):
            for i in range(1, N + 1):
                for j in range(1, N + 1):
                    if i != j:
                        for w in range(1, N + 1):
                            for k in range(1, N + 1):
                                if (w != i or k != j) and w != k:
                                    clauses.append([f"{-var(d,h,i,j)}", f"{-var(d,h,w,k)}"])

    # Un jugador no puede jugar ni de local ni de visitante dos dias consecutivos
    for d in range(1, dur_date):
        for i in range(1, N + 1):
            for j in range(1, N + 1):
                if i != j:
                    for h in range(1, (dur_hour // 2) + 1):
                        for w in range(1, N + 1):
                            if w != i and w != j:
                                for k in range(1, (dur_hour // 2) + 1):
                                    clauses.append([f"{-var(d,h,i,j)}", f"{-var(d+1,k,i,w)}"])
                                    clauses.append([f"{-var(d,h,i,j)}", f"{-var(d+1,k,w,j)}"])


    print("Saving value dictionary in obj/keys.pkl")
    save_obj(value_dict, "keys")

    print("Writing cnf.txt ...")
    cnf = open("cnf.txt", "w")
    separator = " "

    cnf.write(f"p cnf {count} {len(clauses)} \n")

    for cls in clauses:
        cls.append("0")
        cnf.write(separator.join(cls) + "\n")

    cnf.close()
    print("Done")



