import sys, json, datetime

if __name__ == '__main__':

    file_name = sys.argv[1]

    f = open(file_name, 'r')
    data = json.loads(f.read())

    N = len(data["participants"])

    def var(d, h, i, j):
        assert(0<= i and i <= N and 0<= j and j <=N)
        value = f"{d}00{h}00{i}00{j}"
        return int(value)

    clauses = []
    
    
    init_date = datetime.date.fromisoformat(data["start_date"])
    end_date = datetime.date.fromisoformat(data["end_date"])
    dur_date = (end_date - init_date).days

    init_hour = datetime.time.fromisoformat(data["start_time"])
    end_hour = datetime.time.fromisoformat(data["end_time"])
    dur_hour = abs(end_hour.hour - init_hour.hour)

    temp = []

    # Los participantes deben jugar al menos una vez con cada uno de los otros participantes
    for i in range(1, N + 1): #Participante que juega como local
        for j in range(1, N + 1): #Participante que juega como visitante
            if i != j:
                for d in range(1, dur_date + 1):
                    temp += [var(d,h,i,j) for h in range(1, dur_hour + 1)]

                clauses.append(temp)
                temp = []

    # Los participantes máximo deben jugar una vez como local y una como visitante con otro participante
    for d in range(1, dur_date + 1):
        for i in range(1, N + 1):
            for j in range(1, N + 1):
                if i != j:
                    for h in range(1, dur_hour + 1):
                        for w in range(1, dur_date + 1):
                            for k in range(1, dur_hour + 1):
                                if w != d or k != h:
                                    clauses.append([-var(d,h,i,j), -var(w,k,i,j)])

    # Un participante puede jugar a lo sumo una vez por dia
    for d in range(1, dur_date + 1):
        for i in range(1, N + 1):
            for j in range(1, N + 1):
                if i != j:
                    for h in range(1, dur_hour + 1):
                        for w in range(1, N + 1):
                            if w != i and w != j:
                                for k in range(1, dur_hour + 1):
                                    clauses.append([-var(d,h,i,j), -var(d,k,i,w)])

    # Dos juegos no pueden ocurrir al mismo tiempo
    for d in range(1, dur_date + 1):
        for h in range(1, dur_hour + 1):
            for i in range(1, N + 1):
                for j in range(1, N + 1):
                    if i != j:
                        for w in range(1, N + 1):
                            for k in range(1, N + 1):
                                if (w != i or k != j) and w != k:
                                    clauses.append([-var(d,h,i,j), -var(d,h,w,k)])

    # Un jugador no puede jugar ni de local ni de visitante dos dias consecutivos
    for d in range(1, dur_date):
        for i in range(1, N + 1):
            for j in range(1, N + 1):
                if i != j:
                    for h in range(1, dur_hour + 1):
                        for w in range(1, N + 1):
                            if w != i and w != j:
                                for k in range(1, dur_hour + 1):
                                    clauses.append([-var(d,h,i,j), -var(d+1,k,i,w)])



