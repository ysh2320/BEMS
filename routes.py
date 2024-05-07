from flask import send_from_directory, request, jsonify,flash,session,redirect,url_for,Blueprint,render_template
from database import *
from database import conn

cursor= conn.cursor()
routes = Blueprint('routes',__name__)

#빌딩 floor 초기화
@routes.route('/create_floor', methods=['POST'])
def create_floor():
    buildID = request.json.get('buildID')
    floorNum = request.json.get('floorNum')

    cursor.execute("SELECT floorNum FROM Building WHERE buildID = ?", (buildID,))
    building_info = cursor.fetchone()

    if building_info:
        floor_prefix = str(buildID)  # floorID의 앞부분은 buildID와 동일하게 설정
        for floor in range(1, floorNum + 1):
            f = floor
            floorID = f'{floor_prefix}{floor:03}'  # floorID 생성

            cursor.execute("INSERT INTO Floor (floorID, buildingID, floorNum) VALUES (?, ?, ?)", (floorID, buildID,f))
        conn.commit()
        return jsonify({'message': 'Floor 생성 완료'})
    else:
        return jsonify({'message': '해당하는 빌딩 정보가 없습니다.'}), 404


#------------------------------------------------------------------------

#회원가입 라우트
@routes.route('/aptId')
def getAPTId():
    cursor = conn.cursor()
    cursor.execute('SELECT buildingID from Building')
    rows = cursor.fetchall()
    # 쿼리 결과를 JSON 형식으로 변환하여 반환
    apartment_ids = [row[0] for row in rows]
    return jsonify(apartment_ids)

@routes.route('/roomNumber', methods= ['post'])
def getRoomNum():
    aptID = request.json.get('apartmentId')
    cursor = conn.cursor()
    cursor.execute('SELECT floorNum from floor where buildingID = %s',aptID)
    rows = cursor.fetchall()
    roomNum = [row[0] for row in rows]
    return jsonify(roomNum)

@routes.route('/signupMember', methods=['POST','get'])
def add_member():
    
        m_id = request.json.get('id')
        cursor = conn.cursor()
        cursor.execute("SELECT M_id FROM Member WHERE M_ID = %s", m_id)
        dupID = cursor.fetchone()
        if dupID:
            print(dupID)
            return jsonify({'error': 'ID가 중복되었습니다.'}), 400
        
        m_name = request.json.get('name')
        m_age = request.json.get('age')
        if not m_age.isdigit():
            return jsonify({'error': '나이는 숫자로만 이루어진 정수여야 합니다.'}), 400
        
        m_password = request.json.get('password')
        m_floorID = int(request.json.get('floorID'))
        m_buildingId = int(request.json.get('buildingId'))
        if not (m_floorID or m_buildingId):
            return jsonify({'error': '건물 또는 호수를 선택하세요.'}), 400
        print(type(m_floorID), type(m_buildingId), type(m_name))

        cursor.execute("INSERT INTO Member VALUES (%s, %s, %s, %s, %s, %s)",
                        (m_id, m_name, m_age, m_password, m_floorID, m_buildingId))
        conn.commit()
        return jsonify({'message': '회원 추가 완료'}) ,200
    

    

#trade의 세션라우트
@routes.route('/setSession' ,methods = ['POST','GET'])
def setSession():
    if request.method == 'POST':
        login_id = request.json.get('loginID')
        session['user_id'] = login_id
        return jsonify({'user_id': session['user_id']})
    else:
        return jsonify({'error': 'Method not allowed'}), 405
    
@routes.route('/getUserName')
def get_current_user():
    print(session)
    if 'user_id' in session:
        return jsonify({'user_id': session['user_id']}),200
    else:
        return jsonify({'error': '사용자가 로그인되지 않았습니다'}), 401

@routes.route('/getTradeInfo', methods=['POST'])
def get_trade_info():
    try:
        intValue = request.json.get('intValue')
        cursor = conn.cursor()
        # sellList 테이블에서 intValue에 해당하는 sellNum 찾기
        cursor.execute('SELECT sellerID FROM sellList WHERE sellNum = %s', intValue)
        row = cursor.fetchone()
        print(session['user_id'])
        # 검색 결과가 있을 경우 해당 데이터 반환, 없을 경우 None 반환
        if row:
            sellerID = row[0]
            cursor.execute('SELECT * FROM admin WHERE A_id = %s', sellerID)
            sellerInfo = cursor.fetchone()
            print(sellerInfo)
            if sellerInfo:
                # sellerInfo를 구조체로 정리하여 JSON 응답으로 반환
                response_data = {
                    'sellerID': sellerInfo[0],
                    'name': sellerInfo[1],
                    'age': sellerInfo[2],
                    'password': sellerInfo[3],
                    'buildID': sellerInfo[4],
                    'secondPass' : sellerInfo[5]
                }
                return jsonify(response_data), 200
            else:
                return jsonify({'error': 'Seller info not found'}), 404
        else:
            return jsonify({'error': 'SellNum not found'}), 401
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@routes.route('/getAdminInfo', methods=['POST'])
def get_AdminInfo():
    print(request.json)
    buyer = get_admin(request.json.get('buyerId'))
    seller = get_admin(request.json.get('sellerId'))
    user = [buyer,seller]
    print(user)
    if user:
        return user
    else:
        return jsonify({'error': 'user not found'}), 401

@routes.route('/sellList')
def sell_list():
    cursor = conn.cursor()
    cursor.execute('select * from sellList')
    rows = cursor.fetchall()
    print(rows)
    return jsonify(rows), 200



#adminLogin
@routes.route('/adminLogin', methods=['POST'])
def admin_login():
    if request.method == 'POST':
        data = request.json  # JSON 형식의 데이터를 가져옴
        id = data.get('id')  # id 키에 해당하는 값 가져옴
        password = data.get('password')  # password 키에 해당하는 값 가져옴
        
        admin = login_admin(id, password)
        
        if admin:
            return admin
        else:
            return jsonify({'error': 'user not found'}), 401
    else:
        return jsonify({'error': 'not found'}), 404
    
@routes.route('/memberLogin', methods=['POST'])
def member_login():
    if request.method == 'POST':
        data = request.json  # JSON 형식의 데이터를 가져옴
        id = data.get('id')  # id 키에 해당하는 값 가져옴
        password = data.get('password')  # password 키에 해당하는 값 가져옴
        print(id, password)
        user = get_user(id, password)
        print(user)
        if user:
            return user
        else:
            return jsonify({'error': 'user not found'}), 401
    else:
        return jsonify({'error': 'not found'}), 404
    
    
@routes.route('/')
def index():
    if "user_id" not in session:
        session["user_id"] = None
    return None