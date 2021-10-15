import sys
from datetime import date, datetime
from dateutil.relativedelta import  relativedelta
import requests
from flask import Flask, render_template
import requests_cache

#initialise the app
app = Flask(__name__)
requests_cache.install_cache('listing_cache', backend='sqlite', expire_after=14400) #backend for caching is SQLite

@app.route('/favicon.png')  #favicon page
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.png', mimetype='image/vnd.microsoft.icon')

@app.route("/")    #loading page
def index():
    return render_template("loading.html")


@app.route("/concalls") #main route
def concalls():
    current = date.today()
    previous = current + relativedelta(months=-1) #go 1 months back

    print("previous date is {} and current date is {}".format(previous, current)) 

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}

    url = "https://api.bseindia.com/BseIndiaAPI/api/AnnGetData/w?strCat=Company+Update&strPrevDate={0}&strScrip=&strSearch=P&strToDate={1}&strType=C".format(previous.strftime("%Y%m%d"), current.strftime("%Y%m%d"))
    data=requests.get(url, headers=headers)
    print("retrived {} MB".format(sys.getsizeof(data) / 1048576))   #get size in MB
    print("Current Time: {0} / Used Cache: {1}".format(datetime.now().strftime("%H:%M:%S"), data.from_cache))
    res=data.json()
    return render_template("concalls.html", records=res['Table'])

