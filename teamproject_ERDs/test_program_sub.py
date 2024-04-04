
import pymysql

def connect_database() :

    # 데이터베이스 연결 설정
    conn = pymysql.connect(
        host='python_mysql_mysql',  # 컨테이너 이름 또는 IP
        user='cocolabhub',
        password='cocolabhub',
        db='python_mysql',  # 데이터베이스 이름
        charset='utf8mb4')
    return conn

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
                user_score = user_score+int(data[0][4])

                # 유저 정답 저장
                sql = "INSERT INTO USER_ANSWER_INFO (USER_ANSWER_INFO_ID,USER_INFO_ID, ANSWER_INFO_ID) VALUES (%s, %s, %s)"
                cursor.execute(sql, (USER_ANSWER_INFO_ID, USER_INFO_ID,ANSWER_INFO_ID))
                conn.commit()
                
            # 유저 점수 저장
            # Update
            sql = "UPDATE USER_INFO SET USER_SCORE=%s WHERE USER_INFO_ID=%s"
            cursor.execute(sql, (user_score, USER_INFO_ID))
            conn.commit()
            # 종료시스템
            end_sign = input('다음 응시자가 있나요? (계속: c, 종료: x) : ')
            while True : 
                if end_sign == 'c' :
                    break
                elif end_sign == 'x' :
                    print("program End!")
                    break
                else :
                    end_sign = input('잘못입력하셨습니다! 다음 응시자가 있나요? (계속: c, 종료: x) : ')

    
def grading(conn) :
    # 정답 출력
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

        # 응시자별 채점 결과 출력 -- 원본
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


        # 응시자별 채점 결과 출력
        # Read
        sql = "SELECT USER_SCORE.USER_INFO_ID, USER_SCORE.USER_NAME, SUM(USER_SCORE.ANSWER_SCORE) FROM (SELECT USER_ANSWER_INFO.USER_INFO_ID, USER_INFO.USER_NAME, ANSWER_INFO.ANSWER_SCORE FROM USER_ANSWER_INFO INNER JOIN ANSWER_INFO ON ANSWER_INFO.ANSWER_INFO_ID = USER_ANSWER_INFO.ANSWER_INFO_ID  INNER JOIN USER_INFO ON USER_ANSWER_INFO.USER_INFO_ID = USER_INFO.USER_INFO_ID  ) AS USER_SCORE GROUP BY USER_SCORE.USER_INFO_ID;"
        cursor.execute(sql)
        data = cursor.fetchall()
        print("응시자별 채점 결과: ")
        for row in data:
            print(f"{row[1]}:  {row[2]}")
            

        sql = "SELECT COUNT(USER_SCORE.USER_INFO_ID), SUM(USER_SCORE.ANSWER_SCORE), ROUND(SUM(USER_SCORE.ANSWER_SCORE)/COUNT(USER_SCORE.USER_INFO_ID),2) FROM (SELECT USER_ANSWER_INFO.USER_INFO_ID, USER_INFO.USER_NAME, ANSWER_INFO.ANSWER_SCORE FROM USER_ANSWER_INFO INNER JOIN ANSWER_INFO ON ANSWER_INFO.ANSWER_INFO_ID = USER_ANSWER_INFO.ANSWER_INFO_ID  INNER JOIN USER_INFO ON USER_ANSWER_INFO.USER_INFO_ID = USER_INFO.USER_INFO_ID  ) AS USER_SCORE;"
        cursor.execute(sql)
        data = cursor.fetchall()
        print(f"과목 평균 점수: {data[0][2]*2}")
        




conn = connect_database()

# 초기값
end_sign = 'c'

test_start(end_sign, conn)

grading(conn)


        






# if __name__ == "__main__" :
