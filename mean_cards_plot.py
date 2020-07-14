import plotly.express as px
import pandas as pd

def get_session_length(df):
    ''' Calculate length of session in seconds'''
    df['session_start'] = pd.to_datetime(df['session_start'])
    df['session_end'] = pd.to_datetime(df['session_end'])
    time_deltas = df['session_end'] - df['session_start']
    session_length = []
    for d in time_deltas:
        session_length.append(d.total_seconds())
    return session_length

def get_start_hour(df):
    '''Isolate start hour from datetime object'''
    start_hour = []
    for t in df['session_start']:
        start_hour.append(t.hour)
    return start_hour

def get_cards_per_min(df):
    '''Calculate cards viewed per minute'''
    cards_per_min = (df['total_looked_at'] / df['session_length']) * 60
    return cards_per_min

def make_bar_chart(df):
    """Makes bar chart based on input dataframe"""
    df['session_length'] = get_session_length(df)
    
    df['start_hour'] = get_start_hour(df)
    
    df['cards_per_min'] = get_cards_per_min(df)
    
    # Make a dictionary containing start hours and mean cards per minute
    means = {}
    for h in range(0,24):
        scratch_df = df[df['start_hour'] == h]
        means[h] = scratch_df['cards_per_min'].mean()
    
    # Convert dictionary to dataframe
    px_df = pd.DataFrame(data=means, index=['mean_cards_per_min']).T
    px_df = px_df.reset_index().rename(columns={'index':'start_hour'})
    
    # Create figure from dataframe
    fig = px.bar(px_df, x='start_hour', y='mean_cards_per_min')
    
    # Return figure as HTML frame
    return fig.write_html('templates/mean_cards_per_min.html')

# Function to retrieve actual user data goes here
df = pd.read_csv('test_data/mean_cards_test.csv')
make_bar_chart(df)