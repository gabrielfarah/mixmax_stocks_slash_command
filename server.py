# encoding: utf-8

""" Mixmax Slash Command Integration

Insert graphs for the prices of stocks in the public stock market into emails. 

__author__ = "Gabriel Farah"
__version__ = "0.1"
__maintainer__ = "Gabriel Farah"

"""

from datetime import datetime, timedelta
from flask import Flask, request, render_template, jsonify, render_template_string
from flask.ext.cors import CORS
from yahoo_finance import Share
 
app = Flask(__name__)
CORS(app, supports_credentials=True)


from symbols import stocks
_SYMBOLS = stocks


_RESPONSE_HTML = """
<div>
<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
<script type="text/javascript">
  google.charts.load('current', {'packages':['corechart']});
  google.charts.setOnLoadCallback(drawChart);

  function drawChart() {
    var data = google.visualization.arrayToDataTable(
      %s

    );
    
    var options = {
      title: 'Stock Performance',
      hAxis: {
        title: 'Time'
      },
      vAxis: {
        title: 'Price'
      },
      legend: { position: 'bottom' },
      trendlines: {
      0: {type: 'exponential', color: '#333', opacity: 1},
      1: {type: 'linear', color: '#111', opacity: .3}
    }
    };

    var chart = new google.visualization.LineChart(document.getElementById('chart_div'));

    chart.draw(data, options);
  }
</script>
</div>
<div id="chart_div" style="width: 900px; height: 500px"></div>
"""


def get_stock_data(stocks_param, initial_date, end_date):
	"""
	This function should be called in an async way. 
	Since this is just a prove of concept is fine,
	But this does 1 blocking http request per stock
	We send as a parameter. Pretty bad leaving it syncronous.
	"""
	temp = []
	add_header = False
	response = []
	if "," in stocks_param:
		stocks = stocks_param.split(",")
	else:
		stocks = [stocks_param]
	header = ["Date"]
	for stock in stocks:
		temp_stock = Share(stock)
		temp.append(reversed(temp_stock.get_historical(initial_date, end_date)))
		header.append(str(stock))
	for item in zip(*temp):
		if add_header != True:
			response.append(header)
			add_header = True
		date = item[0]["Date"]
		prices = []
		for resp in item:
			prices.append(float(resp["Adj_Close"]))
		response.append([date] + prices)
	return response

@app.route("/typehead", methods=['GET', 'OPTIONS'])
def typehead():
	"""
	This function will return the partials stock symbols for a given request
	"""
	partial_stock = request.args.get('text')
	if partial_stock is None:
		return jsonify(Error="No stock was send as input")
	resp = [{"title":s,"text":s} for s in _SYMBOLS if partial_stock.upper() in s]
	return jsonify(resp)


@app.route("/", methods=['GET', 'OPTIONS'])
def index():
	"""
	This is the only endpoint of our webapp.
	It must receive inputs as the follow to work:
		http://127.0.0.1:8080/?text=YHOO,GOOG&initial_date=2013-01-01&end_date=2016-01-01&format=json
	Where stocks is a comma separated stock symbol,
	Initial_date and end_date are dates of the form YYYY-MM-DD
	From which we will retrieve the information from. 
	Finally the format variable indicates if we should return a webpage html or a json
	"""
	stocks = request.args.get('text')
	initial_date = request.args.get('initial_date')
	end_date = request.args.get('end_date')
	render_format = request.args.get('format')
	if initial_date is None or end_date is None:
		end_date = datetime.today().strftime('%Y-%m-%d')
		one_year_ago = datetime.today() - timedelta(days=365)
		initial_date = one_year_ago.strftime('%Y-%m-%d')
	if stocks is None:
		return jsonify(Error="No stock was send as input")
	# TODO Validate user inputs
	data = get_stock_data(stocks,initial_date,end_date)
	# TODO make the get_stock_data asynchonous
	if render_format is "html":
		return render_template('response.html', data=data)
	else:
		rendered = _RESPONSE_HTML % data
		return jsonify({'body':rendered})

if __name__ == "__main__":
	app.run(port = 8080, debug = True)