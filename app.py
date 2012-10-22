from flask import Flask, g, render_template
from pymongo import Connection

app = Flask(__name__)
app.config.from_object('config.ProductionConfig')

@app.before_request
def before_request():
	conn = Connection('mongodb://localhost/')
	g.conn = conn
	g.db = conn.blueberry


@app.teardown_request
def teardown_request(exception):
	g.conn.close()

@app.route('/')
def index():
	posts = g.db.posts.find()
	return render_template('Index.html', posts=posts)

@app.route('/post')
def post():
	return app.config['DATA_SOURCE']

if __name__ == '__main__':
	app.run(debug=True)
