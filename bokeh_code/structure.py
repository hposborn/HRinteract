import pandas as pd
import numpy as np
from bokeh.layouts import column, row
from bokeh.models import Select, CustomJS, Slider
from bokeh.palettes import Spectral5
from bokeh.plotting import curdoc, figure, show, output_file
from bokeh.models import ColumnDataSource, NumeralTickFormatter, HoverTool
from bokeh.transform import cumsum

import astropy.io.ascii as ascii
df=ascii.read("../Data/MIST_iso_60d24e849c2d1.iso").to_pandas()

c_mass=df['c_core_mass']
he_mass=df['he_core_mass']
star_mass=df['star_mass']
plot1 = figure(width = 300, height = 300)
plot1.annular_wedge(x = 0, y = 0, inner_radius =he_mass**0.5, outer_radius = star_mass**0.5, start_angle = 0, end_angle = 6.5, line_color = "white", fill_color ="blue")
show(plot1)

#plot2 = figure(width = 300, height = 300)
#plot2.annular_wedge(x = 0, y = 0, inner_radius =c_mass**0.5, outer_radius = star_mass**0.5, start_angle = 0, end_angle = 6.5, line_color = "white", fill_color ="yellow")
#show(plot2)