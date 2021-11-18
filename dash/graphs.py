import torch
import plotly.express as px
import plotly.graph_objects as go

from torch.fft import rfft

def fig_flow (flows): 
    m = flows.mean([1])
    flows = (flows - m) * torch.sign(m)
    x = list(torch.linspace(0, 1, flows.shape[1]))
    y = [list(f) for f in flows]
    fig = px.line(x=x, y=y)
    fig.for_each_trace(
        lambda t: t.update(name = "pulse", line_color='#f82'))
    fig.update_layout(
            showlegend=False, 
            margin=dict(l=30, r=30, t=30, b=30),
            height=300)
    return fig
