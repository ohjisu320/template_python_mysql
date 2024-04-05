
import pymysql


# 데이터베이스 연결
def connect_database() :
    conn = pymysql.connect(
        host='python_mysql_mysql',  # 컨테이너 이름 또는 IP
        user='cocolabhub',
        password='cocolabhub',
        db='python_mysql',  # 데이터베이스 이름
        charset='utf8mb4')
    return conn

# 시험 출제
def test_create(conn, answer_type, quest_type) :
    # 시험 출제 전 QUEST/ANSWER 테이블 초기화
    try : 
        with conn.cursor() as cursor:
            sql_reset_0 = "SET FOREIGN_KEY_CHECKS = 0;"
            sql_reset_1 = "SET FOREIGN_KEY_CHECKS = 1;"
            sql_delete_quest = "DELETE FROM QUEST_INFO;"
            sql_delete_answer = "DELETE FROM ANSWER_INFO;"
            sql_delete_useranswer = "DELETE FROM USER_ANSWER_INFO;"
            sql_delete_user = "DELETE FROM USER_INFO;"
            # cursor.execute(sql_reset_0)
            # cursor.execute(sql_delete_quest)
            # cursor.execute(sql_delete_answer)
            # cursor.execute(sql_delete_useranswer)
            # cursor.execute(sql_delete_user)
            # cursor.execute(sql_reset_1)
            conn.commit()
    except :
        pass
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
            correct_answer = input("정답: ")
            answer_score = int(input("점수 : "))
            
            # Update
            sql = "UPDATE ANSWER_INFO SET ANSWER_SCORE = %s WHERE QUEST_INFO_ID =%s AND ANSWER_NUMBER=%s;"
            cursor.execute(sql, (answer_score, QUEST_INFO_ID, correct_answer))
            conn.commit()
        

# 시험 응시
def test_start(end_sign, conn) :
    while end_sign == 'c' :
        with conn.cursor() as cursor:
            try: 
                # 초기값
                user_score = 0
                USER_NAME = input("응시자 이름을 입력하세요: ")
                # USER_INFO_ID 불러오기
                sql = "SELECT COUNT(USER_INFO_ID) FROM USER_INFO"
                cursor.execute(sql)
                data = cursor.fetchall()
                USER_INFO_number = data[0][0]
            
                USER_INFO_ID = f"USER_INFO_{USER_INFO_number+1}"
            except : 
                
                USER_INFO_ID = "USER_INFO_1"

            # 위에서 받은 USER_INFO_ID대로 입력값과 함께 저장
            sql = "INSERT INTO USER_INFO (USER_INFO_ID,USER_NAME) VALUES (%s, %s)"
            cursor.execute(sql, (USER_INFO_ID, USER_NAME))
            conn.commit()

            print("문제를 풀어주세요")

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
                # with conn.cursor() as cursor:
                # Read
                sql = f"SELECT * FROM ANSWER_INFO HAVING QUEST_INFO_ID = '{QUEST_INFO_ID}';"
                cursor.execute(sql)
                data = cursor.fetchall()
                for row in data:
                    print(str(row[3])+") "+row[2])
                
                
                # 답항 입력 전 USER_ANSWER_INFO_ID 몇갠지 계산
                try : 
                    # with conn.cursor() as cursor:
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
                sql =  f"SELECT * FROM ANSWER_INFO  HAVING QUEST_INFO_ID = '{QUEST_INFO_ID}' AND ANSWER_NUMBER = '{user_answer}';"
                cursor.execute(sql)
                data = cursor.fetchall()
                ANSWER_INFO_ID = data[0][0]
                # try : 
                #     user_score = user_score+int(data[0][4])
                # except : 
                #     user_score = user_score+0

                # 유저 정답 저장
                sql = "INSERT INTO USER_ANSWER_INFO (USER_ANSWER_INFO_ID,USER_INFO_ID, ANSWER_INFO_ID) VALUES (%s, %s, %s)"
                cursor.execute(sql, (USER_ANSWER_INFO_ID, USER_INFO_ID,ANSWER_INFO_ID))
                conn.commit()
                
            # # 유저 점수 저장
            # # Update
            # sql = "UPDATE USER_INFO SET USER_SCORE=%s WHERE USER_INFO_ID=%s"
            # cursor.execute(sql, (user_score, USER_INFO_ID))
            # conn.commit()
            # 종료시스템
            end_sign = input('다음 응시자가 있나요? (계속: c, 종료: x) : ')
            while True : 
                if end_sign == 'c' :
                    break
                elif end_sign == 'x' :
                    print("Test End!")
                    break
                else :
                    end_sign = input('잘못입력하셨습니다! 다음 응시자가 있나요? (계속: c, 종료: x) : ')

# 시험 채점
def grading(conn) :
    # 정답 출력
    print("")
    print("시험 결과를 조회합니다.")
    with conn.cursor() as cursor:
        # Read
        sql = f"SELECT * FROM  ANSWER_INFO HAVING ANSWER_SCORE >0;"
        cursor.execute(sql)
        data = cursor.fetchall()
        print("각 문항 정답 :", end=' ')

        for index, row in enumerate(data):
            if index < len(data)-1 :
                print(row[3], end=', ')
            else :
                print(row[3])

        # 응시자별 채점 결과 출력 -- 원본 - 컬럼에 저장해서 불러오기
        # Read
        # sql = f"SELECT * FROM USER_INFO GROUP BY USER_INFO_ID ORDER BY USER_SCORE DESC;"
        # cursor.execute(sql)
        # data = cursor.fetchall()
        # print("응시자별 채점 결과: ")
        # for row in data:
        #     print(f"{row[1]}:  {row[2]}")

        # sql = f"SELECT ROUND(SUM(USER_SCORE)/count(USER_INFO_ID),0) FROM USER_INFO;"
        # cursor.execute(sql)
        # data = cursor.fetchall()
        # print(f"과목 평균 점수: {data[0][0]}")


        # 응시자별 채점 결과 출력 쿼리문으로 작성
    
        sql = "SELECT USER_SCORE.USER_INFO_ID, USER_SCORE.USER_NAME, SUM(USER_SCORE.ANSWER_SCORE) FROM (SELECT USER_ANSWER_INFO.USER_INFO_ID, USER_INFO.USER_NAME, ANSWER_INFO.ANSWER_SCORE FROM USER_ANSWER_INFO INNER JOIN ANSWER_INFO ON ANSWER_INFO.ANSWER_INFO_ID = USER_ANSWER_INFO.ANSWER_INFO_ID  INNER JOIN USER_INFO ON USER_ANSWER_INFO.USER_INFO_ID = USER_INFO.USER_INFO_ID  ) AS USER_SCORE GROUP BY USER_SCORE.USER_INFO_ID;"
        cursor.execute(sql)
        data = cursor.fetchall()
        print("응시자별 채점 결과: ")
        for row in data:
            if row[2] == None : 
                print(f"{row[1]}:  0")
            else : 
                print(f"{row[1]}:  {row[2]}")

                    
            

        sql = "SELECT SUM(USER_SCORE_UPDATE.USER_SCORE_SEP)/COUNT(USER_SCORE_UPDATE.USER_NAME) FROM (SELECT USER_SCORE.USER_NAME, SUM(USER_SCORE.ANSWER_SCORE) AS USER_SCORE_SEP FROM (SELECT USER_ANSWER_INFO.USER_INFO_ID, USER_INFO.USER_NAME, ANSWER_INFO.ANSWER_SCORE  FROM USER_ANSWER_INFO  INNER JOIN ANSWER_INFO ON ANSWER_INFO.ANSWER_INFO_ID = USER_ANSWER_INFO.ANSWER_INFO_ID   INNER JOIN USER_INFO ON USER_ANSWER_INFO.USER_INFO_ID = USER_INFO.USER_INFO_ID  )  AS USER_SCORE GROUP BY USER_SCORE.USER_INFO_ID) AS USER_SCORE_UPDATE;"
        cursor.execute(sql)
        data = cursor.fetchall()
        print(f"과목 평균 점수: {round(data[0][0],2)}")
        



if __name__ == "__main__" :
    conn = connect_database()
    # answer_type = int(input("문제 유형을 입력하세요 (N지 선다형): "))
    # quest_type = int(input("문제 수를 입력하세요 (N개 문항) : "))
    # test_create(answer_type, quest_type)
    
    # 초기값
    end_sign = 'c'
    test_start_sign='Y'
    while True :
        test_start_sign = input("시험을 응시하시겠습니까(Y/N)? :")
        if test_start_sign == 'Y':
            test_start(end_sign, conn)
            grading(conn)
            break
        elif test_start_sign == 'N':
            grading(conn)
            break
        else :
            test_start_sign = input("잘못입력하셨습니다! 시험을 응시하시겠습니까(Y/N)? :")

    
