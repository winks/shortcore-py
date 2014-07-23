import os
import random
import sqlite3
import string
import sys
import time

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.debug = True
app.db_file = './data/urls.sqlite'


def reformat(row):
    return {
        'key': row[0],
        'url': row[1],
        'counter': row[2],
        'created': row[3],
    }


def item_save(url):
    conn = sqlite3.connect(app.db_file)
    cur = conn.cursor()

    # if already in db, don't save again
    sql = 'SELECT * FROM urls WHERE url = ?'
    cur.execute(sql, (url,))
    row = cur.fetchone()
    if row:
        return reformat(row)

    # find a free key
    key = None
    key_free = False
    while not key_free:
        key = id_generator()
        sql = 'SELECT * FROM urls WHERE key = ?'
        cur.execute(sql, (key,))
        row = cur.fetchone()
        if not row or 'key' not in row:
            key_free = True

    created = int(time.time())
    sql = 'INSERT INTO urls VALUES (?,?,?,?)'
    cur.execute(sql, (key, url, 0, created))
    conn.commit()
    conn.close()

    return reformat((key, url, 0, created))


def item_get(key):
    conn = sqlite3.connect(app.db_file)
    cur = conn.cursor()
    sql = 'SELECT * FROM urls WHERE key = ?'
    cur.execute(sql, (key,))
    row = cur.fetchone()
    conn.close()
    if row:
        return reformat(row)

    return None


def item_all():
    conn = sqlite3.connect(app.db_file)
    cur = conn.cursor()
    sql = 'SELECT * FROM urls order by url ASC'
    cur.execute(sql)
    rows = cur.fetchall()
    conn.close()
    urls = {}
    for r in rows:
        urls[r[0]] = reformat(r)

    return urls


def item_inc(key, counter):
    conn = sqlite3.connect(app.db_file)
    cur = conn.cursor()
    sql = 'UPDATE urls set counter = ? WHERE key = ?'
    cur.execute(sql, (int(counter)+1, key))
    conn.close()


def id_generator(size=3, chars=None):
    if not chars:
        chars = string.ascii_uppercase + string.digits + string.ascii_lowercase
    return ''.join(random.choice(chars) for _ in range(size))


@app.route('/')
def index():
    urls = item_all()
    return '<p>Usage: <code>GET</code>: <code>/new?item={URL}</code>' +\
           ' (<code>POST</code> also works)' + '<br></p>' + \
           '<br>'.join('<tt><a href="/{}">{}</a></tt> - {}'.format(
               x,
               x,
               y['url']) for x, y in urls.iteritems())


@app.route('/new', methods=['GET', 'POST'])
def new_item():
    if request.method == 'POST':
        item = request.form['item']
    else:
        item = request.args.get('item')
    if not item:
        return 'no item'
    else:
        x = item_save(item)
        return 'Item saved: ' + item + '<br>' + \
            '<tt><a href="{}">{}</a></tt>'.format(x['key'], x['url']) + '<br>'


@app.route('/<key>')
def show_item(key):
    row = item_get(key)
    if row:
        item_inc(row['key'], row['counter'])
        return redirect(row['url'])
    else:
        return redirect(url_for('index'))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        app.db_file = sys.argv[1]
    print(app.db_file)
    app.run()
