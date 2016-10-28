# mixmax stock market slash command
Insert graphs for the prices of stocks in the public stock market into emails. 

![final visualization of plugin](https://raw.githubusercontent.com/gabrielfarah/mixmax_stocks_slash_command/master/assets/screen2.jpg)


## Requeriments
* Flask==0.11.1
* Flask-Cors==3.0.2
* yahoo-finance==1.3.2

You can install them running:

```
pip install flask flask-cors yahoo-finance
```

## How to run
1. First start the server using the following line:
```
python server.py
```

2. By default the development server running with Flask will start in localhost at port 8080. Once there you need to go to: 
```
Mixmax Dashboard, click Settings -> Integrations -> Add Slash Command.
```

### On the options:
3. Typeahead API URL add http://localhost:8080/typeahead
4. and for the Resolver API URL add http://localhost:8080/

5. Finally to run your slash command create an email and type:
```
/stocks <STOCK SYMBOL>
```
#### The suggestions looks like this
![final visualization of plugin](https://raw.githubusercontent.com/gabrielfarah/mixmax_stocks_slash_command/master/assets/screen1.jpg)

#### Note: You could use the "," to compare multiple quotes

![final visualization of plugin](https://raw.githubusercontent.com/gabrielfarah/mixmax_stocks_slash_command/master/assets/screen3.jpg)

