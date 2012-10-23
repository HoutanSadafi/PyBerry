from flask import Flask, g, request, redirect, url_for, render_template
from pymongo import Connection
from view_helper import *

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

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
	page_size = parse_query_string(request.args, 'size', int_try_parse, 4)
	page_number = parse_query_string(request.args, 'page', int_try_parse, 1)
	number_to_skip = page_size*(page_number-1)

	posts = g.db.posts.find().sort('id', -1).skip(number_to_skip).limit(page_size)

	if posts.count(with_limit_and_skip=True) == 0:
		return redirect(url_for('about'))
	else:
		pagination = create_pagination(posts.count(), number_to_skip, page_size, page_number)
		return render_template('index.html', posts=posts, pagination=pagination)

@app.route('/about')
def about():
	return render_template('about.html')

if __name__ == '__main__':
	app.run()
