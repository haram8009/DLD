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

def findPI(n, PiList, mintermList):
    # makeBefore
    before=[]
    after=[]
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

    foundlist=[]
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
                        if str in foundlist:
                            continue
                        foundlist.append(str)
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

    pi_str_list=[]
    for pi in PiList:
        pi_str_list.append(pi.getbstr())
    pi_str_list.sort()
    return pi_str_list, PiList, mintermList


def findEPI(PiList, mintermList):
    pi_chart = makePiChart(PiList, mintermList)
    epi_str_list=[]
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

    # fix PiList, mintermList
    for str in epi_str_list:
        for I in PiList:
            if (I.getbstr()==str):
                for mt in I.getterms():
                    if mt in mintermList:
                        mintermList.remove(mt)
                PiList.remove(I)
    return epi_str_list, PiList, mintermList

def eliminateDominatingColumns(PiList, mintermList):
    # makePiChart
    pi_chart = makePiChart(PiList, mintermList)

    dic = {}
    # 민텀마다 체크 몇개인지 세기, key=mt '인덱스' in mintermList, value=체크개수
    # make dic
    for mt_idx, mt in enumerate(mintermList):
        for i in range(len(PiList)):
            if pi_chart[i][mt_idx] == True:
                if dic.get(mt_idx) == None:
                    dic[mt_idx] =1
                else:
                    dic[mt_idx] += 1

    def isDominating(mt, next_mt):
        for i in range(len(PiList)):
            if pi_chart[i][next_mt] == True:
                if pi_chart[i][mt] == False:
                    return False
        return True

    dominatingMtList=[]
    # 돌아가면서 나보다 체크 적은것만 비교해서 내가 dominating 하는지 여부 확인 == make dominatingMtList
    # mt는 mintermList의 '인덱스'
    for mt, cnt in dic.items():
        for next_mt, next_cnt in dic.items():
            if(mintermList[mt]==mintermList[next_mt]):
                continue
            if(cnt>next_cnt):
                if isDominating(mt, next_mt):
                    dominatingMtList.append(mintermList[mt])
    # mintermList 에서 dominating하는 mt 지우기 == eliminateDominatingColumns
    for mt in dominatingMtList:
        if mt in mintermList:
            mintermList.remove(mt)
    return PiList, mintermList


def eliminateDominatedRows(PiList, mintermList):
    def isDominated(pi, next_pi):
        for mt in pi.getterms():
            if not mt in next_pi.getterms():
                return False
        return True

    dominatedPiList=[]
    # 돌아가면서 나보다 체크 많은것만 비교해서 내가 dominated 하는지 여부 확인 == make dominatedPiList
    for pi_idx, pi in enumerate(PiList):
        for next_pi_idx, next_pi in enumerate(PiList):
            if (pi==next_pi):
                continue
            if (len(pi.getterms()) < len(next_pi.getterms())):
                if isDominated(pi, next_pi):
                    dominatedPiList.append(pi)
    # PiList 에서 dominated 한 pi 지우기 == eliminateDominatedRows
    for pi in dominatedPiList:
        if pi in PiList:
            PiList.remove(pi)
    return PiList, mintermList

def chooseInterchangeable(PiList, mintermList):
    # PiList[0]을 임의로 결정
    choosedInterchangeable = PiList[0]
    str = choosedInterchangeable.getbstr()
    # fix PiList, mintermList
    covered_list=[]
    for mt in choosedInterchangeable.getterms():
        if mt in mintermList:
            # choosedInterchangeable이 커버하는 minterm을 같이 커버하는 다른 pi도 PiList에서 삭제
            for pi in PiList:
                if mt in pi.getterms():
                    if not pi in covered_list:
                        covered_list.append(pi)
            # 해당 minterm 삭제
            mintermList.remove(mt)
    for pi in covered_list:
        PiList.remove(pi) # pi에는 choosedInterchangeable도 포함되어있음
    return [str], PiList, mintermList


def makePiChart(PiList, mintermList):
    pi_chart=[]
    for pi_idx, pi in enumerate(PiList):
        pi_chart.append([])
        for i in range(len(mintermList)):
            pi_chart[pi_idx].append(False)
    for mt_idx, mt in enumerate(mintermList):
        for pi_idx, pi in enumerate(PiList):
            if mt in pi.getterms():
                pi_chart[pi_idx][mt_idx]= True
    return pi_chart

def solution(minterm):
    answer=[]
    PiList=[]
    mintermList = minterm[2:]
    n=minterm[0] # 변수개수

    # finding PI
    pi_str_list, PiList, mintermList = findPI(n, PiList, mintermList)
    answer+=pi_str_list

    # finding EPI
    answer.append("EPI")
    epi_str_list, PiList, mintermList = findEPI(PiList, mintermList)
    answer+=epi_str_list

    answer.append("secondery EPI")
    while len(mintermList)>0 :
        # eliminateDominatingColumns
        PiList, mintermList = eliminateDominatingColumns(PiList, mintermList)
        # eliminateDominatedRows
        PiList, mintermList = eliminateDominatedRows(PiList, mintermList)
        # find secondery EPI
        secondery_epi_str_list=[]
        secondery_epi_str_list, PiList, mintermList = findEPI(PiList, mintermList)

        if len(secondery_epi_str_list)>0: # secondery_epi 발생
            secondery_epi_str_list+=['<-secondery_epi']
            answer+=secondery_epi_str_list
        else : # secondery_epi가 생기지 않으면 chooseInterchangable
            secondery_epi_str_list, PiList, mintermList = chooseInterchangeable(PiList, mintermList)
            secondery_epi_str_list+=['<-chooseInterchangable']
            answer+=secondery_epi_str_list

    # print : 2->'-'
    for idx, str in enumerate(answer):
        str = list(str)
        for i in range(len(str)):
            if str[i]=='2':
                str[i]='-'
        answer[idx]=''.join(str)
    return answer


# minterm = [4,11 ,0,2,5,6,7,8,10,12,13,14,15]
minterm = [4,13 ,0,2,3,4,5,6,7,8,9,10,11,12,13]
# minterm = [4,6, 2,3,7,9,11,13]
print(solution(minterm))
