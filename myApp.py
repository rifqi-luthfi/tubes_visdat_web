from bokeh.models.widgets.sliders import DateRangeSlider
import pandas as pd
import numpy as np
import bokeh
from bokeh.io import curdoc, show, output_notebook
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, HoverTool, CustomJS, Select, CDSView, GroupFilter
from bokeh.layouts import column, row, layout
from bokeh.models.widgets import Tabs, Panel
from bokeh.models.annotations import Title
from bokeh.models.widgets.buttons import Dropdown


#tema untuk visualisai bokehdf
curdoc().theme = "dark_minimal"

output_notebook()

"""Read Dataset"""

data = pd.read_csv('./data/stock_market.csv')
# data

data.rename(columns = {'Adj Close':'Adj_Close'}, inplace = True)
data['Date'] = pd.to_datetime(data['Date'])
# data

#menetapkan 2 angka dibelakang koma
data = data.round(0)
data.tail()

# melihat tipe yang ada di feature name
marketList = data['Name'].unique()

#Melihat sebaran data
data1 = data[data['Name'] == 'HANG SENG']
data2 = data[data['Name'] == 'NASDAQ']
data3 = data[data['Name'] == 'NIKKEI']

# for i in [data1, data2, data3]:
#    # print(i.shape)

hang_seng_cds = ColumnDataSource(data1)
nasdaq_cds = ColumnDataSource(data2)
nikkei_cds = ColumnDataSource(data3)

fig_market= figure(sizing_mode="stretch_width", plot_height=350,
             x_axis_type='datetime', 
             x_axis_label='Month-Year', 
             y_axis_label='Price',
             y_axis_type="linear",
             title='Market Pasar Saham')

tooltips= [
                     ('Adj Close', '@Adj_Close'),
                     ('Date', '@Date{%F}')
]

fig_market.add_tools(HoverTool(tooltips=tooltips, formatters={'@Date': 'datetime'}))

cols1 = data[['Date','Adj_Close','Name']]
cols2 = cols1[cols1['Name'] == 'HANG SENG']
col1_cds = ColumnDataSource(data=cols1)
col2_cds = ColumnDataSource(data=cols2)

# callback for list market
callback_list_market = CustomJS(args=dict(source=col1_cds, sc=col2_cds), code="""
                                var f = cb_obj.value;
                                sc.data['Date'] = [];
                                sc.data['Adj_Close'] = [];
                                for(var i = 0; i <= source.get_length(); i++){
                                    if (source.data['Name'][i] == f){
                                        sc.data['Date'].push(source.data['Date'][i]);
                                        sc.data['Adj_Close'].push(source.data['Adj_Close'][i]);
                                    }
                                }
                                sc.change.emit();
                                """)
dropdown = Select(options=['HANG SENG', 'NASDAQ', 'NIKKEI'], value ='HANG SENG', title ='Stock Saham')   

fig_market.line(x='Date', y='Adj_Close', source=col2_cds, color='green')

fig = figure(sizing_mode="fixed", plot_height=500,
             x_axis_type='datetime', 
             x_axis_label='Month-Year', 
             y_axis_label='Price',
             y_axis_type="linear",
             title='Market Pasar Saham')

fig.add_tools(HoverTool(tooltips=tooltips, formatters={'@Date': 'datetime'}))

fig.line(x='Date', y='Adj_Close', source=hang_seng_cds, legend_label='Hang Seng', color='yellow')
fig.line(x='Date', y='Adj_Close', source=nasdaq_cds, legend_label='Nasdaq', color='green')
fig.line(x='Date', y='Adj_Close', source=nikkei_cds, legend_label='Nikkei', color='red')

dropdown.js_on_change('value', callback_list_market)


date_range_slider = DateRangeSlider(value=(min(data['Date']), max(data['Date'])),
                                    start=min(data['Date']), end=max(data['Date']))

date_range_slider.js_link("value", fig_market.x_range, "start", attr_selector=0)
date_range_slider.js_link("value", fig_market.x_range, "end", attr_selector=1)

date_range_slider_1 = DateRangeSlider(value=(min(data['Date']), max(data['Date'])),
                                    start=min(data['Date']), end=max(data['Date']))

date_range_slider_1.js_link("value", fig.x_range, "start", attr_selector=0)
date_range_slider_1.js_link("value", fig.x_range, "end", attr_selector=1)

# show(fig)
layout1 = column(dropdown, fig_market, date_range_slider)
layout2 = column(fig, date_range_slider_1)

tab1 = Panel(child=layout1,title="Pencarian Stock Saham")
tab2 = Panel(child=layout2,title="Visualisasi Semua Stock Saham")
tabs = Tabs(tabs=[ tab1, tab2 ])

curdoc().add_root(tabs)

# curdoc().add_root(layout)
# curdoc().title = "Stocks"