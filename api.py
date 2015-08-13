from flask import Flask, request, Response, jsonify
import configs
# eventually change this to a separate read-only postgres user
pg_connection = psycopg2.connect(**configs.POSTGRES)
pg_connection.autocommit = True
pg_cursor = pg_connection.cursor(cursor_factory=DictCursor)

app = Flask(__name__)


def _error_handler(error, error_code=400):
    response = jsonify({
        'meta': {
            'name': error.__class__.__name__,
            'message': error.message,
            'status': 'error'
        }
    })
    response.status_code = error_code
    return response

app.register_error_handler(Exception, _error_handler)


@app.route('/api', methods=["GET"])
def get_data():
    request.args['tables'] = [
        table for table in\
        request.args.get('tables', request.args.get('table')).split('+')
    ]
    pg_cursor.execute(
        """ SELECT {columns}
        """, {
            'columns':
        }
    )
    return jsonify({})


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=9999, debug=True)
