

class JugadorIdeal :

    Portero = {
        "altura":0.95, 
        "agilidad":0.90, 
        "reflejos":0.90, 
        "velocidad":0.70, 
        "técnica":0.70, 
        "visión":0.75,
        "fisico":0.70, 
        "ppp":0.50, 
        "distancia_de_lanzamiento":0.95, 
        "distancia_de_tiro":0.70
    }

    Defensa = {
        "altura":0.85, 
        "agilidad":0.75, 
        "reflejos":0.75, 
        "velocidad":0.85, 
        "técnica":0.70, 
        "visión":0.75,
        "fisico":0.90, 
        "ppp":0.75, 
        "distancia_de_lanzamiento":0.70, 
        "distancia_de_tiro":0.80
    }

    Medio = {
        "altura":0.80, 
        "agilidad":0.80, 
        "reflejos":0.80, 
        "velocidad":0.80, 
        "técnica":0.85, 
        "visión":0.90,
        "fisico":0.75, 
        "ppp":0.90, 
        "distancia_de_lanzamiento":0.70, 
        "distancia_de_tiro":0.75
    }

    Delantero = {
        "altura":0.88, 
        "agilidad":0.85, 
        "reflejos":0.80, 
        "velocidad":0.85, 
        "técnica":0.90, 
        "visión":0.80,
        "fisico":0.85, 
        "ppp":0.70, 
        "distancia_de_lanzamiento":0.70, 
        "distancia_de_tiro":0.90
    }

    def __init__(self):
        self.Portero = self.Portero
        self.Defensa = self.Defensa
        self.Medio = self.Medio
        self.Delantero = self.Delantero