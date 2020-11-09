from sklearn import preprocessing
import requests
import pandas as pd

url1 = "https://www.xdeamx.com/reto3/process.php"
url2 = "https://www.xdeamx.com/reto3/general.php"


def _http_rq_post(url):
    headers = {'accept': 'text/html'}
    s = requests.Session()
    data = {'numero': '4004'}
    response = s.post(url=url, headers=headers, data=data)
    return s, response


def _http_rq_get(url, session):
    headers = {'accept': 'text/html'}
    response = session.get(url=url, headers=headers)
    return response


def _save_html(response, name=""):
    f = open(name+"htmldata.html", "w")
    f.write(response.text)
    f.close()


def dowload():

    s, r1 = _http_rq_post(url1)
    r2 = _http_rq_get(url2, s)

    _save_html(r2, "general")

    file_name = 'generalhtmldata.html'
    df = pd.read_html(file_name)

    df_runners = df[0]
    df_runners['duration-minutes'] = pd.to_numeric(df_runners['Tiempo Total (Minutos)'][:206])
    df_runners['laps'] = pd.to_numeric(df_runners['No de vueltas'][:206])
    df_runners['elevation'] = pd.to_numeric(df_runners['Elevación total'][:206])
    df_runners['distance'] = pd.to_numeric(df_runners['Dis. Total'][:206])
    df_runners['category'] = df_runners['distance']/df_runners['laps']
    del df_runners['Género']

    df_metrics = df_runners[['duration-minutes', 'laps', 'elevation', 'distance']]
    x = df_metrics
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    df_metrics_n = pd.DataFrame(x_scaled)
    df_metrics_n.columns = ['duration-minutes', 'laps', 'elevation', 'distance']
    df_metrics_n.index = df_runners['category']

    return df_runners, df_metrics_n
