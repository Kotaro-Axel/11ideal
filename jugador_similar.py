def jugador_mas_similar(jugadores, jugador_ideal):
    similitud_max = -math.inf
    jugador_mas_similar = None
    indice = 0

    for jugador in jugadores:
        similitud = np.float64(0)
        for caracteristica in GENES:
                simprev=(jugador_ideal[caracteristica]-jugador[caracteristica])
                similitud += max(simprev,0)
                # print(similitud)
                print(caracteristica, jugador[caracteristica], jugador_ideal[caracteristica], similitud)
        if similitud > similitud_max:
            similitud_max = similitud
            jugador_mas_similar = jugador
            jugadores.pop(indice)
        indice+=1
    return jugador_mas_similar
