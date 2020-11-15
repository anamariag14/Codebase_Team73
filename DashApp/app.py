import dash


app = dash.Dash(
    __name__, 
    update_title='Loading...',
    suppress_callback_exceptions=True
)

app.title = 'Cargue Bogota'
