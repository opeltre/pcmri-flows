import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash import callback_context
import plotly.express as px

import torch
import json
from os import path 
from glob import glob
from graphs import fig_pulses, fig_raw, fig_spectrum

from pcmri import Dataset

#--- Flow pulses ---
db = Dataset('full')

def pulse_keys(tag):
    return [k for k, tk in db_tags.items()\
              if ["good", "noisy", "bad"][tk] == tag]

#--- State ---
global keys
global index
tag     = "good" 
keys    = pulse_keys(tag)
index   = 0

#--- app ---
app = dash.Dash(__name__)

#--- Controls ---

controls = html.Div(id="controls", children=[
    html.Div(children=[
        html.Span(children='Pulses: '),
        dcc.Input(id='n-pulses', value=12)
    ])
])

tags = html.Div(id="tags", children=[
    html.Button(id="good", children='Good'),
    html.Button(id="noisy", children='Noisy'),
    html.Button(id="bad", children='Bad')
])
seek = html.Div(id="seek", children=[
    html.Button(id="prev", children="<"),
    html.Button(id="next", children=">")])
btns = html.Div(id="btns", children=[tags, seek])

keydiv = html.Div(id='key', children=f'inf_20160913115100_INF2')
tagdiv = html.Div(id='tag', children='good')
info = html.Div(id="info", children=[tagdiv, keydiv])

#--- Layout --- 

app.layout = html.Div(children=[
    html.Div(className="flex-h", 
             children=[controls, btns, info]),
    dcc.Graph(id='segments')
])

#--- Callbacks ---

@app.callback(
    Output('segments', 'figure'),
    Input('key', 'children'),
    Input('n-pulses', 'value'))
def update_exam(key, n):
    flows = db.get(key).flow()
    flows *= torch.sign(torch.mean([1]))
    print(flows)
    pulses = data["pulses"]
    try:
        Npulses = int(n) 
    except:
        Npulses = 1
    return fig_flow(flow, Npulses)

@app.callback(
    Output('tag', 'children'),
    Input('good', 'n_clicks'),
    Input('noisy', 'n_clicks'),
    Input('bad', 'n_clicks'))
def tag_exam(n1, n2, n3):
    changed = [p['prop_id'] for p in callback_context.triggered][0]
    print(f"changed: {changed}")
    tag = changed.split(".")[0]
    tag = tag if tag in ["good", "noisy", "bad"] else "good"
    global keys
    keys = pulse_keys(tag)
    return tag

@app.callback(
    Output('key', 'children'),
    Input('prev', 'n_clicks'),
    Input('next', 'n_clicks'))
def seek_exam(p, n):
    changed = [p['prop_id'] for p in callback_context.triggered][0]
    print(f"changed: {changed}")
    btn = changed.split(".")[0]
    if btn == "prev":
        mv = -1
    elif btn == "next":
        mv = +1
    else:
        mv = 0
    global keys
    global index
    index += mv
    return keys[(index + mv) % len(keys)]

#--- Run on 8050 ---

if __name__ == '__main__':
    app.run_server(debug=True)
