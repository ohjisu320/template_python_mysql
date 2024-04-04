from test_program_sub import connect_database, test_create, test_start, grading

conn = connect_database()
answer_type = int(input("문제 유형을 입력하세요 (N지 선다형): "))
quest_type = int(input("문제 수를 입력하세요 (N개 문항) : "))
test_create(conn, answer_type, quest_type)
    
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

