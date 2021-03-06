import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from datetime import datetime, timedelta
import pandas as pd

today = str(datetime.now() -timedelta(hours=9))
tomorrow = str(pd.to_datetime(today[:10], format='%Y-%m-%d') + timedelta(days=1))
my_path ='../spyre/data/'
odds_path = '../spyre/odds_data/'
today_odds_path = odds_path+ today[:10]

match_nsc = pd.read_csv(my_path+ today[:10] + '.txt')
match_nsc_en = pd.read_csv(my_path+ today[:10] + '_en.txt')
match_nsc_all = pd.concat([match_nsc, match_nsc_en], ignore_index=True)
# mtype = list(match_nsc_all['mtype'].unique())
#
# option_type = [{'label': mtype[i], 'value': mtype[i]} for i in range(len(mtype))]

def get_match_type(lang):
    return list(match_nsc_all.loc[match_nsc_all.lang==str(lang)]['mtype'].unique())

def get_odds_eu(ref):
    df_eu = pd.read_csv(today_odds_path + '/' + str(ref) + '_eu.txt', index_col=False)
    return  df_eu[['home','draw','away','dt']]

def get_odds_asian(ref):
    df_asia = pd.read_csv(today_odds_path + '/' + str(ref) + '_asia.txt', index_col=False)
    return df_asia[['home', 'pankou' ,'away', 'dt']]



app = dash.Dash()
server = app.server
app.layout = html.Div([
    html.Div([
            html.H4(children="顶级赛事赔率观测 |\nFootball match odds monitor |\n----visualized by 4sea Data"
                    , style={'textAlign':'left', 'backgroundColor':'#563D7B',
               'color':'#F8F9FA', 'font-size':'24px', 'font':'Bebas Neue'}),
        ], className='header'),


    html.Div([


        html.Div([
            dcc.Dropdown(
                id='match-type-checklist',
            #     options=option_type,
            #     values=[option_type[i]['value'] for i in range(len(option_type))],
            #     labelStyle={'display': 'inline-block', 'font-size': '13px'}
            multi=True),
        ], className='six columns', style={ 'font-size':'12px', "textAlign":'left'}),

        html.Div([
            html.Label('language'),
            dcc.RadioItems(
                id='lang-select',
                options=[
                    {'label': 'EN', 'value': 'en'},
                    {'label': '中文', 'value': 'zh_cn'},

                ],
                value='zh_cn', labelStyle={'display': 'inline-block', 'font-size': '13px'}
            ),
        ], className='six columns', style={'font-size': '14px', "textAlign": 'right'}),

    ], className='row'),
    # html.Br([]),
    html.Div([

        html.Div([

            html.Br(),
            html.Label('Match Day: {} to {} UTC+08:00'.format(today[:10], tomorrow[:10])),
            html.Br(),
            dcc.RadioItems(id='href-dropdown',

                           ),

            # html.Hr(),


        ],
            className='four columns', style={'font-size':'13px'}),

        html.Div([
            html.Div([
                dcc.Graph(
                    id='selected-odds-eu'

                ),
            ], ),
            html.Div([
                dcc.Graph(
                    id='selected-odds-asia',
                ),
            ], ),


        ],className='eight columns')




    ], className='row'),

html.H6(children="Contact & Copyright: 4sea.club@gmail.com",
        style={'textAlign':'center', 'backgroundColor':'#563D7B',
               'color':'#F8F9FA', 'font-size':'16px'}),



])

app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})


@app.callback(
    dash.dependencies.Output('match-type-checklist', 'options'),
    [dash.dependencies.Input('lang-select', 'value')])
def select_lang(selected_lang):
    match = match_nsc_all.loc[match_nsc_all['lang']==selected_lang].reset_index(drop=True)
    mtype = list(match['mtype'].unique())
    return [{'label': mtype[i], 'value': mtype[i]} for i in range(len(mtype))]

@app.callback(
    dash.dependencies.Output('match-type-checklist', 'value'),
    [dash.dependencies.Input('match-type-checklist', 'options')])
def set_match(match_type_options):
    return [match_type_options[i]['value'] for i in range(len(match_type_options))]


@app.callback(
    dash.dependencies.Output('href-dropdown', 'options'),
    [dash.dependencies.Input('match-type-checklist', 'value')]
)
def set_href_options(selected_match_type):
    effect_options = match_nsc_all.loc[(match_nsc_all['mtype'].isin(selected_match_type))].reset_index(drop=True)
    return [{"label": effect_options.loc[i, 'dt_utc08'][11:] + ' '+ effect_options.loc[i, 'mtype'] + ' ' + effect_options.loc[i, 'home'] + '-' + effect_options.loc[i, 'away'],
             "value": effect_options.loc[i, 'href_nsc']} for i in range(len(effect_options))]


@app.callback(
    dash.dependencies.Output('href-dropdown', 'value'),
    [dash.dependencies.Input('href-dropdown', 'options')])
def set_href_value(available_options):
    return available_options[0]['value']


@app.callback(
    dash.dependencies.Output('selected-odds-eu', 'figure'),
    [dash.dependencies.Input('href-dropdown', 'value')])
def set_selected_children(selected_href):
    df = get_odds_eu(selected_href)
    trace0 = go.Scatter(
        x = list(df['dt']),
        y = list(df['home']),
        name = 'home')
    trace1 = go.Scatter(
        x = list(df['dt']),
        y = list(df['away']),
        name = 'away')
    trace2 = go.Scatter(
        x = list(df['dt']),
        y = list(df['draw']),
        name = 'draw')
    data = [trace0, trace1, trace2]
    layout = dict(title='欧赔临场走势 - European Odds Trend',
                  # xaxis=dict(title='timeline'),
                  yaxis=dict(title='odds'))
    fig = dict(data=data, layout=layout)
    return fig

@app.callback(
    dash.dependencies.Output('selected-odds-asia', 'figure'),
    [dash.dependencies.Input('href-dropdown', 'value')])
def set_selected_children(selected_href):
    df = get_odds_asian(selected_href)
    trace0 = go.Scatter(
        x = list(df['dt']),
        y = list(df['home']),
        name = 'home')
    trace1 = go.Scatter(
        x = list(df['dt']),
        y = list(df['away']),
        name = 'away')

    data = [trace0, trace1]
    layout = dict(title='亚盘临场走势 - Asian Handicap Trend',
                  xaxis=dict(title='timeline'),
                  yaxis=dict(title='odds'))
    fig = dict(data=data, layout=layout)
    return fig





if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')