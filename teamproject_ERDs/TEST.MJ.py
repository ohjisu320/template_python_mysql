import pymysql

# 데이터베이스 연결 설정
conn = pymysql.connect(
    host='python_mysql_mysql',  # 컨테이너 이름 또는 IP
    user='cocolabhub',
    password='cocolabhub',
    db='python_mysql',  # 데이터베이스 이름
    charset='utf8mb4')

# try:
answer_type = int(input("문제 유형을 입력하세요 (N지 선다형): "))
quest_type = int(input("문제 수를 입력하세요 (N개 문항) : "))
print("문제와 선택지를 입력하세요:")

for x in range(quest_type):
    QUEST = input(f"문항 {x+1}: ")
    # try:
    with conn.cursor() as cursor:
        # QUEST_INFO_ID 가져오기
        sql = "SELECT COUNT(QUEST_INFO_ID) FROM QUEST_INFO"
        cursor.execute(sql)
        data = cursor.fetchall()
        QUEST_INFO_ID = "QUEST_INFO_"+str(data[0][0]+1)
        # 문제 저장
        sql = "INSERT INTO QUEST_INFO (QUEST_INFO_ID, QUEST, QUEST_NUMBER) VALUES (%s, %s, %s)"
        cursor.execute(sql, (QUEST_INFO_ID, QUEST, x+1))
        conn.commit()

        # 선택지 입력
        print("선택지: ")
        for y in range(answer_type):
            answer = input(f"{y+1}. ")
            # ANSWER_INFO_ID 가져오기
            sql = "SELECT COUNT(ANSWER_INFO_ID) FROM ANSWER_INFO"
            cursor.execute(sql)
            data = cursor.fetchall()
            ANSWER_INFO_ID = "ANSWER_INFO_"+str(data[0][0]+1)
            # 선택지 저장
            sql = "INSERT INTO ANSWER_INFO (ANSWER_INFO_ID, ANSWER, ANSWER_NUMBER, QUEST_INFO_ID) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (ANSWER_INFO_ID, answer, y+1, QUEST_INFO_ID))
            conn.commit()
        # except Exception as e:
        #     print(f"에러 발생: {e}")

# finally:
#     conn.close()
