#### Share
- [ERDexcel](https://docs.google.com/spreadsheets/d/1EACJj0UoUFynZ7n44fwx1CS5yjQNbe9g8iXA7fQaU9Q/edit?usp=sharing)
- [ERDcloud](https://www.erdcloud.com/d/Pr32JC22AHKXTFnrt)

#### Members

|WORKS|MEMBER|
|--|--|
|시험출제 프로그램 작성|명준
|시험응시 프로그램 작성|지수
|시험결과 도출|지수

##### 사전 접근 고민
######  [테이블 분리] - 문제정보/선택지정보/응시자답변정보/응시자정보
  - 문제정보: 문제정보ID(PK), 문제(내용), 문제번호
  - 선택지정보: 선택지정보ID(PK), 문제정보ID(FK), 선택지(내용), 선택지번호, 선택지점수
  - 응시자답변정보: 응시자답변정보ID(PK), 응시자정보ID(FK), 선택지정보ID(FK)
  - 응시자정보: 응시자정보ID(PK), 응시자이름
###### [과정]
    1) 출제 과정 : 입력받은 문제, 문제번호(FOR문변수), 문제정보ID 문제정보테이블에 INSERT -> 입력받은 선택지, 선택지번호(FOR문변수), 선택지정보ID 선택지정보테이블에 INSERT -> 입력받은 정답과 일치하는 값에 선택지점수 UPDATE
    2) 응시 과정 :  입력받은 응시자 이름, 응시자정보ID 응시자정보테이블에 INSERT -> 문제정보/선택지정보 테이블에서 문제번호와 문제, 선택지번호와 선택지 출력 -> 응시자에 입력받은 정보와 일치하는 선택지정보테이블-선택지의 선택지정보ID, 응시자정보ID를 응시자답변정보에 INSERT
    3) 채점 과정 : 응시자답변정보-응시자정보ID와 일치하는 응시자정보-응시자정보ID의 응시자 이름, 응시자답변정보-선택지정보ID와 일치하는 선택지정보-선택지정보ID의 점수 출력

##### 난이도 있던 QUERY
```
sql = "SELECT USER_SCORE.USER_INFO_ID, USER_SCORE.USER_NAME, SUM(USER_SCORE.ANSWER_SCORE) FROM (SELECT USER_ANSWER_INFO.USER_INFO_ID, USER_INFO.USER_NAME, ANSWER_INFO.ANSWER_SCORE FROM USER_ANSWER_INFO INNER JOIN ANSWER_INFO ON ANSWER_INFO.ANSWER_INFO_ID = USER_ANSWER_INFO.ANSWER_INFO_ID  INNER JOIN USER_INFO ON USER_ANSWER_INFO.USER_INFO_ID = USER_INFO.USER_INFO_ID  ) AS USER_SCORE GROUP BY USER_SCORE.USER_INFO_ID;"
```
채점 과정에서 응시자의 점수를 출력하는 과정

##### NoSQL과의 차이점
- 쿼리문 안에서 원하는 정보만 빼낼 수 있어서 PYTHON 코드자체는 간결했다.

#### DDL

<details>
	<summary>
		<bold>CREATE TABLE</bold>
	</summary>

```
CREATE TABLE `QUEST_INFO` (
	`QUEST_INFO_ID`	VARCHAR(50)	NOT NULL,
	`QUEST`	VARCHAR(255)	NULL,
	`QUEST_NUMBER`	DECIMAL(20,0)	NULL
);

CREATE TABLE `ANSWER_INFO` (
	`ANSWER_INFO_ID`	VARCHAR(50)	NOT NULL,
	`QUEST_INFO_ID`	VARCHAR(50)	NOT NULL,
	`ANSWER`	VARCHAR(255)	NULL,
	`ANSWER_NUMBER`	DECIMAL(20,0)	NULL,
	`ANSWER_SCORE`	DECIMAL(20,0)	NULL
);

CREATE TABLE `USER_ANSWER_INFO` (
	`USER_ANSWER_INFO_ID`	VARCHAR(50)	NOT NULL,
	`USER_INFO_ID`	VARCHAR(50)	NOT NULL,
	`ANSWER_INFO_ID2`	VARCHAR(50)	NOT NULL
);

CREATE TABLE `USER_INFO` (
	`USER_INFO_ID`	VARCHAR(50)	NOT NULL,
	`USER_NAME`	VARCHAR(255)	NULL
);

ALTER TABLE `QUEST_INFO` ADD CONSTRAINT `PK_QUEST_INFO` PRIMARY KEY (
	`QUEST_INFO_ID`
);

ALTER TABLE `ANSWER_INFO` ADD CONSTRAINT `PK_ANSWER_INFO` PRIMARY KEY (
	`ANSWER_INFO_ID`,
	`QUEST_INFO_ID`
);

ALTER TABLE `USER_ANSWER_INFO` ADD CONSTRAINT `PK_USER_ANSWER_INFO` PRIMARY KEY (
	`USER_ANSWER_INFO_ID`,
	`USER_INFO_ID`,
	`ANSWER_INFO_ID2`
);

ALTER TABLE `USER_INFO` ADD CONSTRAINT `PK_USER_INFO` PRIMARY KEY (
	`USER_INFO_ID`
);

ALTER TABLE `ANSWER_INFO` ADD CONSTRAINT `FK_QUEST_INFO_TO_ANSWER_INFO_1` FOREIGN KEY (
	`QUEST_INFO_ID`
)
REFERENCES `QUEST_INFO` (
	`QUEST_INFO_ID`
);

ALTER TABLE `USER_ANSWER_INFO` ADD CONSTRAINT `FK_USER_INFO_TO_USER_ANSWER_INFO_1` FOREIGN KEY (
	`USER_INFO_ID`
)
REFERENCES `USER_INFO` (
	`USER_INFO_ID`
);
```

</details>


## python_mysql
#### Main package
- java:17
- mysql:8

#### CLI with Dockerfile and compose.xml : duration 150.4s
```
# --project-name is docker container name
~$ docker-compose --project-name python_mysql up -d --build
```
#### samples
- [samples/python_mysql.py](./samples/python_mysql.py)

#### database infors
+ user='cocolabhub',
+ password='cocolabhub',
+ db='python_mysql'



