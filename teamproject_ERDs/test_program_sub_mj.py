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

def test_create(answer_type, quest_type) :
    print("문제와 선택지를 입력하세요:")

    for x in range(quest_type):
        QUEST = input(f"문항 {x+1}: ")

        with conn.cursor() as cursor:
            # QUEST_INFO_ID 가져오기
            sql = "SELECT COUNT(QUEST_INFO_ID) FROM QUEST_INFO"
            cursor.execute(sql)
            data = cursor.fetchall()
            QUEST_INFO_ID = "QUEST_INFO_"+str(data[0][0]+1)
            # MYSQL에 문제 저장
            sql = "INSERT INTO QUEST_INFO (QUEST_INFO_ID, QUEST, QUEST_NUMBER) VALUES (%s, %s, %s)"
            cursor.execute(sql, (QUEST_INFO_ID, QUEST, x+1))
            conn.commit()

            # 선택지 입력
            print("선택지: ")
            for y in range(answer_type):
                answer = input(f"{y+1}. ")
                # answer_score = int(input("점수를 입력하세요: "))
                # ANSWER_INFO_ID 가져오기
                sql = "SELECT COUNT(ANSWER_INFO_ID) FROM ANSWER_INFO"
                sq2 = "UPDATE ANSWER_INFO SET ANSWER_SCORE=%s WHERE QUEST_INFO_ID=%s AND ANSWER_NUMBER=%s"
                cursor.execute(sql)
                data = cursor.fetchall()
                ANSWER_INFO_ID = "ANSWER_INFO_"+str(data[0][0]+1)
            # MYSQL에 선택지 저장
                sql = "INSERT INTO ANSWER_INFO (ANSWER_INFO_ID, ANSWER, ANSWER_NUMBER, QUEST_INFO_ID) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (ANSWER_INFO_ID, answer, y+1, QUEST_INFO_ID))
                # cursor.execute(sq2, (answer_score, QUEST_INFO_ID, y+1))
                conn.commit()
        
        # # 점수 입력
        # answer_score = int(input("점수를 입력하세요: "))
        # sql = "UPDATE ANSWER_INFO SET ANSWER_SCORE=%s WHERE QUEST_INFO_ID=%s AND ANSWER_NUMBER=%s"
        # cursor.execute(sql, (answer_score, QUEST_INFO_ID, y+1))
        # conn.commit()

test_create(answer_type, quest_type)



# MYSQL에서 테이블 한번에 삭제시 오류 날때
# 비활성화: SET foreign_key_checks = 0;
# 데이터 삽입
# 활성화: SET foreign_key_checks = 1;





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
