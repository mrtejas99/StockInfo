from datetime import date, datetime
from dateutil.relativedelta import  relativedelta
import requests
from flask import Flask, render_template
import requests_cache

app = Flask(__name__)
requests_cache.install_cache('listing_cache', backend='sqlite', expire_after=180)

@app.route('/favicon.png')  
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.png', mimetype='image/vnd.microsoft.icon')

@app.route("/")    
def index():
    return render_template("loading.html")


@app.route("/concalls")
def concalls():
    current = date.today()
    previous = current + relativedelta(months=-4) #go 4 months back

    print("previous date is {} and current date is {}".format(previous, current)) 

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}

    url = "https://api.bseindia.com/BseIndiaAPI/api/AnnGetData/w?strCat=Company+Update&strPrevDate={0}&strScrip=&strSearch=P&strToDate={1}&strType=C".format(previous.strftime("%Y%m%d"), current.strftime("%Y%m%d"))
    data=requests.get(url, headers=headers)
    print("Current Time: {0} / Used Cache: {1}".format(datetime.now().strftime("%H:%M:%S"), data.from_cache))
    res=data.json()
    return render_template("concalls.html", records=res['Table'])

if __name__ == '__main__':
    app.run(debug = True)
