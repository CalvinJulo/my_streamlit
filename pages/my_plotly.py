# -*-coding:utf-8 -*-

"""
# File       : xx.py
# Time       ：2021/9/11 19:02
# Author     ：
# version    ：
# Description： 
"""

# CMD Run Command ： streamlit run /Users/stock/st_stock.py --server.port 8501

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)



import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np


def pick_dataset(dataset_name):
    dataset_dict ={
        'iris':px.data.iris(),
        # 'absolute_import':px.data.absolute_import(),
        'carshare':px.data.carshare(),
        'election':px.data.election(),
        'election_geojson':px.data.election_geojson(),
        'experiment':px.data.experiment(), 
        'gapminder':px.data.gapminder(),
        'medals_long':px.data.medals_long(), 
        'medals_wide':px.data.medals_wide(), 
        'stocks':px.data.stocks(), 
        'tips':px.data.tips(), 
        'wind':px.data.wind()                 
        }
    if dataset_name ==None:
        return None
    else:
        return dataset_dict[dataset_name]

dataset_list =['carshare', 'election', 'election_geojson', 'experiment', 'gapminder', 'iris', 'medals_long', 'medals_wide', 'stocks', 'tips', 'wind']
dataset = st.pills('Dataset',dataset_list)
df = pick_dataset(dataset)
if dataset =='election_geojson':
    show_df = {'type':df['type'],'features':df['features'][:2]}
    st.write(show_df)
elif dataset==None:
    pass
else:
    st.write(df.head())
    st.write(df.describe(include='all'))





st.write('''Basics: scatter, line, area, bar, funnel, timeline
Part-of-Whole: pie, sunburst, treemap, icicle, funnel_area
1D Distributions: histogram, box, violin, strip, ecdf
2D Distributions: density_heatmap, density_contour
Matrix or Image Input: imshow
3-Dimensional: scatter_3d, line_3d
Multidimensional: scatter_matrix, parallel_coordinates, parallel_categories
Tile Maps: scatter_map, line_map, choropleth_map, density_map
Outline Maps: scatter_geo, line_geo, choropleth
Polar Charts: scatter_polar, line_polar, bar_polar
Ternary Charts: scatter_ternary, line_ternary''')

        
    
df1 = px.data.iris()
fig1 = px.scatter(df1, x="sepal_width", y="sepal_length", color="species")
st.plotly_chart(fig1)

fig2 = px.scatter(df1, x="sepal_width", y="sepal_length", color="species", marginal_y="violin",
           marginal_x="box", template="simple_white")

st.plotly_chart(fig2)

df1["e"] = df1["sepal_width"]/100
fig3 = px.scatter(df1, x="sepal_width", y="sepal_length", color="species", error_x="e", error_y="e")
st.plotly_chart(fig3)

df4 = px.data.tips()
fig4 = px.bar(df4, x="sex", y="total_bill", color="smoker", barmode="group")
st.plotly_chart(fig4)

df5 = px.data.medals_long()
fig5 = px.bar(df5, x="medal", y="count", color="nation",
             pattern_shape="nation", pattern_shape_sequence=[".", "x", "+"])

st.plotly_chart(fig5)

df6 = px.data.tips()
fig6 = px.bar(df6, x="sex", y="total_bill", color="smoker", barmode="group", facet_row="time", facet_col="day",
       category_orders={"day": ["Thur", "Fri", "Sat", "Sun"], "time": ["Lunch", "Dinner"]})
st.plotly_chart(fig6)

df7 = px.data.iris()
fig7 = px.scatter_matrix(df7, dimensions=["sepal_width", "sepal_length", "petal_width", "petal_length"], color="species")
st.plotly_chart(fig7)

df8 = px.data.iris()
fig8 = px.parallel_coordinates(df8, color="species_id", labels={"species_id": "Species",
                  "sepal_width": "Sepal Width", "sepal_length": "Sepal Length",
                  "petal_width": "Petal Width", "petal_length": "Petal Length", },
                    color_continuous_scale=px.colors.diverging.Tealrose, color_continuous_midpoint=2)

st.plotly_chart(fig8)
df9 = px.data.tips()
fig9 = px.parallel_categories(df9, color="size", color_continuous_scale=px.colors.sequential.Inferno)
st.plotly_chart(fig9)

df10 = px.data.gapminder()
fig10 = px.scatter(df10.query("year==2007"), x="gdpPercap", y="lifeExp", size="pop", color="continent",
           hover_name="country", log_x=True, size_max=60)
st.plotly_chart(fig10)

df11 = px.data.gapminder()
fig11 = px.scatter(df11, x="gdpPercap", y="lifeExp", animation_frame="year", animation_group="country",
           size="pop", color="continent", hover_name="country", facet_col="continent",
           log_x=True, size_max=45, range_x=[100,100000], range_y=[25,90])
st.plotly_chart(fig11)


df12 = px.data.gapminder()
fig12 = px.line(df12, x="year", y="lifeExp", color="continent", line_group="country", hover_name="country",
        line_shape="spline", render_mode="svg")
st.plotly_chart(fig12)

df13 = px.data.gapminder()
fig13 = px.area(df13, x="year", y="pop", color="continent", line_group="country")
st.plotly_chart(fig13)


df14 = pd.DataFrame([
    dict(Task="Job A", Start='2009-01-01', Finish='2009-02-28', Resource="Alex"),
    dict(Task="Job B", Start='2009-03-05', Finish='2009-04-15', Resource="Alex"),
    dict(Task="Job C", Start='2009-02-20', Finish='2009-05-30', Resource="Max")
])

fig14 = px.timeline(df14, x_start="Start", x_end="Finish", y="Resource", color="Resource")
st.plotly_chart(fig14)

data15 = dict(
    number=[39, 27.4, 20.6, 11, 2],
    stage=["Website visit", "Downloads", "Potential customers", "Requested price", "Invoice sent"])
fig15 = px.funnel(data15, x='number', y='stage')
st.plotly_chart(fig15)



df16 = px.data.gapminder().query("year == 2007").query("continent == 'Europe'")
df16.loc[df16['pop'] < 2.e6, 'country'] = 'Other countries' # Represent only large countries
fig16 = px.pie(df16, values='pop', names='country', title='Population of European continent')
st.plotly_chart(fig16)


df17 = px.data.gapminder().query("year == 2007")
fig17 = px.sunburst(df17, path=['continent', 'country'], values='pop',color='lifeExp', hover_data=['iso_alpha'])
st.plotly_chart(fig17)


df18 = px.data.gapminder().query("year == 2007")
fig18 = px.treemap(df18, path=[px.Constant('world'), 'continent', 'country'], values='pop',color='lifeExp', hover_data=['iso_alpha'])
st.plotly_chart(fig18)


df19 = px.data.gapminder().query("year == 2007")
fig19 = px.icicle(df19, path=[px.Constant('world'), 'continent', 'country'], values='pop',color='lifeExp', hover_data=['iso_alpha'])
st.plotly_chart(fig19)


df20 = px.data.tips()
fig20 = px.histogram(df20, x="total_bill", y="tip", color="sex", marginal="rug", hover_data=df20.columns)
st.plotly_chart(fig20)


df21 = px.data.tips()
fig21 = px.box(df21, x="day", y="total_bill", color="smoker", notched=True)
st.plotly_chart(fig21)


df22 = px.data.tips()
fig22 = px.violin(df22, y="tip", x="smoker", color="sex", box=True, points="all", hover_data=df22.columns)
st.plotly_chart(fig22)

df23 = px.data.tips()
fig23 = px.ecdf(df23, x="total_bill", color="sex")
st.plotly_chart(fig23)

df24 = px.data.tips()
fig24 = px.strip(df24, x="total_bill", y="time", orientation="h", color="smoker")
st.plotly_chart(fig24)


df25 = px.data.iris()
fig25 = px.density_contour(df25, x="sepal_width", y="sepal_length")
st.plotly_chart(fig25)


df26 = px.data.iris()
fig26 = px.density_heatmap(df26, x="sepal_width", y="sepal_length", marginal_x="rug", marginal_y="histogram")
st.plotly_chart(fig26)


data27=[[1, 25, 30, 50, 1], [20, 1, 60, 80, 30], [30, 60, 1, 5, 20]]
fig27 = px.imshow(data27,
                labels=dict(x="Day of Week", y="Time of Day", color="Productivity"),
                x=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
                y=['Morning', 'Afternoon', 'Evening']
               )
fig27.update_xaxes(side="top")
st.plotly_chart(fig27)


df28 = px.data.carshare()
fig28 = px.scatter_map(df28, lat="centroid_lat", lon="centroid_lon", color="peak_hour", size="car_hours",
                  color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10,
                  map_style="carto-positron")
st.plotly_chart(fig28)

df29 = px.data.election()
geojson29 = px.data.election_geojson()
fig29 = px.choropleth_map(df29, geojson=geojson29, color="Bergeron",
                           locations="district", featureidkey="properties.district",
                           center={"lat": 45.5517, "lon": -73.7073},
                           map_style="carto-positron", zoom=9)
st.plotly_chart(fig29)

df30 = px.data.gapminder()
fig30 = px.scatter_geo(df30, locations="iso_alpha", color="continent", hover_name="country", size="pop",
               animation_frame="year", projection="natural earth")

st.plotly_chart(fig30)

df31 = px.data.gapminder()
fig31 = px.choropleth(df31, locations="iso_alpha", color="lifeExp", hover_name="country", animation_frame="year", range_color=[20,80])
st.plotly_chart(fig31)




df32 = px.data.wind()
fig32 = px.scatter_polar(df32, r="frequency", theta="direction", color="strength", symbol="strength",
            color_discrete_sequence=px.colors.sequential.Plasma_r)
st.plotly_chart(fig32)


df33 = px.data.wind()
fig33 = px.line_polar(df33, r="frequency", theta="direction", color="strength", line_close=True,
            color_discrete_sequence=px.colors.sequential.Plasma_r)
st.plotly_chart(fig33)

df34 = px.data.wind()
fig34 = px.bar_polar(df34, r="frequency", theta="direction", color="strength", template="plotly_dark",
            color_discrete_sequence= px.colors.sequential.Plasma_r)
st.plotly_chart(fig34)

df35 = px.data.election()
fig35 = px.scatter_3d(df35, x="Joly", y="Coderre", z="Bergeron", color="winner", size="total", hover_name="district",
                  symbol="result", color_discrete_map = {"Joly": "blue", "Bergeron": "green", "Coderre":"red"})

st.plotly_chart(fig35）

df36 = px.data.election()
fig36 = px.scatter_ternary(df36, a="Joly", b="Coderre", c="Bergeron", color="winner", size="total", hover_name="district",
                   size_max=15, color_discrete_map = {"Joly": "blue", "Bergeron": "green", "Coderre":"red"} )

st.plotly_chart(fig36)








