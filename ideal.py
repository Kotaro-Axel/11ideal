

class JugadorIdeal :

    Portero = {
        "altura":0.97, 
        "agilidad":0.92, 
        "reflejos":0.94, 
        "velocidad":0.72, 
        "técnica":0.72, 
        "visión":0.88,
        "fisico":0.72, 
        "ppp":0.40, 
        "distancia_de_lanzamiento":0.90, 
        "distancia_de_tiro":0.72
    }

    Defensa = {
        "altura":0.84, 
        "agilidad":0.75, 
        "reflejos":0.75, 
        "velocidad":0.75, 
        "técnica":0.70, 
        "visión":0.75,
        "fisico":0.90, 
        "ppp":0.75, 
        "distancia_de_lanzamiento":0.10, 
        "distancia_de_tiro":0.80
    }

    Medio = {
        "altura":0.80, 
        "agilidad":0.80, 
        "reflejos":0.75, 
        "velocidad":0.80, 
        "técnica":0.85, 
        "visión":0.85,
        "fisico":0.75, 
        "ppp":0.90, 
        "distancia_de_lanzamiento":0.10, 
        "distancia_de_tiro":0.70
    }

    Delantero = {
        "altura":0.89, 
        "agilidad":0.85, 
        "reflejos":0.80, 
        "velocidad":0.85, 
        "técnica":0.85, 
        "visión":0.85,
        "fisico":0.80, 
        "ppp":0.70, 
        "distancia_de_lanzamiento":0.10, 
        "distancia_de_tiro":0.90
    }

    def __init__(self):
        self.Portero = self.Portero
        self.Defensa = self.Portero
        self.Medio = self.Portero
        self.Delantero = self.Portero