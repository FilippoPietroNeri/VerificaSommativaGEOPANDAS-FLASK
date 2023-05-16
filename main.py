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

#ESERCIZIO 1#
sostaGeometry = [Point(xy) for xy in zip(sosta_turistici['LONG_X_4326'], sosta_turistici['LAT_Y_4326'])]
sostagdf = gpd.GeoDataFrame(sosta_turistici, crs="EPSG:4326", geometry=sostaGeometry)
#############

milano3857 = milano.to_crs(3857)
sosta3857 = sostagdf.to_crs(3857)

@app.route('/')
def homepage():
    return render_template('index.html')


@app.route('/res/<id>/')
def handler_exercise(id):
    match int(id):
        case 1:
            ### ESERCIZIO 2 ###

            fig, ax = plt.subplots(figsize=(10, 10))
            sosta3857.plot(ax=ax, color='red')
            milano3857.plot(ax=ax, facecolor='none', edgecolor='none')
            ctx.add_basemap(ax=ax)

            # INITIALIZE DECODER
            buf1 = BytesIO()
            fig.savefig(buf1, format="png")
            data1 = base64.b64encode(buf1.getbuffer()).decode("ascii")
            return render_template('result.html', image=f'data:image/png;base64,{data1}')
        case 2:
            ### ESERCIZIO 3 ###

            fig, ax = plt.subplots(figsize=(10, 10))
            sosta3857.plot(ax=ax, color='red')
            milano3857.plot(ax=ax, facecolor='none')
            ctx.add_basemap(ax=ax)

            # INITIALIZE DECODER
            buf1 = BytesIO()
            fig.savefig(buf1, format="png")
            data1 = base64.b64encode(buf1.getbuffer()).decode("ascii")
            return render_template('result.html', image=f'data:image/png;base64,{data1}')
        case 3:
            ### ESERCIZIO 4 ###

            localizzazione = request.args.get('location')
            result = sostagdf[sostagdf['localizzaz'] == localizzazione]
            if len(result) > 0:
                quartiere = milano[milano.contains(result.geometry.squeeze())]
                if not quartiere.empty:
                    fig, ax = plt.subplots(figsize=(10, 10))
                    quartiere.to_crs(3857).plot(ax=ax, facecolor='none')
                    result.to_crs(3857).plot(ax=ax, color='red')
                    ctx.add_basemap(ax=ax)

                    # INITIALIZE DECODER
                    buf1 = BytesIO()
                    fig.savefig(buf1, format="png")
                    data1 = base64.b64encode(buf1.getbuffer()).decode("ascii")

                    return render_template('result.html', quart=quartiere['NIL'], image=f'data:image/png;base64,{data1}')
                else:
                    print('Il parcheggio in questo quartiere non esiste!')
            else:
                print('Non esiste nessun parcheggio con questa localizzazione!')
            
        case 4:
            ### ESERCIZIO 5 ###
            longitudine = float(request.args.get('long'))
            latitudine = float(request.args.get('lat'))
            distanza = float(request.args.get('dist'))

            userPoint = gpd.GeoSeries(Point(longitudine,latitudine))
            sosteVicine = sostagdf[sostagdf.distance(userPoint.squeeze()) <= distanza]  
            return render_template('dfresult.html', dataframe=sosteVicine.to_html())
        case 5:
            ### ESERCIZIO 6 ###
            senzasoste = milano[~milano.intersects(sostagdf.unary_union)]
            fig, ax = plt.subplots(figsize=(10, 10))
            milano3857.plot(ax=ax,facecolor='none', edgecolor='none')
            senzasoste.to_crs(3857).plot(ax=ax,facecolor='none', edgecolor='gray', linewidth=2)
            ctx.add_basemap(ax=ax)

            # INITIALIZE DECODER
            buf1 = BytesIO()
            fig.savefig(buf1, format="png")
            data1 = base64.b64encode(buf1.getbuffer()).decode("ascii")
            return render_template('result.html', image=f'data:image/png;base64,{data1}')
        case 6:
            ### ESERCIZIO 7 ###

            return render_template('index.html')
        case _:
            return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3245, debug=True)
