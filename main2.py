import base64
from io import BytesIO
import pandas as pd
import geopandas as gpd
import contextily as ctx
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon
from flask import Flask, render_template, request, redirect
app = Flask(__name__)

milano = gpd.read_file('https://github.com/FilippoPietroNeri/datigpd/raw/main/ds964_nil_wm.zip')
sosta_turistici = pd.read_csv('https://raw.githubusercontent.com/FilippoPietroNeri/datigpd/main/sosta_turistici.csv', sep=';')
sostaGeometry = [Point(xy) for xy in zip(sosta_turistici['LONG_X_4326'], sosta_turistici['LAT_Y_4326'])]
sostagdf = gpd.GeoDataFrame(sosta_turistici, crs="EPSG:4326", geometry=sostaGeometry)
milano3857 = milano.to_crs(3857)
sosta3857 = sostagdf.to_crs(3857)


@app.route('/')
def homepage():
    quartieri_con_parcheggi = gpd.sjoin(milano, sostagdf, op='intersects')
    lista_quartieri_con_parcheggi = quartieri_con_parcheggi['NIL'].unique()
    print(lista_quartieri_con_parcheggi)
    return render_template('indextest.html', quartierilist = lista_quartieri_con_parcheggi)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3245, debug=True)