import json

from app import app, sql_general_dao
from flask import render_template, request


@app.route('/')
def index():

    return render_template('index.html')


@app.route('/login/', methods=['get','post'])
def login():
    # message = ''
    username: str = None
    password: str = None

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

    if username and password:
        return f"Sucessfull login <u>{username}</u> and your password is <u>{password}</u>"
    else:
        return render_template('login_page.html')


@app.route('/get-database-content/')
def get_database_content():
    return render_template('get_database_content.html', all_table_names=sql_general_dao.get_all_table_names())


@app.route('/table-content/<table_name>/')
def table_content(table_name):
    column_names = sql_general_dao.get_table_column_name(table_name)
    table_content = sql_general_dao.get_table_content(table_name)
    table_content = [item.values() for item in table_content]

    return render_template("table_content.html", table_content=table_content, column_names=column_names)


@app.route('/general-conversion/')
def display_general_conversion():
    all_questionnaire_general_info = sql_general_dao.get_all_questionnaire_general_info()
    for i in range(len(all_questionnaire_general_info)):

        all_questionnaire_general_info[i]['poll_creation_time'] = all_questionnaire_general_info[i]['poll_creation_time'].isoformat()
    # all_questionnaire_general_info = json.dumps(all_questionnaire_general_info)
    # print(all_questionnaire_general_info)
    return render_template('conversion/general_conversion.html', data=all_questionnaire_general_info)


@app.route('/general-conversion/conversion/<string:table_name>')
def concrete_conversion(table_name: str):
    from app.conversion import make_conversion_page_content

    table_content = make_conversion_page_content(table_name)
    # print(table_content)
    # print(table_name)
    column_names = table_content[-1].keys()

    return render_template('conversion/conversion.html', column_names=column_names, table_content=table_content)


@app.route('/bot-statistics/')
def bot_statistics():
    return None


@app.route('/speed-print-text/')
def speed_print_text():
    data = None
    with open("text_to_print.txt") as f:
        data = f.read()

    return render_template('speed-print/speed-print-text.html', data=data)
