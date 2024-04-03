
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

    # mysql로 저장
    with conn.cursor() as cursor:
        # Create
        sql = "INSERT INTO QUEST_INFO (QUEST_INFO_ID,QUEST, QUEST_NUMBER) VALUES (%s, %s, %s)"
        cursor.execute(sql, (f"QUESTION_{x+1}", QUEST, x+1))
        conn.commit()

    
    print("선택지: ")
    for y in range(answer_type) :
        input(f"{y+1}. ")
        # mysql로 저장






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

    with conn.cursor() as cursor:
        # Create
        sql = "INSERT INTO TableName (pk_id,column1, column2) VALUES (%s, %s, %s)"
        cursor.execute(sql, (1, 'value1', 'value2'))
        conn.commit()
