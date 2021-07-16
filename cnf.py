import sys, json, datetime

if __name__ == '__main__':

    file_name = sys.argv[1]

    f = open(file_name, 'r')
    data = json.loads(f.read())

    N = len(data["participants"])

    def var(d, h, i, j):
        assert(0<= i and i <= N and 0<= j and j <=N)
        return d*(N**3)+h*(N**2)+(i*N)+j+1

    clauses = []
    
    
    init_date = datetime.date.fromisoformat(data["start_date"])
    end_date = datetime.date.fromisoformat(data["end_date"])
    dur_date = (end_date - init_date).days

    init_hour = datetime.time.fromisoformat(data["start_time"])
    end_hour = datetime.time.fromisoformat(data["end_time"])
    dur_hour = abs(end_hour.hour - init_hour.hour)

    temp = []

    # Los participantes deben jugar al menos una vez con cada uno de los otros participantes
    for i in range(0, N): #Participante que juega como local
        for j in range(0, N): #Participante que juega como visitante
            if i != j:
                for d in range(0, dur_date):
                    temp += [var(d,h,i,j) for h in range(0, dur_hour)]

                clauses.append(temp)
                temp = []

    # Los participantes máximo deben jugar una vez como local y una como visitante con otro participante
    for d in range(0, dur_date):
    for i in range(0, N):
        for j in range(0,N):
            if i != j:
                for h in range(0, dur_hour):
                    for w in range(0, dur_date):
                        for k in range(0, dur_hour):
                            if w != d or k != h:
                                clauses.append([-var(d,h,i,j), -var(w,k,i,j)])

    # Un participante puede jugar a lo sumo una vez por dia
    for d in range(0, dur_date):
        for i in range(0, N):
            for j in range(0,N):
                if i != j:
                    for h in range(0, dur_hour):
                        for w in range(0, N):
                            if w != i and w != j:
                                for k in range(0, dur_hour):
                                    clauses.append([-var(d,h,i,j), -var(d,k,i,w)])

    # Dos juegos no pueden ocurrir al mismo tiempo
    for d in range(0, dur_date):
        for h in range(0, dur_hour):
            for i in range(0,N):
                for j in range(0, N):
                    if i != j:
                        for w in range(0, N):
                            for k in range(0, N):
                                if (w != i or k != j) and w != k:
                                    clauses.append([-var(d,h,i,j), -var(d,h,w,k)])

    # Un jugador no puede jugar ni de local ni de visitante dos dias consecutivos
    for d in range(0, dur_date - 1):
        for i in range(0, N):
            for j in range(0,N):
                if i != j:
                    for h in range(0, dur_hour):
                        for w in range(0, N):
                            if w != i and w != j:
                                for k in range(0, dur_hour):
                                    clauses.append([-var(d,h,i,j), -var(d+1,k,i,w)])


