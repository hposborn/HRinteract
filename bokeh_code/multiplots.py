import pandas as pd
import numpy as np
from bokeh.palettes import Spectral11
from bokeh.models import ColumnDataSource, Slider, Select, CDSView, BooleanFilter
from bokeh.plotting import figure
from bokeh.layouts import column, row
from bokeh.io import curdoc
from random import sample

import astropy.io.ascii as ascii
#df=ascii.read("../Data/MIST_iso_60d24e849c2d1.iso").to_pandas()
df=pd.read_csv("../Data/MIST_iso_60d24e849c2d1_short.csv")

df['AbsMag']=4.83 - 2.5*df['log_L']

#Initialising interactive parts:
columns = sorted(df.columns)
discrete = [x for x in columns if df[x].dtype == object]
continuous = [x for x in columns if x not in discrete]

df['size']=np.tile(1,len(df))
df['col']=np.tile('',len(df))

all_source = ColumnDataSource(data=df)

x = Select(title='X-Axis', value='log_Teff', options=columns)
y = Select(title='Y-Axis', value='log_L', options=columns)
size = Select(title='Size', value='log_R', options=['None'] + continuous)
color = Select(title='Color', value='log_Teff', options=['None'] + continuous)
slider_age=Slider(start=5, end=10.5, value=7.5, step=0.5, title="Age [Gyr]")

#Values needed for randomised data selection:
nselect=1200
p=np.clip(nselect/len(df),0,0.99)

view = CDSView(source=all_source, filters=[BooleanFilter(all_source.data["log10_isochrone_age_yr"]<(slider_age.value+0.55)),
                                           BooleanFilter(all_source.data["log10_isochrone_age_yr"]>(slider_age.value-0.55)),
                                           BooleanFilter(np.random.choice(a=[False, True], size=len(df), p=[1-p, p]))])

def update_source_filter():
    f1=all_source.data["log10_isochrone_age_yr"]<(slider_age.value+0.55)
    f2=all_source.data["log10_isochrone_age_yr"]>(slider_age.value-0.55)
    f3=np.random.choice(a=[False, True], size=len(all_source.data['index']), p=[1-p, p])
    view = CDSView(source=all_source, filters=[BooleanFilter(f1),BooleanFilter(f2),BooleanFilter(f3)])
    return view

def create_figure1(view):
    #Setting up (randomised) Age-constrained data to be used in plotting:

    #Setting up colour and sizes:
    SIZES = list(range(6, 22, 3))
    N_SIZES = len(SIZES)
    
    TOOLTIPS = [
    ("Mass", "@star_mass"),
    ("log(Radius)", "@log_R"),
    ("log(Teff)", "@log_Teff"),
    ("Age", "@log10_isochrone_age_yr")
    ]

    # Plot scatter with data from source
    plot1 = figure(plot_height=550, plot_width=700, tools="crosshair,box_zoom,reset,save,wheel_zoom,hover",tooltips=TOOLTIPS)    
    plot1.xaxis.axis_label = x.value.title()
    plot1.yaxis.axis_label = y.value.title()


    
    #Making sizes integer intervals
    if len(set(all_source.data[size.value])) > N_SIZES:
        groups = pd.qcut(all_source.data[size.value], N_SIZES, duplicates='drop')
    else:
        groups = pd.Categorical(all_source.data[size.value])
    all_source.data['size'] = [SIZES[xx] for xx in groups.codes]

    #Making colours integer intervals
    if len(set(all_source.data[color.value])) > 11:
        groups = pd.qcut(all_source.data[color.value], 11, duplicates='drop')
    else:
        groups = pd.Categorical(all_source.data[color.value])
    all_source.data['color'] = [Spectral11[::-1][xx] for xx in groups.codes]
    
    plot1.circle(x=x.value, y=y.value, color='color', size='size', source=all_source, view=view)

    if (y.value=='log_L' and x.value=='log_Teff'):
        q = np.array([4.5, 5.3, 4, 3.7, 3.8])
        r = np.array([-1, 6, 1, 3, 6 ])
        n = np.array(['White\ndwarfs', 'Planetary\nNebulae', 'Main\nSequence', 'Red\nGiants', 'Asymptotic\ngiant branch'])
        plot1.text(q, r, text=n,text_baseline="middle", text_align="center", color='black',text_font_size='8pt')

    if x.value=='log_Teff' or x.value=='log_G':
        plot1.x_range.flipped = True
        #=(xs.min(), xs.max())
    if y.value=='log_Teff' or y.value=='log_G':
        plot1.y_range.flipped = True
        #=(xs.min(), xs.max())
    return plot1

def create_figure2(view):
    # Plot graph two with data from df2 and source 2 as line
    single_source_ix = np.random.randint(len(all_source.data['log_L']))
    plot2 = figure(plot_height=260, plot_width=300, title="place_holder_1_for_structure", 
                tools="crosshair,box_zoom,reset,save,wheel_zoom,hover")    
    plot2.circle(x=all_source.data['log_L'][single_source_ix], y=all_source.data['log10_isochrone_age_yr'][single_source_ix])
    # safe data from plot 2 for later change in subroutine
    return plot2

def create_figure3(view):
    # Plot graph two with data from df2 and source 2 as line
    single_source_ix = np.random.randint(len(all_source.data['log_L']))
    plot2 = figure(plot_height=260, plot_width=300, title="place_holder_2_for_structure", 
                tools="crosshair,box_zoom,reset,save,wheel_zoom,hover")    
    plot2.circle(x=all_source.data['log_L'][single_source_ix], y=all_source.data['log10_isochrone_age_yr'][single_source_ix])
    # safe data from plot 2 for later change in subroutine
    return plot2

def updateplot1(attr, old, new):
    update_source_filter()
    layout.children[1] = create_figure1(view)

def updateplots(attr, old, new):
    view = update_source_filter()
    extras.children[0] = create_figure2(view)
    extras.children[1] = create_figure3(view)
    layout.children[1] = create_figure1(view)

controls = column(x, y, color, size, slider_age, width=200)
extras = column(create_figure2(view), create_figure3(view))
layout = row(controls, create_figure1(view), extras)

# add taptool to HR_points plot
slider_age.on_change('value',updateplots)
x.on_change('value', updateplot1)
y.on_change('value', updateplot1)
size.on_change('value', updateplot1)
color.on_change('value', updateplot1)

curdoc().add_root(layout)
curdoc().title = "interact"