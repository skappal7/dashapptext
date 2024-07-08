import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from textblob import TextBlob
import nltk
from nltk.corpus import stopwords
import string
import io
import base64

nltk.download('stopwords')

# Initialize the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout
app.layout = dbc.Container([
    dbc.Row(dbc.Col(html.H1("Text and Sentiment Analytics App", className="text-center mt-4"))),
    dbc.Row(dbc.Col(dcc.Upload(
        id='upload-data',
        children=html.Div(['Drag and Drop or ', html.A('Select Files')]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=False
    ))),
    dbc.Row(dbc.Col(dbc.Button("Analyze", id="analyze-button", className="btn btn-primary mt-3"))),
    dbc.Row(dbc.Col(html.Div(id='output-data-upload'))),
    dbc.Row(dbc.Col(dcc.Graph(id='sentiment-graph'))),
], fluid=True)

# Callbacks
@app.callback(
    [Output('output-data-upload', 'children'),
     Output('sentiment-graph', 'figure')],
    [Input('analyze-button', 'n_clicks')],
    [State('upload-data', 'contents'),
     State('upload-data', 'filename')]
)
def update_output(n_clicks, contents, filename):
    if contents is None:
        return "No file uploaded yet.", {}

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'txt' in filename:
            # Assume that the user uploaded a TXT file
            df = pd.DataFrame([decoded.decode('utf-8')], columns=['text'])
        else:
            return "Unsupported file type.", {}
    except Exception as e:
        return f"Error processing file: {str(e)}", {}

    # Text Preprocessing
    def preprocess_text(text):
        stop_words = set(stopwords.words('english'))
        text = text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation))
        text = ' '.join([word for word in text.split() if word not in stop_words])
        return text

    df['cleaned_text'] = df['text'].apply(preprocess_text)

    # Sentiment Analysis
    df['sentiment'] = df['cleaned_text'].apply(lambda x: TextBlob(x).sentiment.polarity)
    df['sentiment_label'] = df['sentiment'].apply(lambda x: 'Positive' if x > 0 else ('Negative' if x < 0 else 'Neutral'))

    # Display text and sentiment
    uploaded_data = html.Div([
        html.H5(filename),
        html.H6(f"Total records: {len(df)}"),
        dbc.Table.from_dataframe(df[['text', 'sentiment', 'sentiment_label']], striped=True, bordered=True, hover=True)
    ])

    # Create sentiment distribution graph
    fig = px.histogram(df, x='sentiment_label', title='Sentiment Distribution', color='sentiment_label')

    return uploaded_data, fig

server = app.server

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080, debug=True)
