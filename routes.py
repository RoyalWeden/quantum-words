from run import app
from flask import request, jsonify
import psycopg2
import random
import os

conn = psycopg2.connect(os.getenv('POSTGRES_URL'))

@app.route('/api/v1/')
def home():
    return 'API v1 Home'

@app.route('/api/v1/word/create', methods=['GET'])
def create_word():
    vars = dict(request.args)

    # requires api key
    api_key = vars.get('api_key')
    if not api_key:
        return jsonify({
            'status': 'error',
            'data': {},
            'message': 'Request requires api key'
        })

    if api_key != os.getenv('API_KEY'):
        return jsonify({
            'status': 'error',
            'data': {},
            'message': 'Invalid api key'
        })
    if 'api_key' in vars:
        vars.pop('api_key')

    for k in vars.keys():
        if k not in ['word', 'definition'] or len(vars) != 2:
            return jsonify({
                'status': 'error',
                'data': {},
                'message': 'Request requires word and definition'
            })

    word = vars['word']
    definition = vars['definition']
    with conn:
        with conn.cursor() as curs:
            curs.execute('CREATE TABLE IF NOT EXISTS words (id serial primary key, word varchar(255) NOT NULL, definition text NOT NULL);')
            curs.execute(f'INSERT INTO words (word, definition) VALUES (\'{word}\', \'{definition}\');')
    return jsonify({
        'status': 'success',
        'data': {},
        'message': 'Successful definition creation'
    })

@app.route('/api/v1/word/get', methods=['GET'])
def get_word():
    vars = dict(request.args)
    if 'api_key' in vars:
        vars.pop('api_key')

    for k in vars.keys():
        if k not in ['word', 'id'] or len(vars) != 1:
            return jsonify({
                'status': 'error',
                'data': {},
                'message': 'Request requires word or id'
            })

    word = vars.get('word')
    id = vars.get('id')
    with conn:
        with conn.cursor() as curs:
            if word:
                curs.execute(f'SELECT * FROM words WHERE word=\'{word}\';')
            elif id:
                curs.execute(f'SELECT * FROM words WHERE id=\'{id}\';')
            fetch = curs.fetchone()
            if fetch:
                return jsonify({
                    'status': 'success',
                    'data': {
                        'id': fetch[0],
                        'word': fetch[1],
                        'definition': fetch[2]
                    },
                    'message': ''
                })
            else:
                return jsonify({
                    'status': 'error',
                    'data': {},
                    'message': 'Could not find word or id'
                })

@app.route('/api/v1/word/remove', methods=['GET'])
def remove_word():
    vars = dict(request.args)

    # requires api key
    api_key = vars.get('api_key')
    if not api_key:
        return jsonify({
            'status': 'error',
            'data': {},
            'message': 'Request requires api key'
        })

    if api_key != os.getenv('API_KEY'):
        return jsonify({
            'status': 'error',
            'data': {},
            'message': 'Invalid api key'
        })
    if 'api_key' in vars:
        vars.pop('api_key')

    for k in vars.keys():
        if k not in ['word', 'id'] or len(vars) != 1:
            return jsonify({
                'status': 'error',
                'data': {},
                'message': 'Request requires only word or id'
            })

    word = vars.get('word')
    id = vars.get('id')
    with conn:
        with conn.cursor() as curs:
            if word:
                curs.execute(f'DELETE FROM words WHERE word=\'{word}\';')
            elif id:
                curs.execute(f'DELETE FROM words WHERE id=\'{id}\';')
    return jsonify({
        'status': 'success',
        'data': {},
        'message': 'Successful word deletion'
    })

@app.route('/api/v1/word/all', methods=['GET'])
def get_all_words():
    vars = dict(request.args)
    if 'api_key' in vars:
        vars.pop('api_key')

    with conn:
        with conn.cursor() as curs:
            curs.execute('SELECT * FROM words')
            fetch = curs.fetchall()
            fetch_dict = []
            for f in fetch:
                fetch_dict.append({
                    'id': f[0],
                    'word': f[1],
                    'definition': f[2]
                })
            return jsonify({
                'status': 'success',
                'data': fetch_dict,
                'message': ''
            })

@app.route('/api/v1/word/random', methods=['GET'])
def get_random_word():
    vars = dict(request.args)
    if 'api_key' in vars:
        vars.pop('api_key')

    with conn:
        with conn.cursor() as curs:
            curs.execute('SELECT * FROM words')
            fetch = curs.fetchall()
            fetch_dict = []
            for f in fetch:
                fetch_dict.append({
                    'id': f[0],
                    'word': f[1],
                    'definition': f[2]
                })
            return jsonify({
                'status': 'success',
                'data': random.choice(fetch_dict),
                'message': ''
            })

@app.route('/api/v1/word/droptable', methods=['GET'])
def drop_word_table():
    vars = dict(request.args)

    # requires api key
    api_key = vars.get('api_key')
    if not api_key:
        return jsonify({
            'status': 'error',
            'data': {},
            'message': 'Request requires api key'
        })

    if api_key != os.getenv('API_KEY'):
        return jsonify({
            'status': 'error',
            'data': {},
            'message': 'Invalid api key'
        })
    if 'api_key' in vars:
        vars.pop('api_key')

    with conn:
        with conn.cursor() as curs:
            curs.execute('DROP TABLE IF EXISTS words;')
            return jsonify({
                'status': 'success',
                'data': {},
                'message': 'Successful table deletion'
            })