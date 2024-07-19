from flask import Flask, request, redirect, url_for, render_template, session
import naver_map
import database
import query
from datetime import timedelta
import random

app = Flask(__name__)

# secret_key 설정 (session데이터 암호화 키)
app.secret_key = 'ABC'
# session의 지속시간을 설정
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=60)

# 클라이언트 ID와 비밀번호
client_id = 'gx4wwzfwty'
client_secret = '71tBFr6FCb6qJPGzS5HjLekN8qhPIsBryYehi5d2'

# 데이터베이스 class 생성 (데이터베이스 정보 저장)
_db = database.MyDB(
    _host = 'localhost', 
    _port = 3306, 
    _user = 'trillion', 
    _password = '1234', 
    _database = 'trillion'
)


# 로그인 화면
@app.route('/')
def index():
    return render_template("index.html")

# 메뉴 화면
@app.route('/menu')
def menu():
    # session에 데이터가 존재하지 않는다면 로그인화면으로 이동
    try:
        if session['user_info']:
            return render_template('menu.html')
        else:
            return redirect('/')
    except:
        return redirect('/')

# 직장 추천 스와이프 페이지
# 로그인을 한 사람의 정보를 기준으로 
# 직장을 추천 ( 데이터베이스에서 로그인을 한 유저의 address를 기준으로 회사 위치를 생각하여 랜덤하게 10개를 추천  )
@app.route('/company')
def company():
    try:
        # session에 데이터가 존재하지 않는다면 로그인화면으로 이동
        if session['user_info']:
            # print(session)
            # 로그인을 한 유저의 주소를 변수에 저장 
            user_addr = session['user_info']['address']
            user_sido = user_addr.split()[0].strip()
            print(user_sido)
            # 회사들의 정보를 로드 
            db_result = _db.sql_query(
                query.company
            )
            # print(len(db_result))
            company_list = []
            # print("유저 주소의 시도 : ", user_sido)
            # db_result에서 company_address에 user_sido 데이터가 포함되어있는 데이터만 추출
            for result in db_result:
                if user_sido in result['company_address']:
                    company_list.append(result)
            # print(len(company_list))
            data = random.sample(company_list, 10)
            keys = data[0].keys()
            print(keys)
            # print(data)
            return render_template('company.html', data=data, keys=keys)
        else:
            return redirect('/')
    except Exception as e:
        print(e)
        return redirect('/')
    # return render_template('company.html')

# 선택한 직장 리스트 화면
@app.route('/company_list')
def company_list():
    # session에 데이터가 존재하지 않는다면 로그인화면으로 이동
    if session['user_info']:
        return render_template('company_list.html')
    else:
        return redirect('/')


# 로그인 프로세스 
@app.route('/signin', methods=['post'])
def signin():
    # 유저가 보낸 아이디 패스워드를 변수에 저장 
    input_id = request.form['_id']
    input_pass = request.form['_pass']
    print('/signin message : ', input_id, input_pass)
    # 데이터베이스에서 유저 id, password 정보 조회
    db_result = _db.sql_query(
        query.login, 
        input_id, 
        input_pass
    )
    # db_result는  [{id:xxx, password:xxxx, name:xxx}]
    # 로그인이 성공했다는 조건 -> db_result 안에 데이터가 존재
    if db_result:
        # session에 데이터를 저장
        session['user_info'] = db_result[0]
        print("세션 데이터", session['user_info'])
        return redirect('/menu')
    else:
        return redirect('/')

@app.route('/send_data')
def send_data():
    input_id = session['user_info']['id']
    input_company_name = request.args['_name']
    input_selected = request.args['_select']
    print(input_id, input_company_name, input_selected)
    try:
        db_result = _db.sql_query(
            query.history, 
            input_id, 
            input_company_name, 
            input_selected
        )
        print(db_result)
    except Exception as e:
        print(e)
    return 'data send'






app.run(debug=True)