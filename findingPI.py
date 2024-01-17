class Implicant:
    def __init__(self, terms, bstr, checked=False):
        self.terms = terms # 튜플
        self.bstr = bstr
        self.checked = checked
        self.onecnt=0 # 1의 개수
        for char in bstr:
            if(char=='1'):
                self.onecnt+=1

    def getterms(self):
        return self.terms
    def getbstr(self):
        return self.bstr
    def isChecked(self): # if checked == False -> PI
        return self.checked

    #def canCombine(self, another): 이건 그냥 바로 구현하는게 나을듯
        # if 1의 개수 차이가 1이고 지금 단계에서 하이픈 개수가 일치할 때 slef.checked=True, return Implicant(keys,bstr"1020",False) -> after[1개수]에 넣어

def solution(minterm):
    before=[]
    after=[]
    PiList=[]

    mintermList = minterm[2:] # 중복되는 원소 제거(?)
    n=minterm[0] # 변수개수
    # makeBefore
    for i in range(n+1):
        before.append([])
    for mt in mintermList:
        string_bynary_minterm = format(mt,'b')
        # 변수 개수만큼 앞에 '0' 붙여줘서 길이 맞추기
        for iter in range(n-len(string_bynary_minterm)):
            string_bynary_minterm = '0'+string_bynary_minterm
        cnt=0
        for char in string_bynary_minterm:
            if(char=='1'):
                cnt+=1
        before[cnt].append(Implicant((mt,),string_bynary_minterm,False))

    answer=[]
    while True:
        # makeAfter
        for i in range(len(before)-1):
            after.append([])
        if (len(after)==0):
            break
        for i in range(n):
            for j in range(len(before[i])):
                prevI=before[i][j]
                for k in range(len(before[i+1])):
                    nextI=before[i+1][k]

                    cnt=0 # 다른 개수
                    idx=-1 #다른곳 idx
                    str="" # 다르다면 합쳣을때 생기는 bstr
                    for index, char in enumerate(prevI.bstr):
                        if char!=nextI.bstr[index]:
                            cnt+=1
                            idx=index
                    if(cnt==1):
                        str=prevI.getbstr()
                        str = list(str)
                        str[idx] = '2'
                        str = ''.join(str)
                        prevI.checked=True
                        nextI.checked=True
                        if str in answer:
                            continue
                        answer.append(str)
                        I = Implicant(prevI.terms+nextI.terms,str,False)
                        ones=I.onecnt
                        after[ones].append(I)
        for ImplicantList in before:
            for i in range(len(ImplicantList)):
                if (ImplicantList[i].isChecked()==False):
                    PiList.append(ImplicantList[i])
        before=after
        after=[]
        n-=1

    for ImplicantList in before:
        for i in range(len(ImplicantList)):
            if (ImplicantList[i].isChecked()==False):
                PiList.append(ImplicantList[i])

    # finding PI
    pi_str_list=[]
    for pi in PiList:
        pi_str_list.append(pi.getbstr())
    pi_str_list.sort()
    for idx, pi_str in enumerate(pi_str_list):
        pi_str = list(pi_str)
        for i in range(len(pi_str)):
            if pi_str[i]=='2':
                pi_str[i]='-'
        pi_str_list[idx]=''.join(pi_str)
    answer=pi_str_list
    return answer

# 여기서부터 시작

minterm=[6,32,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]
print(solution(minterm))
