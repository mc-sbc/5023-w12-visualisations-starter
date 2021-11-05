import json

from flask import render_template
from flask_login import login_required
import pandas as pd
import plotly.express as px
import plotly

from sqlalchemy import func

from app import db
from app.chart import bp
from app.models import Book, Genre

@bp.route('/')
@login_required
def chart_list():
    return render_template('chart_list.html', title = 'List of Charts')

@bp.route('/book_ratings')
@login_required
def book_ratings_chart():
    # Retrieve all the books in the collection
    book_query = Book.query
    df = pd.read_sql(book_query.statement, book_query.session.bind)

    # Draw the chart and dump it into JSON format
    chart = px.bar(df, x='title', y='critics_rating')
    chart_JSON = json.dumps(chart, cls=plotly.utils.PlotlyJSONEncoder, indent=4)

    # Returns the template, including the JSON data for the chart
    return render_template('chart_page.html', title = 'Critic ratings for books', chart_JSON = chart_JSON)
    
@bp.route('/user_books')
@login_required
def user_books_chart():
    # Run query to get count of books owned per user and load into DataFrame
    query = (
        "SELECT username, count(*) as books_owned "
        "FROM user_book ub "
        "JOIN user u on ub.user_id = u.id "
        "GROUP BY username"
    )
    df = pd.read_sql(query, db.session.bind)

    # Draw the chart and dump it into JSON format
    chart = px.bar(df, x ='username', y='books_owned')
    chart_JSON = json.dumps(chart, cls=plotly.utils.PlotlyJSONEncoder, indent=4)

    # Returns the template, including the JSON data for the chart
    return render_template('chart_page.html', title = 'Books owned per user', chart_JSON = chart_JSON)

@bp.route('/books_read')
@login_required
def books_read_chart():
    # Run query to get books read per year by user and load into DataFrame
    query = (
        "SELECT username, books_read_per_year "
        "FROM user u "
    )
    df = pd.read_sql(query, db.session.bind)

    # Draw the chart and dump it into JSON format
    chart = px.bar(
        df, x ='username', y='books_read_per_year', title='Books read per year by user',
        labels = {'username': 'Username','books_read_per_year': 'Books read per year'},
        template = 'plotly_white'
    )
    chart_JSON = json.dumps(chart, cls=plotly.utils.PlotlyJSONEncoder, indent=4)

    # Returns the template, including the JSON data for the chart
    return render_template('chart_page.html', title = 'Books read per year', chart_JSON = chart_JSON)

@bp.route('/books_per_genre_SQL_statement')
@login_required
def books_per_genre_SQL_statement_chart():
    # Run query to get count of books per genre
    query = (
        "SELECT name, count(*) as number_of_books "
        "FROM book b "
        "JOIN genre g on b.genre_id = g.id "
        "GROUP BY name "
    )
    df = pd.read_sql(query, db.session.bind)

    # Draw the chart and dump it into JSON format
    chart = px.bar(
        df, x ='name', y='number_of_books', title='Number of books per genre',
        labels = {'name': 'Genre','number_of_books': 'Number of books'},
        template = 'plotly_white'
    )
    chart_JSON = json.dumps(chart, cls=plotly.utils.PlotlyJSONEncoder, indent=4)

    # Returns the template, including the JSON data for the chart
    return render_template('chart_page.html', title = 'Books per genre', chart_JSON = chart_JSON)

@bp.route('/books_per_genre_SQLAlchemy')
@login_required
def books_per_genre_SQLAlchemy_chart():
    # Run SQLAlchemy query to get count of books per genre
    query = db.session.query(
        Genre.name, 
        func.count(Genre.name)
        ).join(Book).group_by(Genre.name)
 
    df = pd.read_sql(query.statement, query.session.bind)

    # Draw the chart and dump it into JSON format
    chart = px.bar(df, x ='name', y='count_1',
        labels = {'name': 'Genre','count_1': 'Number of books'},
        title='Number of books per genre',
        template='plotly_white')
    
    chart_JSON = json.dumps(chart, cls=plotly.utils.PlotlyJSONEncoder, indent=4)

    # Returns the template, including the JSON data for the chart
    return render_template('chart_page.html', title = 'Books per genre', chart_JSON = chart_JSON)