from flask import Flask, render_template
from flask_bootstrap import Bootstrap5

app = Flask(__name__)
bootstrap = Bootstrap5(app)


my_info = {
   'flavors': ['sweet','sour'],'colors': ['blue','green','brown']
}


@app.route('/')
def home():
    return render_template('index.html', my_info=my_info)
