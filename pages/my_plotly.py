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
df16.loc[df['pop'] < 2.e6, 'country'] = 'Other countries' # Represent only large countries
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














