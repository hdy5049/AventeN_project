import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import platform
import os
from matplotlib import font_manager, rc
from collections import Counter

# ==========================================
# [설정] 파일 목록
# ==========================================
FILE_NAMES = [
    "avante_n_reviews_cleaned.csv",
    "avante_n_reviews_cleaned2.csv",
    "avante_n_reviews_cleaned3.csv",
    "avante_n_reviews_cleaned4.csv",
    "avante_n_reviews_cleaned5.csv",
    "avante_n_reviews_cleaned6.csv"
]

# ==========================================
# [설정] 한글 폰트 (그래프 깨짐 방지)
# ==========================================
system_name = platform.system()
if system_name == 'Windows':
    rc('font', family='Malgun Gothic')
elif system_name == 'Darwin':
    rc('font', family='AppleGothic')
else:
    rc('font', family='NanumGothic')
plt.rcParams['axes.unicode_minus'] = False

# ==========================================
# [키워드 설정]
# ==========================================
COMPETITORS = {
    "제네시스 G70": ["G70", "지칠공", "칠공", "제네시스"],
    "기아 스팅어": ["스팅어", "마팅어", "기아"],
    "BMW (3시리즈/M)": ["비엠", "BMW", "3시리즈", "M2", "M3", "M4"],
    "머스탱/카마로": ["머스탱", "카마로", "미국차", "머슬카"],
    "폭스바겐 골프 GTI": ["골프", "GTI", "폭스바겐"]
}

# 경쟁차 오너 차단 리스트
COMPETITOR_OWNER_BAN_LIST = [
    "G70 탑니다", "G70 샀", "G70 오너", "G70 출고", "G70 운용",
    "스팅어 탑니다", "스팅어 샀", "스팅어 오너", "스팅어 출고", "스팅어 운용",
    "3시리즈 탑니다", "3시리즈 오너", "BMW 오너", "골프 샀", "골프 출고",
    "머스탱 탑니다", "카마로 탑니다", "제 차는 G70", "제 차는 스팅어"
]

# 찐 오너 인증 (필수 포함)
REAL_OWNER_PROOF = [
    "제 차", "내 차", "제차", "내차", "자차", "세컨카", "데일리카",
    "출고", "계약", "인수", "기변", "대차", "가져왔", "넘어왔", "바꿨", "구입", "구매",
    "타보니", "타보니까", "타면서", "운행중", "운용중", "길들이기", "키로수", "km",
    "고급유", "서킷", "인제", "와인딩", "공도", "방지턱", "팝콘"
]

# 아반떼N 매력 포인트
CN7N_STRENGTHS = [
    "재미", "펀카", "코너", "핸들링", "팝콘", "배기음", "가성비", "미션", "DCT",
    "거동", "랩타임", "전륜", "끝판왕", "장난감", "빠르다", "따다", "이긴다", "압살",
    "만족", "행복", "웃음", "지린다", "미쳤다", "최고"
]

EXCLUDE_CONTEXT = ["전기차", "아이오닉", "EV6", "테슬라", "하브", "하이브리드", "주유", "연비"]


def visualize_results(comp_df, strength_counts):
    """분석 결과를 그래프로 시각화하는 함수"""
    plt.figure(figsize=(14, 6))

    # 1. 경쟁 차종 언급 빈도 (Bar Chart)
    plt.subplot(1, 2, 1)
    if not comp_df.empty:
        comp_counts = comp_df['경쟁차종'].value_counts()
        sns.barplot(x=comp_counts.index, y=comp_counts.values, palette='viridis')
        plt.title('아반떼N 오너들이 가장 많이 비교하는 차종', fontsize=14, fontweight='bold')
        plt.xlabel('경쟁 차종')
        plt.ylabel('유효 비교 리뷰 수')
        plt.xticks(rotation=15)

        # 수치 표시
        for i, v in enumerate(comp_counts.values):
            plt.text(i, v + 0.5, str(v), ha='center', fontweight='bold')

    # 2. 아반떼N 매력 키워드 Top 10 (Bar Chart)
    plt.subplot(1, 2, 2)
    if strength_counts:
        top_strengths = strength_counts.most_common(10)
        words = [x[0] for x in top_strengths]
        counts = [x[1] for x in top_strengths]

        sns.barplot(x=counts, y=words, palette='magma')
        plt.title('오너들이 꼽은 아반떼N 핵심 매력 (Top 10)', fontsize=14, fontweight='bold')
        plt.xlabel('언급 빈도')

    plt.tight_layout()
    plt.show()


def analyze_reviews():
    print("🚀 데이터 로딩 중...")

    df_list = []
    for file in FILE_NAMES:
        if os.path.exists(file):
            try:
                temp_df = pd.read_csv(file)
                df_list.append(temp_df)
            except:
                pass

    if not df_list:
        print("❌ 데이터가 없습니다.")
        return

    df = pd.concat(df_list, ignore_index=True)
    df = df.drop_duplicates(subset=['Review'], keep='first')
    df['Review'] = df['Review'].fillna('')

    # 노이즈 제거
    mask_exclude = df['Review'].str.contains('|'.join(EXCLUDE_CONTEXT), case=False)
    df = df[~mask_exclude]

    print(f"✅ 통합 완료 (분석 대상: {len(df):,}개)")
    print("=" * 60)

    comparison_rows = []  # 경쟁차 비교
    general_reviews = []  # 순수 아반떼N 후기
    strength_counter = Counter()  # 매력 포인트 카운팅용

    for _, row in df.iterrows():
        text = row['Review']
        likes = row.get('Likes', 0)

        # 1. 찐 오너 인증 (없으면 패스)
        if not any(k in text for k in REAL_OWNER_PROOF):
            continue

        # 2. 경쟁차 오너 차단 (있으면 패스)
        if any(k in text for k in COMPETITOR_OWNER_BAN_LIST):
            continue

        # 3. 분류: 경쟁차 언급이 있는가?
        mentioned_competitor = None
        for car_name, keywords in COMPETITORS.items():
            if any(k in text for k in keywords):
                mentioned_competitor = car_name
                break

        # 4. 매력 포인트 카운팅 (시각화용)
        for strength in CN7N_STRENGTHS:
            if strength in text:
                strength_counter[strength] += 1

        if mentioned_competitor:
            # [비교 리뷰]
            if any(k in text for k in CN7N_STRENGTHS):
                comparison_rows.append({
                    "경쟁차종": mentioned_competitor,
                    "좋아요": likes,
                    "내용": text
                })
        else:
            # [일반 리뷰] (경쟁차 언급 X)
            if any(k in text for k in CN7N_STRENGTHS) and len(text) > 30:
                general_reviews.append({
                    "좋아요": likes,
                    "내용": text
                })

    # ==========================================
    # 결과 텍스트 출력
    # ==========================================
    pd.set_option('display.max_colwidth', 100)

    # 1. 경쟁차 비교
    comp_df = pd.DataFrame()
    if comparison_rows:
        comp_df = pd.DataFrame(comparison_rows)
        comp_df = comp_df.sort_values(by=["경쟁차종", "좋아요"], ascending=[True, False])

        print("\n⚔️ [Part 1] 맛보기: 경쟁차종 비교 (Top 2 베스트만)")
        for car in COMPETITORS.keys():
            car_reviews = comp_df[comp_df['경쟁차종'] == car].head(2)

            if not car_reviews.empty:
                print(f"\n🚘 vs [{car}]")
                for _, row in car_reviews.iterrows():
                    print(f"  - (👍{row['좋아요']}) {row['내용']}")
                    print("  " + "-" * 50)

    # 2. 아반떼N 순수 후기
    if general_reviews:
        gen_df = pd.DataFrame(general_reviews)
        gen_df = gen_df.sort_values(by="좋아요", ascending=False)

        print("\n" + "=" * 60)
        print("🏁 [Part 2] 메인: 아반떼N 찐 오너들의 주행 경험 (Top 50)")
        print("=" * 60 + "\n")

        top_general = gen_df.head(50)
        for i, row in top_general.reset_index().iterrows():
            print(f"[{i + 1}위] (👍{row['좋아요']})")
            print(f"📄 {row['내용']}")
            print("-" * 60)
    else:
        print("❌ 일반 후기를 찾지 못했습니다.")

    # ==========================================
    # 시각화 실행
    # ==========================================
    print("\n📈 그래프를 생성합니다...")
    visualize_results(comp_df, strength_counter)


if __name__ == "__main__":
    analyze_reviews()