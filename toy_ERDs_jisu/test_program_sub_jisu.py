
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
        sql = "INSERT INTO USER_INFO (USER_INFO_ID,NAME) VALUES (%s, %s)"
        cursor.execute(sql, (USER_INFO_ID, USER_NAME))
        conn.commit()
    
    print("문제를 풀어주세요")

    with conn.cursor() as cursor:
        # 문제 읽기
        sql = "SELECT * FROM QUEST_ANSWER WHERE PARENT_ID IS NULL;"
        cursor.execute(sql)
        quest_data = cursor.fetchall()
        for row in quest_data:
            # 문제 출력 및 반복
            print(str(row[1])+". "+str(row[2]))
            QUEST_INFO_ID = row[0]
            pass

            # 선택지 출력 및 반복
            with conn.cursor() as cursor:
                # Read
                sql = "WITH RECURSIVE SubQuestanswers AS ( SELECT QA.* FROM QUEST_ANSWER QA WHERE QA.PARENT_ID = %s UNION ALL SELECT QA.* FROM QUEST_ANSWER QA INNER JOIN SubQuestanswers SD ON QA.PARENT_ID = QA.CHILD_ID) SELECT * FROM SubQuestanswers;"
                cursor.execute(sql, (QUEST_INFO_ID))
                data = cursor.fetchall()
                for row in data:
                    print(str(row[1])+") "+row[2])
            
            
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

            # 유저 정답과 QUEST_ANSWER의 NUMBER와 매칭한 CHILD_ID 출력

            with conn.cursor() as cursor:
                # Read
                sql =  f"WITH RECURSIVE SubQuestanswer AS ( SELECT QA.* FROM QUEST_ANSWER QA WHERE QA.PARENT_ID = 'QUEST_ANSWER_1' UNION ALL SELECT QA.* FROM QUEST_ANSWER QA INNER JOIN SubQuestanswer SD ON QA.PARENT_ID = QA.CHILD_ID) SELECT SubQuestanswer.* FROM SubQuestanswer HAVING NUMBER=%s;"
                cursor.execute(sql, user_answer)
                data = cursor.fetchall()
                CHILD_ID = data[0][0]




            # 유저 정답 저장
            with conn.cursor() as cursor:
                # Create
                sql = "INSERT INTO USER_ANSWER (CHILD_ID,USER_INFO_ID) VALUES (%s, %s)"
                cursor.execute(sql, (CHILD_ID, USER_INFO_ID))
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

# parent_id = null 인 것 중 첫번째의 number 출력, 
with conn.cursor() as cursor:
        # Read
        sql = "SELECT NUMBER FROM QUEST_ANSWER WHERE PARENT_ID IS NULL;"
        cursor.execute(sql)
        data = cursor.fetchall()
        for row in data:
            print(f"{int(row[0])}번 문제의 답: ")
            sql = "SELECT NUMBER FROM QUEST_ANSWER WHERE PARENT_ID = 'QUEST_ANSWER_1' AND SCORE >0 ;"
            cursor.execute(sql)
            data = cursor.fetchall()
            for index, row in enumerate(data):
                if index < len(data)-1 :
                    print(row[0], end=', ')
                else :
                    print(row[0])


# 응시자별 채점 결과 출력
with conn.cursor() as cursor:
    # Read
    sql = "WITH RECURSIVE SubQuestanswers AS ( SELECT QA.* FROM  QUEST_ANSWER QA  UNION ALL  SELECT QA.* FROM QUEST_ANSWER QA INNER JOIN SubQuestanswers SD ON QA.CHILD_ID = QA.PARENT_ID ) SELECT USER_INFO.NAME, USER_ANSWER.USER_INFO_ID, QUEST_ANSWER.PARENT_ID,  QUEST_ANSWER.SCORE, SubQuestanswers.NUMBER FROM USER_ANSWER   LEFT JOIN QUEST_ANSWER  ON QUEST_ANSWER.CHILD_ID = USER_ANSWER.CHILD_ID LEFT JOIN SubQuestanswers ON SubQuestanswers.CHILD_ID = QUEST_ANSWER.PARENT_ID LEFT JOIN USER_INFO ON USER_INFO.USER_INFO_ID = USER_ANSWER.USER_INFO_ID ORDER BY USER_INFO_ID, NUMBER;"
    cursor.execute(sql)
    data = cursor.fetchall()
    print("응시자별 채점 결과: ")
    user = ''
    for index, row in enumerate(data):  
        
        if user ==  row[0]:   
            print(f"{row[4]}번. {row[3]}점")
        else :        
            user =  row[0]
            print(f"응시자{row[0]}.  ")
            print(f"{row[4]}번. {row[3]}점")
        
            
    print("")
        

    sql = f"SELECT ROUND(SUM(QUEST_ANSWER.SCORE)/COUNT(USER_ANSWER.USER_INFO_ID), 2) FROM USER_ANSWER LEFT JOIN QUEST_ANSWER ON QUEST_ANSWER.CHILD_ID = USER_ANSWER.CHILD_ID LEFT JOIN USER_INFO ON USER_INFO.USER_INFO_ID = USER_ANSWER.USER_INFO_ID ;"
    cursor.execute(sql)
    data = cursor.fetchall()
    print("")
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
