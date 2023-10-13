


for i in ['업종', '대표자명', '홈페이지', '기업주소', '사업내용', '바로가기', '기업비전']:
    if '기업주소' in i:
        cpn_add_index = int(['업종', '대표자명', '홈페이지', '기업주소', '사업내용', '바로가기', '기업비전'].index(i)) + 1
        print('//*[@id="content"]/div/div[2]/div[1]/dl[1]/dd[' + str(cpn_add_index) + ']')