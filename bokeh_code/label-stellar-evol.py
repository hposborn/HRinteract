import pandas as pd
import numpy as np
from bokeh.layouts import column, row
from bokeh.models import Select, CustomJS, Slider
from bokeh.palettes import Spectral5
from bokeh.plotting import curdoc, figure, show
from bokeh.models import ColumnDataSource, NumeralTickFormatter, HoverTool
from bokeh.transform import cumsum

import astropy.io.ascii as ascii
df=ascii.read("../Data/MIST_iso_60d24e849c2d1.iso").to_pandas()

#filt=df.loc[(df['initial_mass']<10) | (df['log10_isochrone_age_yr']==5)]



nselect = 3000
select_ix=np.random.choice(len(df), nselect, replace=False)
df=df.loc[select_ix,[col for col in df.columns if 'cent' not in col and 'surf' not in col]]




SIZES = list(range(6, 22, 3))
COLORS = Spectral5
N_SIZES = len(SIZES)
N_COLORS = len(COLORS)

columns = sorted(df.columns)
discrete = [x for x in columns if df[x].dtype == object]
continuous = [x for x in columns if x not in discrete]

def create_figure():

    ageranges = df.index
    #(df['log10_isochrone_age_yr']>age.value-0.25)*(df['log10_isochrone_age_yr']<age.value+0.25)

    xs = np.random.normal(df.loc[ageranges,x.value].values,0.01*np.median(abs(np.diff(df.loc[ageranges,x.value].values))))
    ys = np.random.normal(df.loc[ageranges,y.value].values,0.01*np.median(abs(np.diff(df.loc[ageranges,x.value].values))))
    x_title = x.value.title()
    y_title = y.value.title()

    kw = dict()
    if x.value in discrete:
        kw['x_range'] = sorted(set(xs))
    if y.value in discrete:
        kw['y_range'] = sorted(set(ys))
    kw['title'] = "%s vs %s" % (x_title, y_title)

    p = figure(height=600, width=800, tools='pan,box_zoom,hover,reset', **kw)
    #p = figure(height=600, width=800, tools=' ', **kw)
    
    p.xaxis.axis_label = x_title
    p.yaxis.axis_label = y_title

    if x.value in discrete:
        p.xaxis.major_label_orientation = pd.np.pi / 4

    sz = 9
    if size.value != 'None':
        if len(set(df[size.value])) > N_SIZES:
            groups = pd.qcut(df[size.value].values, N_SIZES, duplicates='drop')
        else:
            groups = pd.Categorical(df[size.value])
        sz = [SIZES[xx] for xx in groups.codes]

    c = "#31AADE"
    if color.value != 'None':
        if len(set(df[color.value])) > N_COLORS:
            groups = pd.qcut(df[color.value].values, N_COLORS, duplicates='drop')
        else:
            groups = pd.Categorical(df[color.value])
        c = [COLORS[::-1][xx] for xx in groups.codes]
        
    
    

    if x.value=='log_Teff':
        p.x_range.flipped = True
    if (y.value=='log_L' and x.value=='log_Teff'):
        q = np.array([4.5, 5.3, 4, 3.7, 3.8])
        r = np.array([-1, 6, 1, 3, 6 ])
        n = np.array(['White dwarfs', 'Planetary Nebula', 'Main Sequence', 'Red Giants', 'Asymptotic giant branch stars'])
        p.circle(x=xs, y=ys, color=c, size=sz, line_color="white", alpha=0.6, hover_color='white', hover_alpha=0.5)
        p.text(q, r, text=n,text_baseline="middle", text_align="center", color='black')
        
    
    show(p)
    return p
    
    
    


    
    
def update(attr, old, new):
    layout.children[1] = create_figure()


x = Select(title='X-Axis', value='log_Teff', options=columns)
x.on_change('value', update)

y = Select(title='Y-Axis', value='log_L', options=columns)
y.on_change('value', update)

size = Select(title='Size', value='log_R', options=['None'] + continuous)
size.on_change('value', update)

color = Select(title='Color', value='log_Teff', options=['None'] + continuous)
color.on_change('value', update)


slider = Slider(start=5, end=10.5, value=4.5, step=0.1, title="Age")
slider.js_on_change("age", CustomJS(code="""
    console.log('slider: age=' + this.age, this.toString())
"""))

controls = column(x, y, color, size, width=200)
layout = row(controls, create_figure())

curdoc().add_root(layout)
curdoc().title = "HR Diagram"

