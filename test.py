rec_title = ['가구', '실내건축 & 인테리어 공사팀 직원 채용( 신입 및 경력직 )','LX하우시스 공식대리점 건일테크 인테리어 컨설턴트 모집','아파트멘터리(주) 홈인테리어 공무 담당 채용','실내인테리어 공사부 경력직 모집']
cpn_kind = []

for i in rec_title:
    if '인테리어' in i:
        if (('시공' in i or '현장' in i) or '공사' in i) and (('설계' in i or '디자' in i) or '컨설턴트' in i):
            cpn_kind.append('종합 인테리어')
        elif (('시공' in i or '현장' in i) or '공사' in i):
            cpn_kind.append('인테리어 시공')
        elif (('설계' in i or '디자' in i) or '컨설턴트' in i):
            cpn_kind.append('인테리어 디자인')
        else:
            cpn_kind.append('확인 필요!')
    elif '가구' in i:
        cpn_kind.append('가구 브랜드')
    elif '침구' in i:
        cpn_kind.append('가구 브랜드')
    else:
        cpn_kind.append('확인 필요!')


print(cpn_kind)