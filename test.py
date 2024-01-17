# 입력 개수만큼 3, 7의 배수 찾기

def isMultipleOf3oro7(num):
    return (num%3==0) or (num%7==0)

def getMultipleOf3or7(n):
    cnt=0
    num=1
    while (cnt != n):
        if(isMultipleOf3oro7(num)):
            cnt+=1
            print(num, end=" ")
        num+=1

getMultipleOf3or7(10)
