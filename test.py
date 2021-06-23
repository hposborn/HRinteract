import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mpld3
import matplotlib.colors
from mpld3 import plugins
import pandas as pd


# Define some CSS to control our custom labels
css = """
table
{
  border-collapse: collapse;
}
th
{
  color: #ffffff;
  background-color: #000000;
}
td
{
  background-color: #cccccc;
}
table, th, td
{
  font-family:Arial, Helvetica, sans-serif;
  border: 1px solid black;
  text-align: right;
}
"""


columns=["EEP","log10_isochrone_age_yr","initial_mass","star_mass","star_mdot","he_core_mass","c_core_mass","log_L","log_LH","log_LHe","log_Teff","log_R","log_g","surface_h1","surface_he3","surface_he4","surface_c12","surface_o16","log_center_T","log_center_Rho","center_gamma","center_h1","center_he4","center_c12","phase"];

df=pd.read_csv("../HRinteract//Data/MIST_iso_60d24e849c2d1.iso",skip_blank_lines=True, comment="#",delim_whitespace=True, header=None, names=columns);



ind= df['log10_isochrone_age_yr'] == 6.5

df1=df[ind]
N=len(df1)

labels=[]
for i in range(N):
    #label = df.iloc[[i], :].T
    label=df1.iloc[[i],:].T
    label.columns = ['Row {0}'.format(i)]
    # .to_html() is unicode; so make leading 'u' go away with str()
    labels.append(str(label.to_html()))
    print(label)
    
fig, ax = plt.subplots()
ax.grid(True, alpha=0.3)
ax.set_xlabel('log_Teff')
ax.set_ylabel('log_L')
ax.set_title('HTML tooltips', size=20)
x=df1["log_Teff"]
y=df1["log_L"]

points = ax.plot(x, y, 'o', color='b', mec='k', ms=15, mew=1, alpha=.6)





tooltip = plugins.PointHTMLTooltip(points[0], labels,
                                   voffset=10, hoffset=10, css=css)
plugins.connect(fig, tooltip)

mpld3.show()
mpld3.save_html(fig,'hr.html')


