# ����������� ����������
from flask import Flask, request
import logging

# ����������, ������� ��� ����������� ��� ������ � JSON
import json

# ������ ����������
# �� ������� __name__, � ��� ���������� ����������, 
# � ����� ������ �� ���������.
# � ������ ������ ��� ���������� '__main__', 
# ��� ��� �� ���������� � ���������� �� ����������� ������.
# ���� �� ����� ���������, ��������, 
# ��������� ������ ������ logging, �� �� �� �������� 'logging'
app = Flask(__name__)

# ������������� ������� �����������
logging.basicConfig(level=logging.INFO)

# �������� �������, ����� ��� ������ ������ ������� 
# � ������� ��������� ���������, ������� ����� ������������.
# ��� ������� ��� ������� ������������� ��������� ������� 
# (buttons � JSON ������).
# ����� ����� ������������ ������� ������ ������, 
# �� �� �������� � ���� ������� ������ �������
# sessionStorage[user_id] = {'suggests': ["�� ����.", "�� ����.", "�������!" ]}
# ����� ������ �������, ��� �� �������� ������������ ��� ��� ���������. 
# ����� �� ��������� ������ �����,
# �� �� ������ ���� ���������. ��� ����� ���-�� �������� :)
sessionStorage = {}


@app.route('/post', methods=['POST'])
# ������� �������� ���� ������� � ���������� �����.
# ������ ������� �������� request.json - ��� JSON, 
# ������� ��������� ��� ����� � ������� POST
def main():
    logging.info(f'Request: {request.json!r}')

    # �������� ����������� �����, �������� ������������
    # �� �������� �������, ������� ����� ��� ������ 
    # ���������� json ����������� � JSON � ������� �����
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    # ���������� request.json � response � ������� handle_dialog. 
    # ��� ���������� ���������� ���� JSON, ������� ��������
    # ��������������� �� ������� �������
    handle_dialog(request.json, response)

    logging.info(f'Response:  {response!r}')

    # ��������������� � JSON � ����������
    return json.dumps(response)


def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        # ��� ����� ������������.
        # �������������� ������ � �������������� ���.
        # ������� ���������, ������� �� ��� ������� � ������ ���

        sessionStorage[user_id] = {
            'suggests': [
                "�� ����.",
                "�� ����.",
                "�������!",
            ]
        }
        # ��������� ����� ������
        res['response']['text'] = '������! ���� �����!'
        # ������� ���������
        res['response']['buttons'] = get_suggests(user_id)
        return

    # ���� ������ ������, ���� ������������ �� �����, 
    # � �������� � ������ ��� ��� �����
    # ������������ ����� ������������.
    # � req['request']['original_utterance'] ����� ���� �����,
    # ��� ��� ������� ������������
    # ���� �� ������� '�����', '�����', '�������', '������', 
    # �� �� �������, ��� ������������ ����������.
    # ���������, �� �� � ���� ��������� �������� "�������"?
    if req['request']['original_utterance'].lower() in [
        '�����',
        '�����',
        '�������',
        '������'
    ]:
        # ������������ ����������, ���������.
        res['response']['text'] = '����� ����� ����� �� ������.�������!'
        res['response']['end_session'] = True
        return

    # ���� ���, �� �������� ��� ������ �����!
    res['response']['text'] = \
        f"��� ������� '{req['request']['original_utterance']}', � �� ���� �����!"
    res['response']['buttons'] = get_suggests(user_id)


# ������� ���������� ��� ��������� ��� ������.
def get_suggests(user_id):
    session = sessionStorage[user_id]

    # �������� ��� ������ ��������� �� �������.
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:2]
    ]

    # ������� ������ ���������, ����� ��������� �������� ������ ���.
    session['suggests'] = session['suggests'][1:]
    sessionStorage[user_id] = session

    # ���� �������� ������ ���� ���������, ���������� ���������
    # �� ������� �� ������.������.
    if len(suggests) < 2:
        suggests.append({
            "title": "�����",
            "url": "https://market.yandex.ru/search?text=����",
            "hide": True
        })

    return suggests


if __name__ == '__main__':
    app.run(port=5001)