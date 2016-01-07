from flask import Flask, request, Response, jsonify
import configs
import psycopg2
from psycopg2.extras import DictCursor
from functools import reduce
from pprint import pprint

# eventually change this to a separate read-only postgres user
pg_connection = psycopg2.connect(**configs.POSTGRES)
pg_connection.autocommit = True
pg_cursor = pg_connection.cursor(cursor_factory=DictCursor)

app = Flask(__name__)


def _error_handler(error, error_code=400):
    response = jsonify({
        'meta': {
            'name': error.__class__.__name__,
            'message': str(error),
            'status': 'error'
        }
    })
    response.status_code = error_code
    return response

# app.register_error_handler(Exception, _error_handler)


# example: http://mysite.com/api?tables=table1+table_2+table_3&min_date=1900Q1&max_date=2000Q4
@app.route('/api', methods=["GET"])
def get_data():

    tables_arg = request.args.get('tables', request.args.get('table'))
    if tables_arg is None:
        return jsonify({'Error': 'You must specify metric tables.'})
    print(tables_arg)
    tables = [table for table in tables_arg.split(' ')]

    tables_sql = '{} base'.format(tables[0])
    for additional_table in tables[1:]:
        tables_sql += '\nLEFT JOIN {table} ON base."DATE" = {table}."DATE"'.format(table=additional_table)
    print(tables_sql)
    # eventually i'll need to check this against a list of table names to prevent sql injection
    pg_cursor.execute(
        """ SELECT *
            FROM {}
            ORDER BY base."DATE" ASC;
        """.format(tables_sql)
    )
    data_return = pg_cursor.fetchall()

    pprint([dict(row) for row in data_return])
    return 'OK'

    # pg_cursor.execute(
    #     """ SELECT {columns}
    #         FROM {tables}
    #         {min_date_clause}
    #         {max_date_clause}
    #         ORDER BY a.DATE ASC;
    #     """, {
    #         'columns': ,
    #         'tables': '{} base'.format(request.args['tables'][0]) +\
    #             reduce(
    #                 lambda table_list, table: table_list + table,
    #                 [
    #                     '\nLEFT JOIN {table} ON base.DATE = {table}.DATE'.format(table=table)\
    #                     for table in request.args['tables'][1:]
    #                 ]
    #             ),
    #         'min_date_clause': 'WHERE a.DATE => {min_date_clause}'.format(
    #             request.args['min_date'] if request.args.get('min_date') else ''
    #         ),
    #         'max_date_clause': (
    #             'AND ' if request.args.get('min_date') else 'WHERE '\
    #             + 'a.DATE <= {max_date}'.format(
    #                 request.args['max_date']
    #             )
    #         ) if request.args.get('max_date') else ''
    #     }
    # )
    # return jsonify({})


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=9999, debug=True)
