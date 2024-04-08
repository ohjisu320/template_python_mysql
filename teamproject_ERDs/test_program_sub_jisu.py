
import pymysql



# 데이터베이스 연결 설정
conn = pymysql.connect(
    host='python_mysql_mysql',  # 컨테이너 이름 또는 IP
    user='cocolabhub',
    password='cocolabhub',
    db='python_mysql',  # 데이터베이스 이름
    charset='utf8mb4')

# 초기값들 모음

end_sign = 'c'


while end_sign == 'c' :
    try: 
        user_score = 0
        USER_NAME = input("응시자 이름을 입력하세요: ")
        with conn.cursor() as cursor:
            # Read
            sql = "SELECT COUNT(USER_INFO_ID) FROM USER_INFO"
            cursor.execute(sql)
            data = cursor.fetchall()
            USER_INFO_number = data[0][0]

        
        USER_INFO_ID = f"USER_INFO_{USER_INFO_number+1}"
    except : 
        
        USER_INFO_ID = "USER_INFO_1"


    # mysql로 저장
    with conn.cursor() as cursor:
        # Create
        sql = "INSERT INTO USER_INFO (USER_INFO_ID,USER_NAME) VALUES (%s, %s)"
        cursor.execute(sql, (USER_INFO_ID, USER_NAME))
        conn.commit()
    
    print("문제를 풀어주세요")

    with conn.cursor() as cursor:
        # 문제 읽기
        sql = "SELECT * FROM QUEST_INFO"
        cursor.execute(sql)
        quest_data = cursor.fetchall()
        for row in quest_data:
            # 문제 출력 및 반복
            print(str(row[2])+". "+row[1])
            QUEST_INFO_ID = row[0]
            pass

            # 선택지 출력 및 반복
            with conn.cursor() as cursor:
                # Read
                sql = f"SELECT * FROM ANSWER_INFO HAVING QUEST_INFO_ID = '{QUEST_INFO_ID}';"
                cursor.execute(sql)
                data = cursor.fetchall()
                for row in data:
                    print(str(row[3])+") "+row[2])
            
            
            # 답항 입력 전 USER_ANSWER_INFO_ID 몇갠지 계산
            try : 
                with conn.cursor() as cursor:
                    # Read
                    sql = f"SELECT COUNT(USER_ANSWER_INFO_ID) FROM USER_ANSWER_INFO"
                    cursor.execute(sql)
                    data = cursor.fetchall()
                    USER_ANSWER_INFO_ID = "USER_ANSWER_INFO_"+str(data[0][0]+1)
                    
            except :
                USER_ANSWER_INFO_ID = "USER_ANSWER_INFO_1"
            # 답항 입력
            user_answer = input("답: ")

            # 유저 정답과 ANSWER_INFO_ID와 매칭한 값 출력

            with conn.cursor() as cursor:
                # Read
                sql =  f"SELECT * FROM ANSWER_INFO  HAVING QUEST_INFO_ID = '{QUEST_INFO_ID}' AND ANSWER_NUMBER = '{user_answer}';"
                cursor.execute(sql)
                data = cursor.fetchall()
                ANSWER_INFO_ID = data[0][0]
                user_score = user_score+int(data[0][4])





            # 유저 정답 저장
            with conn.cursor() as cursor:
                # Create
                sql = "INSERT INTO USER_ANSWER_INFO (USER_ANSWER_INFO_ID,USER_INFO_ID, ANSWER_INFO_ID) VALUES (%s, %s, %s)"
                cursor.execute(sql, (USER_ANSWER_INFO_ID, USER_INFO_ID,ANSWER_INFO_ID))
                conn.commit()
            
        # 유저 점수 저장
        with conn.cursor() as cursor:
            # Update
            sql = "UPDATE USER_INFO SET USER_SCORE=%s WHERE USER_INFO_ID=%s"
            cursor.execute(sql, (user_score, USER_INFO_ID))
            conn.commit()
       
    
    
   
        end_sign = input('다음 응시자가 있나요? (계속: c, 종료: x) : ')
        while True : 
            if end_sign == 'c' :
                break
            elif end_sign == 'x' :
                print("program End!")
                break
            else :
                end_sign = input('잘못입력하셨습니다! 다음 응시자가 있나요? (계속: c, 종료: x) : ')
        


# 정답 출력
with conn.cursor() as cursor:
    # Read
    sql = f"SELECT * FROM  ANSWER_INFO HAVING ANSWER_SCORE >0;"
    cursor.execute(sql)
    data = cursor.fetchall()
    print("각 문항 정답 :")
    for row in data:
        print(f"{row[3]}, ")


# 응시자별 채점 결과 출력
with conn.cursor() as cursor:
    # Read
    sql = f"SELECT * FROM USER_INFO GROUP BY USER_INFO_ID;"
    cursor.execute(sql)
    data = cursor.fetchall()
    print("응시자별 채점 결과: ")
    for row in data:
        print(f"{row[1]}:  {row[2]}")

    sql = f"SELECT ROUND(SUM(USER_SCORE)/count(USER_INFO_ID),0) FROM USER_INFO;"
    cursor.execute(sql)
    data = cursor.fetchall()
    print(f"과목 평균 점수: {data[0][0]}")
        
        






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
    #     sql = "INSERT INTO TableName (id,column1, column2) VALUES (%s, %s, %s)"
    #     cursor.execute(sql, (1, 'value1', 'value2'))
    #     conn.commit()
