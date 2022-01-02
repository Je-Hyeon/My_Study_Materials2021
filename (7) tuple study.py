# 튜플의 사용
## 리스트에 튜플 정보를 저장하고, 반복문을 튜플로 돌린다

example_text = "Hello my name is jehyeon, i'm from Korea and, i am student from SKKU major in globaleconomics"
words_list = example_text.split()

list_a = list()
for word in words_list:
    list_a.append(( len(word), word))

print(list_a)

list_a.sort(reverse= True)   # 단어 길이 별로 정렬했다.

print(list_a)

list_b = list()

for len, word in list_a:  # 길이 나타내는 숫자 버리고, 단어만 리스트에 저장
    list_b.append(word)

print(list_b)