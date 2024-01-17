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

    # print([ppii.bstr for ppii in PiList])
    pi_str_list=[]
    for pi in PiList:
        pi_str_list.append(pi.getbstr())
    pi_str_list.sort()
    answer=pi_str_list

    # finding EPI
    answer.append("EPI")
    # make pi_chart
    pi_chart=[]
    epi_str_list=[]
    #make pi_chart
    for pi_idx, pi in enumerate(PiList):
        pi_chart.append([])
        for i in range(len(mintermList)):
            pi_chart[pi_idx].append(False)

    for mt_idx, mt in enumerate(mintermList):
        for pi_idx, pi in enumerate(PiList):
            if mt in pi.terms:
                pi_chart[pi_idx][mt_idx]= True

    # find epi
    for mt_idx, mt in enumerate(mintermList):
        cnt=0
        str=[]
        for pi_idx, pi in enumerate(PiList):
            if pi_chart[pi_idx][mt_idx]==True:
                cnt+=1
                str.append(pi.bstr)
        if cnt==1:
            str=''.join(str)
            if not (str in epi_str_list):
                epi_str_list.append(str)

    epi_str_list.sort()
    answer+=epi_str_list
    # 2->'-'
    for idx, str in enumerate(answer):
        str = list(str)
        for i in range(len(str)):
            if str[i]=='2':
                str[i]='-'
        answer[idx]=''.join(str)
    return answer

# 여기서부터 시작

minterm = [4,7,0,1,2,3,10,11,12]
print(solution(minterm))
