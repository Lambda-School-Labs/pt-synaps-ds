import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

def leitner_proportions(df):

    denom = df.shape[0]
    prop_dict = {}

    for i in range(1,6):
        df_i = df[df['comfort_level'] == i]
        numer = df_i.shape[0]
        prop_dict[i] = numer / denom

    plotly_df = pd.DataFrame.from_dict([prop_dict], orient='columns')    
    
    return plotly_df

def get_label_locs(plotly_df):
    
    # TODO: Make this put the numbers in the correct places even on non-dummy 
    # data
    df_t = plotly_df.T.rename(columns={0:'proportion'})
    
    locs = {}
    
    for prop, text in zip(df_t['proportion'], df_t.index):
        locs[text] = prop

def leitner_bar(plotly_df):
    
    fig = px.bar(plotly_df, orientation='h', width=400, height=200)
    fig.update_xaxes(
        showticklabels=False,
        showgrid=False,
        title_text='')
    fig.update_yaxes(showticklabels=False,
        showgrid=False,
        showline=False,
        zeroline=False,
        title_text='')
    fig.update_layout(
        plot_bgcolor = '#ffffff',
        showlegend = False,
        # Works perfectly for dummy data. 
        # TODO: Make it work for other data by finishing get_label_locs()
        annotations=[
            dict(
            x=0,
            y=-0.2,
            text=1,
            showarrow=False,
            xref='paper',
            yref='paper'
            ),
            dict(
            x=0.36,
            y=-0.2,
            text=2,
            showarrow=False,
            xref='paper',
            yref='paper'
            ),
            dict(
            x=0.53,
            y=-0.2,
            text=3,
            showarrow=False,
            xref='paper',
            yref='paper'
            ),
            dict(
            x=0.72,
            y=-0.2,
            text=4,
            showarrow=False,
            xref='paper',
            yref='paper'
            ),
            dict(
            x=0.88,
            y=-0.2,
            text=5,
            showarrow=False,
            xref='paper',
            yref='paper'
            )
        ]
        )
    fig.update_traces(marker=dict(color="#FF909A"),
                     selector=dict(name='Level 1'))
    fig.update_traces(marker=dict(color="#EFC9ED"),
                     selector=dict(name='Level 2'))
    fig.update_traces(marker=dict(color="#C8F5FF"),
                     selector=dict(name='Level 3'))
    fig.update_traces(marker=dict(color="#D5E3FF"),
                     selector=dict(name='Level 4'))
    fig.update_traces(marker=dict(color="#FFF4BD"),
                     selector=dict(name='Level 5'))
    fig.show()
#     return fig.to_json()