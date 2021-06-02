from datetime import date
from dateutil.relativedelta import  relativedelta
import requests
from flask import Flask, render_template
app = Flask(__name__)
from time import sleep    
    
@app.route('/favicon.png')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.png', mimetype='image/vnd.microsoft.icon')
      

@app.route("/")
def index():
    return render_template("loading.html")

@app.route("/concalls")
def concalls():
    current = date.today()
    previous = current + relativedelta(months=-1) #go 4 months back

    print("previous date is {} and current date is {}".format(previous, current)) 

    #Create session and add UA for visiting the site
    session = requests.Session()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}

    url = "https://api.bseindia.com/BseIndiaAPI/api/AnnGetData/w?strCat=Company+Update&strPrevDate={0}&strScrip=&strSearch=P&strToDate={1}&strType=C".format(previous.strftime("%Y%m%d"), current.strftime("%Y%m%d"))
    #sleep(10)
    res=session.get(url, headers=headers).json()
    return render_template("concalls.html", records=res['Table'])

if __name__ == '__main__':
	app.run(host = '0.0.0.0', debug=True)