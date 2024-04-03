import pymysql

# 데이터베이스 연결 설정
conn = pymysql.connect(
    host='python_mysql_mysql',  # 컨테이너 이름 또는 IP
    user='cocolabhub',
    password='cocolabhub',
    db='python_mysql',  # 데이터베이스 이름
    charset='utf8mb4')

answer_type = int(input("문제 유형을 입력하세요 (N지 선다형): "))
quest_type = int(input("문제 수를 입력하세요 (N개 문항) : "))
print("문제와 선택지를 입력하세요:")

for x in range(quest_type) :
    QUEST = input(f"문항 {x+1}: ")
    try : 
        with conn.cursor() as cursor:
        # Read
            sql = "SELECT QUEST_INFO_ID FROM QUEST_INFO"
            cursor.execute(sql)
            data = cursor.fetchall()
            for row in data:
                last = row  # 각 행 출력
            
            QUEST_INFO_ID_NUMBER = int(last[0][11:])
    except :
        QUEST_INFO_ID_NUMBER = 3
    # mysql로 문제 저장
    with conn.cursor() as cursor:
        # Create
        sql = "INSERT INTO QUEST_INFO (QUEST_INFO_ID,QUEST, QUEST_NUMBER) VALUES (%s, %s, %s)"
        cursor.execute(sql, (f"QUEST_INFO_{QUEST_INFO_ID_NUMBER+1}", QUEST, x+1))
        conn.commit()
        
    with conn.cursor() as cursor:
    # Read
        sql = "SELECT ANSWER_INFO_ID FROM ANSWER_INFO"
        cursor.execute(sql)
        data = cursor.fetchall()
        for row in data:
            last = row  # 각 행 출력
        
        ANSWER_INFO_ID_NUMBER = int(last[0][12:])
        
        
    # 선택지 입력
    print("선택지: ")
    for y in range(answer_type):
        answer = input(f"{y+1}. ")
        # Create
        sql = "INSERT INTO ANSWER_INFO (ANSWER_INFO_ID,ANSWER, ANSWER_NUMBER, QUEST_INFO_ID) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (f"ANSWER_INFO_{ANSWER_INFO_ID_NUMBER+1}", answer, y+1, f"QUEST_INFO_{x+1}"))
        conn.commit()

conn.close()




# if __name__ == "__main__" :
#     import pymysql
#     # 데이터베이스 연결 설정
#     conn = pymysql.connect(
#         host='python_mysql_mysql',  # 컨테이너 이름 또는 IP
#         user='cocolabhub',
#         password='cocolabhub',
#         db='python_mysql',  # 데이터베이스 이름
#         charset='utf8mb4')
    
#     create_test()

    # with conn.cursor() as cursor:
    #     # Create
    #     sql = "INSERT INTO TableName (pk_id,column1, column2) VALUES (%s, %s, %s)"
    #     cursor.execute(sql, (1, 'value1', 'value2'))
    #     conn.commit()
