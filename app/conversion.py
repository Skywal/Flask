import copy
import datetime
import json
from app import sql_general_dao
from dateutil import parser


def make_conversion_page_content(table_name: str):

    json_table_content = sql_general_dao.get_table_content(table_name)

    for i in range(len(json_table_content)):
        json_table_content[i]['answer'] = json_table_content[i]['answer'].split("_;")
        if json_table_content[i]['answer_time']:
            json_table_content[i]['answer_time'] = json.loads(json_table_content[i]['answer_time'])

    # print(json_table_content)

    # get login name from 'user' table
    user_id = [item['id_user'] for item in json_table_content]
    user_logins = [item['login_telegram'] for item in sql_general_dao.find_user_names_by_id(user_id)]
    user_names = [item['name_telegram'] for item in sql_general_dao.find_user_names_by_id(user_id)]
    user_last_names = [item['last_name_telegram'] for item in sql_general_dao.find_user_names_by_id(user_id)]


    for i in range(len(json_table_content)):
        json_table_content[i].update({
            'telegram login': f'{"@"}{user_logins[i]}',
            'telegram name and last name': f'{user_names[i]} {user_last_names[i]}'
        })
    # end get login name

    answer_time = [item['answer_time'] for item in json_table_content]

    # підготовка для вирахунку дельти часу
    for i in range(len(answer_time)):
        if answer_time[i]:
            answer_time[i].insert(0, json_table_content[i]['start_time'])
            answer_time[i].append(json_table_content[i]['pass_date'])

    answer_delta = count_answer_delta(answer_time)
    # print(answer_delta)

    final_json_data = []
    for index, item in enumerate(json_table_content):
        record={}
        record['id'] = item['id']
        record['id author'] = item['id_author']
        record['id user'] = item['id_user']
        record['telegram login'] = item['telegram login']
        record['telegram name and last name'] = item['telegram name and last name']
        for i in range(len(item['answer'])):
            record['{} {}'.format('answer', i)] = item['answer'][i]

        if item['answer_time']:
            for i in range(len(answer_delta[index])):
                # print(i, index)
                # print(len(answer_delta[index]))
                "{}:{}"
                if not answer_delta[index][i]:
                    record['{} {}'.format('answer time', i)] = answer_delta[index][i]
                elif answer_delta[index][i]:
                    # to_out = "{}:{}".format(answer_delta[index][i][0], answer_delta[index][i][1] if answer_delta[index][i][1]>9 else "0{}".format(answer_delta[index][i][1]))
                    to_out = "{0:0>2}:{1:0>2}".format(answer_delta[index][i][0], answer_delta[index][i][1])
                    record['{} {}'.format('answer time', i)] = to_out
                else:
                    record['{} {}'.format('answer time', i)] = "####"
        else:
            tem = [None]*len(item['answer'])
            for i in range(len(tem)):
                record['{} {}'.format('answer time', i)] = tem[i]

        record['start time'] = item['start_time']
        record['end time'] = item['end_time']
        record['pass date'] = item['pass_date']

        final_json_data.append(record)

    return final_json_data


def count_answer_delta(answer_time):

    time_list = copy.deepcopy(answer_time)
    # конвертація дати з формату ISO в формат datetime з ігноруванням None всередині списку часу на відповідь для
    # кожного користувача (означає що тест редагували і не точно буде якщо буде рахуватися з цим тому його виключаємо
    # а потім додамо назад)
    for i in range(len(time_list)):
        if time_list[i]:
            normal_datetime = []
            for item in time_list[i]:
                if item and type(item) != datetime.datetime:
                    normal_datetime.append(parser.parse(item))
                elif not item:
                    # normal_datetime.append(0) # for this time just ignore new questions
                    pass
                else:
                    normal_datetime.append(item)
            time_list[i] = copy.deepcopy(normal_datetime)
        else:
            time_list[i] = None

    # Вираховуємо різницю в часі між відповідями
    seconds_in_day = 24*60*60
    time_delta = []
    for item in time_list:
        if type(item) == list:
            time_delta.append([])
            for i in range(len(item) - 1):
                diff = item[i+1] - item[i]
                delta = divmod(diff.days * seconds_in_day + diff.seconds, 60)
                time_delta[-1].append([delta[0], delta[1], diff.microseconds/1e6])
        else:
            time_delta.append(None)

    # дізнаємося де були None в списках часів між відповідями
    old_nones = []
    for i in range(len(answer_time)):
        old_nones.append([])
        if type(answer_time[i]) == list:
            for j in range(len(answer_time[i])):
                if not answer_time[i][j]:
                    old_nones[-1].append(j)

    for i in range(len(time_delta)):
        for item in old_nones[i]:
            if type(time_delta[i]) == list:
                time_delta[i].insert(item, None)

    return time_delta


if __name__ == "__main__":
    make_conversion_page_content("1624818960_395372589_statistic")
