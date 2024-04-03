
import pymysql




list_dict_ANSWER = [
    {
    'ANSWER_INFO_ID':"ANSWER_INFO_1"
    , 'QUEST_INFO_ID':'QUEST_INFO_1'
    , 'ANSWER' : 'Guido van Rossum'
    , 'ANSWER_NUMBER' : 1
    , 'ANSWER_SCORE' : 10
    }
    , {
    'ANSWER_INFO_ID':"ANSWER_INFO_2"
    , 'QUEST_INFO_ID':'QUEST_INFO_1'
    , 'ANSWER' : 'James Gosling'
    , 'ANSWER_NUMBER' : 2
    , 'ANSWER_SCORE' : 0
    }
    , {
    'ANSWER_INFO_ID':"ANSWER_INFO_3"
    , 'QUEST_INFO_ID':'QUEST_INFO_1'
    , 'ANSWER' : 'Dennis Ritchie'
    , 'ANSWER_NUMBER' : 3
    , 'ANSWER_SCORE' : 0
    }
    ,{
    'ANSWER_INFO_ID':"ANSWER_INFO_4"
    , 'QUEST_INFO_ID':'QUEST_INFO_1'
    , 'ANSWER' : 'Brendan Eich'
    , 'ANSWER_NUMBER' : 4
    , 'ANSWER_SCORE' : 0
    }
]

# 데이터베이스 연결 설정
conn = pymysql.connect(
    host='python_mysql_mysql',  # 컨테이너 이름 또는 IP
    user='cocolabhub',
    password='cocolabhub',
    db='python_mysql',  # 데이터베이스 이름
    charset='utf8mb4')

x=1
quest_type = 4
answer_type = 2
while True : 
#     "USER_INFO_1"[10:]
# 1
# int("USER_INFO_1"[10:])
# 1
    USER_NAME = input("응시자 이름을 입력하세요: ")
    with conn.cursor() as cursor:
        # Read
        sql = "SELECT USER_INFO_ID FROM USER_INFO"
        cursor.execute(sql)
        data = cursor.fetchall()
        for row in data:
            last = row

    
    USER_INFO_ID = "USER_INFO_"+str(int(last[0][10:])+1)



    # mysql로 저장
    with conn.cursor() as cursor:
        # Create
        sql = "INSERT INTO USER_INFO (USER_INFO_ID,USER_NAME) VALUES (%s, %s)"
        cursor.execute(sql, (USER_INFO_ID, USER_NAME))
        conn.commit()
    x = x+1
    print("문제를 풀어주세요")

    for x in range(len(list_dict_ANSWER)) : # 임의의 값
        with conn.cursor() as cursor:
            # Read
            sql = "SELECT QUEST_NUMBER, QUEST FROM QUEST_INFO"
            cursor.execute(sql)
            data = cursor.fetchall()
            for row in data:
                print(str(row[0])+". "+str(row[1]))

                with conn.cursor() as cursor:
                    # Read
                    sql = "SELECT QUEST_NUMBER, QUEST FROM QUEST_INFO"
                    cursor.execute(sql)
                    data = cursor.fetchall()
                answer_count = 0
                x = 0
                while True : 
                    if list_dict_ANSWER[x]["QUEST_INFO_ID"]=="QUEST_INFO_"+str(x+1) : 
                        answer_count = answer_count+1
                        x = x+1
                        pass
                    else :
                        break
                for y in range(answer_count) :
                    print(str(list_dict_ANSWER[x]["ANSWER_NUMBER"])+". "+str(list_dict_ANSWER[x]["ANSWER"]))


    


        
        






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
