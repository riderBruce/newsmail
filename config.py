SEARCH_KEY_ROWS = [
    ['\"현대건설\" 안전 사고', '-현대건설기계 -분양 -배구 -주가 -개발사업 -시연회 -스마트 -로봇 -인공지능 -AI'],
    ['\"현대건설\" 환경 사고', '-현대건설기계 -분양 -배구 -주가 -개발사업 -시연회 -스마트 -로봇 -인공지능 -AI -현대해상'],
    ['\"현대건설\" 공정거래', '-현대건설기계'],
    ['\"현대건설\" 하도급 갑질', '-현대건설기계'],
    ['\"현대건설\" 불법 하도급', '-현대건설기계'],
    ['\"현대건설\" 재하도', '-현대건설기계'],
    ['\"현대건설\" 체불', '-현대건설기계 -배구'],
    ['\"현대건설\" 본드콜', '-현대건설기계 -배구'],
    ['\"현대건설\" 고용노동부', '-현대건설기계 -분양 -배구 -주가 -개발사업 -시연회 -스마트 -로봇 -인공지능 -AI'],
    ['\"현대건설\" 국토교통부', '-현대건설기계 -분양 -배구 -주가 -개발사업 -시연회 -스마트 -로봇 -인공지능 -AI'],
    ['\"현대건설\" ESG', '-AI -현대건설기계'],
    ['현대건설 | 현대엔지니어링 \"지배구조\" ', '-AI -현대건설기계'],
    ['\"현대건설\" 석탄', '-현대건설기계 -대륙간거래소'],
    ['\"현대건설\"', '-현대건설기계 -분양 -배구 -스마트 -주가 -로봇 -인공지능 -AI -양효진 -퍼블릭 -대륙간거래소 -통일'],
    # 검색어 글자수 제한 있어서 더이상 못 늘림  -> 현대건설 쌍따움표 추가
    ['고용노동부 건설 현장', '-현대건설기계 -분양 -배구 -주가 -개발사업 -시연회 -스마트 -로봇 -인공지능 -AI'],
    ['국토교통부 건설 현장', '-현대건설기계 -분양 -배구 -주가 -개발사업 -시연회 -스마트 -로봇 -인공지능 -AI'],
    ['국토교통부 건설업', '-현대건설기계 -분양 -배구 -주가 -개발사업 -시연회 -스마트 -로봇 -인공지능 -AI'],
    ['"Hyundai Engineering and Construction"', '-AI -HHI -현대건설기계 -배구 -현대중공업'],
    ['지방고용노동청 건설', '-현대건설기계 -분양 -배구 -주가 -개발사업 -시연회 -스마트 -로봇 -인공지능 -AI'],
    ['노동청 건설', '-현대건설기계 -분양 -배구 -주가 -개발사업 -시연회 -스마트 -로봇 -인공지능 -AI'],
    ['서울 국토청', '-현대건설기계 -분양 -배구 -주가 -개발사업 -시연회 -스마트 -로봇 -인공지능 -AI'],
    ['원주 국토청', '-현대건설기계 -분양 -배구 -주가 -개발사업 -시연회 -스마트 -로봇 -인공지능 -AI'],
    ['대전 국토청', '-현대건설기계 -분양 -배구 -주가 -개발사업 -시연회 -스마트 -로봇 -인공지능 -AI'],
    ['부산 국토청', '-현대건설기계 -분양 -배구 -주가 -개발사업 -시연회 -스마트 -로봇 -인공지능 -AI'],
    ['익산 국토청', '-현대건설기계 -분양 -배구 -주가 -개발사업 -시연회 -스마트 -로봇 -인공지능 -AI'],
    ['지방국토관리청', '-현대건설기계 -분양 -배구 -주가 -개발사업 -시연회 -스마트 -로봇 -인공지능 -AI'],
    ['국토청 건설', '-현대건설기계 -분양 -배구 -주가 -개발사업 -시연회 -스마트 -로봇 -인공지능 -AI'],
]

GOOGLE_KEYS = [
    '"Hyundai Engineering and Construction"',
    '"Hyundai Engineering & Construction"',
    '"Hyundai E&C"',
    '"HDEC"',
]

# 최종 제목에서 제외하는 키워드 :

# 제목 회피 1차
EXCEPTION_KEY_LEVEL_0 = [
    "사설", "증권",
    "브리핑", "주요기사", "1면", "기고", "칼럼", "재송", "주요공시", "입찰동향", "입낙찰",
    "건설주", "株", "주가", "그룹주", "수혜주", "증권", "금융투자", "코스닥", "코스피", "증시",
    "인사", "동정",
    "일정", "리뷰", "눈길", "비즈&", "헤경",
    "홍보실장", "부고", "부음", "별세", "(종합)", "검찰에 묻다", "결혼",
    "개찰현황", "오늘의 경기", "내일의 경기", "V리그",
    "아이유", "집수리", "수소", "하모의 숲",
]

# 제목 + 내용 회피 2차 (제목 등장시 삭제, 내용에 1회이상 등장시 삭제)
EXCEPTION_KEY_LEVEL_1 = [
    "현대건설기계", "HHI",
    "임상영", "이도희",
    "UAM",
]
# 제목 + 내용회피 3차 (제목 등장시 삭제, 내용에 5회 이상 등장시 삭제)
EXCEPTION_KEY_LEVEL_2 = [
    "배구", "양효진", "황민경", "김연경", "박사랑", "이현지", "문슬기", "이윤정", "야스민", "라셈", "이다현", "김주향", "이다영", "이재영",
    "라셈", "강성형", "유진형", "허수봉", "캣벨", "황연주", "치어리더", "김도아",
    "시즌", "득점", "우승", "선수", "결승", "드래프트", "응원단", "리그", "서브", "스파이크", "블로킹",
    "대표팀", "태극마크", "MVP", "리시브", "GS칼텍스", "캐피탈", "대뷔", "기업은행", "개막", "흥국생명",
    "수주소식", "분양", "힐스테이트", "Hillstate", "청약", "상가", "오피스텔", "리모델링", "시행사",
    "타운하우스", "웃돈", "힐스 에비뉴", "모델하우스", "펜트하우스",
    "컨소시움 단지", "재개발", "역세권", "MICE",
    "GTX", "신도시", "부동산",
    "스타트업", "경력직", "신입", "경력", "서류접수", "채용", "산학협력", "취업", "공채",
    "현대해상", "건설기계", "건설장비", "현대산업개발", "현대중공업", "삼우", "저축은행",
    "포토",
    "방역", "허리케인", "납품대금",
    "메리츠", "메가박스",
    "미술작품", "퍼블릭", "시진핑", "AI", "인공지능", "로봇",
]

# "재건축", "시공사", "시공권", "정비사업",

EXCEPTION_KEYS_ALL = EXCEPTION_KEY_LEVEL_0 + EXCEPTION_KEY_LEVEL_1 + EXCEPTION_KEY_LEVEL_2

BLACK_LIST_MEDIAS = [
    "여성소비자신문",
    "단디뉴스",
    "뉴스1",
    "OSEN",
    "스포츠서울",
    "스포츠조선",
    "데일리스포츠한국",
    "미디어스",
    "오토타임즈",
    "발리볼코리아",
    "더스파이크",
    "스포탈코리아",
    "NSP통신",
    "굿모닝충청",
    "서울문화투데이",
    "마이데일리",
    "아이뉴스24",
]

MAJOR_MEDIAS = [
    '경향신문', '국민일보', '뉴스1', '뉴시스', '대전일보', '동아일보', '문화일보', '서울신문', '세계일보', '연합뉴스', '조선일보', '중앙일보', '한겨레', '한국일보',
    '매일경제', '머니투데이', '비즈니스워치', '서울경제', '아시아경제', '이데일리', '조선비즈', '파이낸셜뉴스', '한국경제', '헤럴드경제', '노컷뉴스', '뉴스타파', '더팩트',
    '데일리안', '머니S', '아이뉴스24', '오마이뉴스', '쿠키뉴스', '프레시안', 'JTBC', 'KBS', 'MBC', 'MBN', 'SBS', 'YTN', '채널A', '한국경제TV',
]
