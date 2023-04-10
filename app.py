from flask import Flask, render_template, request, redirect, session
from datetime import datetime
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create-article', methods=["POST", "GET"])
def create_page():
    if request.method == "POST":
        title = request.form['title']
        text = request.form['article']
        date_time = datetime.utcnow().strftime("%d/%m/%Y %H:%M:%S")
        try:
            db = sqlite3.connect('blog.db')
            sql = db.cursor()
            sql.execute("""CREATE TABLE IF NOT EXISTS articles (      
                                id INTEGER primary key,
                                title TEXT,
                                text TEXT,
                                date_time TEXT
                            )""")
            db.commit()
            sql.execute(
                """INSERT INTO articles (title, text, date_time) VALUES (?, ?, ?)""", (title, text, date_time))
            db.commit()
        except Exception as ex:
            print(ex)

        return redirect('/')
    else:
        return render_template('create.html')

@app.route('/articles')
def articles_page():
    db = sqlite3.connect('blog.db')
    sql = db.cursor()
    sql.execute("""CREATE TABLE IF NOT EXISTS articles (      
                                id INTEGER primary key,
                                title TEXT,
                                text TEXT,
                                date_time TEXT
                            )""")
    db.commit()
    sql.execute("""SELECT * FROM articles ORDER BY id DESC""")
    articles = sql.fetchall()
    db.commit()
    return render_template('posts.html', articles = articles)

@app.route('/articles/<int:id>')
def articles_detailed(id):
    db = sqlite3.connect('blog.db')
    sql = db.cursor()
    sql.execute(f"""SELECT * FROM articles WHERE id = {id}""")
    article = sql.fetchone()
    db.commit()
    return render_template('post_details.html', article=article)

@app.route('/articles/<int:id>/delete')
def article_delete(id):
    db = sqlite3.connect('blog.db')
    sql = db.cursor()
    sql.execute(f"""DELETE FROM articles WHERE id = {id}""")
    db.commit()
    return redirect('/articles')


@app.route('/articles/<int:id>/update', methods=["POST", "GET"])
def update_page(id):
    if request.method == "POST":
        title = request.form['title']
        text = request.form['article']
        date_time = datetime.utcnow().strftime("%d/%m/%Y %H:%M:%S")
        try:
            db = sqlite3.connect('blog.db')
            sql = db.cursor()
            sql.execute(
                """UPDATE articles
                SET title = ?,
                text = ?,
                date_time = ?
                WHERE id = ?""", (title, text, date_time, id)
            )
            db.commit()
        except Exception as ex:
            print(ex)

        return redirect('/articles')
    else:
        db = sqlite3.connect('blog.db')
        sql = db.cursor()
        sql.execute(f"""SELECT * FROM articles WHERE id = {id}""")
        article_update = sql.fetchone()
        db.commit()
        return render_template('post_update.html', article_update=article_update)

if __name__ == '__main__':
    app.run(debug=True)