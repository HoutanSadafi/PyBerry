from flask import Flask, g, request, redirect, url_for, render_template
from pymongo import Connection
from view_helper import *
import calendar as cal

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

@app.before_request
def before_request():
	conn = Connection('mongodb://localhost/')
	g.conn = conn
	g.db = conn.blueberry
	get_posts_per_author_aggregate(g)

@app.teardown_request
def teardown_request(exception):
	g.conn.close()


def get_posts_per_author_aggregate(g):
	aggregate = g.db.postsPerMonth.find()
	output = [ { 'year' : int(item['_id']['year']), 'month' : int(item['_id']['month']), 'count' : int(item['value']['count']), 'month_name' : cal.month_name[int(item['_id']['month'])] } for item in aggregate]
	g.posts_per_month = output

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
		return render_template('index.html', posts=posts, pagination=pagination, posts_per_month = g.posts_per_month)

@app.route('/about')
def about():
	return render_template('about.html')

if __name__ == '__main__':
	app.run()
