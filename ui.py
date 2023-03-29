import matplotlib.pyplot as plt
import numpy as np
from ideal import JugadorIdeal
from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D
from test import initiate_genetic
from itertools import chain


Portero_ideal = list(JugadorIdeal.Portero.values())
Defensa_ideal = list(JugadorIdeal.Defensa.values())
Medio_ideal = list(JugadorIdeal.Medio.values())
Delantero_ideal = list(JugadorIdeal.Delantero.values())

def radar_factory(num_vars, frame='circle'):
    """
    Create a radar chart with `num_vars` axes.

    This function creates a RadarAxes projection and registers it.

    Parameters
    ----------
    num_vars : int
        Number of variables for radar chart.
    frame : {'circle', 'polygon'}
        Shape of frame surrounding axes.

    """
    # calculate evenly-spaced axis angles
    theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)

    class RadarTransform(PolarAxes.PolarTransform):

        def transform_path_non_affine(self, path):
            # Paths with non-unit interpolation steps correspond to gridlines,
            # in which case we force interpolation (to defeat PolarTransform's
            # autoconversion to circular arcs).
            if path._interpolation_steps > 1:
                path = path.interpolated(num_vars)
            return Path(self.transform(path.vertices), path.codes)

    class RadarAxes(PolarAxes):

        name = 'radar'
        PolarTransform = RadarTransform

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # rotate plot such that the first axis is at the top
            self.set_theta_zero_location('N')

        def fill(self, *args, closed=True, **kwargs):
            """Override fill so that line is closed by default"""
            return super().fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            """Override plot so that line is closed by default"""
            lines = super().plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)

        def _close_line(self, line):
            x, y = line.get_data()
            # FIXME: markers at x[0], y[0] get doubled-up
            if x[0] != x[-1]:
                x = np.append(x, x[0])
                y = np.append(y, y[0])
                line.set_data(x, y)

        def set_varlabels(self, labels):
            self.set_thetagrids(np.degrees(theta), labels)

        def _gen_axes_patch(self):
            # The Axes patch must be centered at (0.5, 0.5) and of radius 0.5
            # in axes coordinates.
            if frame == 'circle':
                return Circle((0.5, 0.5), 0.5)
            elif frame == 'polygon':
                return RegularPolygon((0.5, 0.5), num_vars,
                                      radius=.5, edgecolor="k")
            else:
                raise ValueError("Unknown value for 'frame': %s" % frame)

        def _gen_axes_spines(self):
            if frame == 'circle':
                return super()._gen_axes_spines()
            elif frame == 'polygon':
                # spine_type must be 'left'/'right'/'top'/'bottom'/'circle'.
                spine = Spine(axes=self,
                              spine_type='circle',
                              path=Path.unit_regular_polygon(num_vars))
                # unit_regular_polygon gives a polygon of radius 1 centered at
                # (0, 0) but we want a polygon of radius 0.5 centered at (0.5,
                # 0.5) in axes coordinates.
                spine.set_transform(Affine2D().scale(.5).translate(.5, .5)
                                    + self.transAxes)
                return {'polar': spine}
            else:
                raise ValueError("Unknown value for 'frame': %s" % frame)

    register_projection(RadarAxes)
    return theta


def example_data(player):
    data = [
        ['Altura', 'Agilidad', 'Reflejos', 'Velocidad', 'Técnica', 'Visión', 'Físico', 'PPP', 'Distancia de lanzamiento','Distancia de tiro'],
        
        ('Defensa', [
            Defensa_ideal,player[40:50],player[50:60],player[60:70],player[70:80]]),
        ('Portero', [
            Portero_ideal,player[0:10]]),
        ('Medio', [
            Medio_ideal,player[80:90],player[90:100],player[100:110],player[110:120]]),
    ('Delantero', [
            Delantero_ideal,player[120:130],player[140:150]])
    ]
    return data

def create_player(player):
    posiciones = ["Portero 1", "Portero 2", "Portero 3", "Portero 4", "Defensa 1", "Defensa 2", "Defensa 3", "Defensa 4"
                  ,  "Medio 1", "Medio 2", "Medio 3", "Medio 4", "Delantero 1", "Delantero 2", "Delantero 3", "Delantero 4"]
    mejores_jugadores=[]
    # print(player[0])
    playerflatten= list(chain.from_iterable(player[0]))
    # print(playerflatten.__len__() )
    for posicion in posiciones:
        # print(posicion)
        caracteristicas = playerflatten[(posiciones.index(posicion))]
        
        # print(caracteristicas)
        for caracteristica,valor in caracteristicas.items():
            # print(caracteristica)
            mejores_jugadores.append(valor)
        mejores_jugadores.pop()
        
            
    return mejores_jugadores
def create_learning_curve(player):
    # print("hey")
    # mejorgen=min(player[0])
    # print("La mejor generacion es la: ",player.index(mejorgen))
    plt.title("Magnitud de la diferencia conforme a las iteraciones")
    plt.xlabel("Iteracion")
    plt.ylabel("Valor de la diferencia")
    plt.plot(player[0],color="red", label="Mejor:")
    plt.plot(player[1],color="blue", label="Peor:")
    plt.plot(player[2],color="green", label="Promedio:")
    plt.legend()
    plt.show()

def main(probabilidad,generaciones):
    N = 10
    theta = radar_factory(N, frame='polygon')
    player =[]
    # probabilidad,generaciones=0.5,10
    player=initiate_genetic(probabilidad,generaciones)
    # print(player.__len__())
    players=create_player(player)
    data = example_data(players)
    spoke_labels = data.pop(0)

    fig, axs = plt.subplots(figsize=(9, 9), nrows=2, ncols=2,
                            subplot_kw=dict(projection='radar'))
    fig.subplots_adjust(wspace=0.75, hspace=0.50, top=0.85, bottom=0.05)

    colors = ['b', 'r', 'g', 'm', 'y']
    for ax, (title, case_data) in zip(axs.flat, data):
        ax.set_rgrids([0.2, 0.4, 0.6, 0.8])
        ax.set_title(title, weight='bold', size='medium', position=(0.5, 1.1),
                     horizontalalignment='center', verticalalignment='center')
        for d, color in zip(case_data, colors):
            ax.plot(theta, d, color=color)
            ax.fill(theta, d, facecolor=color, alpha=0.25, label='_nolegend_')
        ax.set_varlabels(spoke_labels)
    labels = ('modelo', 'Jugador 1', 'Jugador 2', 'Jugador 3', 'Jugador 4')
    legend = axs[0, 0].legend(labels, loc=(0.9, .95),
                              labelspacing=0.1, fontsize='small')

    fig.text(0.5, 0.965, 'Mejor generación de jugadores vs jugador ideal',
             horizontalalignment='center', color='black', weight='bold',
             size='large')

    plt.show()
    create_learning_curve(player[1])
# main(0.5,10)