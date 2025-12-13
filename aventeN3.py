# ============================================================
# 🏎️ Avante N Real Owner Review Analysis (FINAL – CLEAN COLOR)
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import platform
import os
from matplotlib import rc
from collections import Counter

# ============================================================
# 0. 시각화 컬러 팔레트
# ============================================================
COLOR_PALETTE = "Set2"

# ============================================================
# 1. 파일 설정
# ============================================================
FILE_NAMES = [
    "avante_n_reviews_cleaned.csv",
    "avante_n_reviews_cleaned2.csv",
    "avante_n_reviews_cleaned3.csv",
    "avante_n_reviews_cleaned4.csv",
    "avante_n_reviews_cleaned5.csv",
    "avante_n_reviews_cleaned6.csv"
]

# ============================================================
# 2. 한글 폰트 설정
# ============================================================
system_name = platform.system()
if system_name == "Windows":
    rc("font", family="Malgun Gothic")
elif system_name == "Darwin":
    rc("font", family="AppleGothic")
else:
    rc("font", family="NanumGothic")

plt.rcParams["axes.unicode_minus"] = False

# ============================================================
# 3. 키워드 정의
# ============================================================
COMPETITORS = {
    "제네시스 G70": ["G70", "지칠공", "칠공"],
    "BMW (3시리즈/M)": ["BMW", "3시리즈", "M2", "M3", "M4"],
    "머스탱/카마로": ["머스탱", "카마로"]
}

REAL_OWNER_PROOF = [
    "내 차", "제 차", "출고", "기변", "대차", "세컨카",
    "타보니", "타보니까", "운행중", "운용중",
    "고급유", "서킷", "와인딩", "인제", "랩타임"
]

STRENGTH_KEYWORDS = [
    "재미", "펀카", "코너", "코너링", "핸들링",
    "배기음", "팝콘", "DCT", "미션", "가성비"
]

# ============================================================
# 4. 데이터 로딩
# ============================================================
dfs = []
for f in FILE_NAMES:
    if os.path.exists(f):
        dfs.append(pd.read_csv(f))

df = pd.concat(dfs, ignore_index=True)
df = df.drop_duplicates(subset="Review")
df["Review"] = df["Review"].fillna("")

print(f"✅ 전체 댓글 수: {len(df):,}")

# ============================================================
# 5. 라벨링 로직
# ============================================================
def label_review(text):
    if not any(k in text for k in REAL_OWNER_PROOF):
        return "non-owner"
    for car, kws in COMPETITORS.items():
        if any(k in text for k in kws):
            return "comparison"
    return "owner"

df["label"] = df["Review"].apply(label_review)

# ============================================================
# 6. 시각화 ① 댓글 필터링 단계별 감소 과정
# ============================================================
stage_counts = [
    len(df),
    df["Review"].str.len().gt(10).sum(),
    df["label"].isin(["owner", "comparison"]).sum(),
    (df["label"] == "owner").sum()
]

stages = ["전체 댓글", "의미 있는 댓글", "경험 언급", "찐 오너"]

plt.figure(figsize=(8,5))
plt.plot(
    stages,
    stage_counts,
    marker="o",
    linewidth=3,
    color="#4C72B0"
)
plt.title("댓글 필터링 단계별 데이터 감소 과정")
plt.ylabel("댓글 수")
plt.grid(True, linestyle="--", alpha=0.5)
plt.show()

# ============================================================
# 7. 시각화 ② 리뷰 유형 비율 (비율 기준)
# ============================================================
ratio = df["label"].value_counts(normalize=True) * 100

plt.figure(figsize=(6,6))
plt.pie(
    ratio,
    labels=ratio.index,
    autopct="%.1f%%",
    startangle=90,
    colors=sns.color_palette(COLOR_PALETTE)
)
plt.title("리뷰 유형 비율 분포")
plt.show()

# ============================================================
# 8. 시각화 ③ 경쟁 차종 언급 빈도
# ============================================================
comp_reviews = df[df["label"] == "comparison"]

comp_counter = Counter()
for text in comp_reviews["Review"]:
    for car, kws in COMPETITORS.items():
        if any(k in text for k in kws):
            comp_counter[car] += 1

plt.figure(figsize=(8,5))
sns.barplot(
    x=list(comp_counter.keys()),
    y=list(comp_counter.values()),
    palette=COLOR_PALETTE
)
plt.title("아반떼 N 오너들의 경쟁 차종 언급 빈도")
plt.ylabel("리뷰 수")
plt.show()

# ============================================================
# 9. 시각화 ④ 오너 vs 비오너 리뷰 길이 분포
# ============================================================
plt.figure(figsize=(8,5))
sns.kdeplot(
    df[df["label"]=="owner"]["Review"].str.len(),
    label="오너",
    linewidth=2,
    color="#0000FF"
)
sns.kdeplot(
    df[df["label"]=="non-owner"]["Review"].str.len(),
    label="비오너",
    linewidth=2,
    color="#000000"
)
plt.title("오너 vs 비오너 리뷰 길이 분포")
plt.xlabel("리뷰 길이")
plt.legend()
plt.show()

# ============================================================
# 10. 시각화 ⑤ 오너 리뷰 핵심 가치 키워드 분석
# ============================================================
owner_reviews = df[df["label"] == "owner"]

strength_counter = Counter()
for text in owner_reviews["Review"]:
    for k in STRENGTH_KEYWORDS:
        if k in text:
            strength_counter[k] += 1

total = sum(strength_counter.values())
strength_ratio = {
    k: v / total * 100 for k, v in strength_counter.items()
}

plt.figure(figsize=(8,5))
sns.barplot(
    x=list(strength_ratio.values()),
    y=list(strength_ratio.keys()),
    palette="Spectral"
)
plt.title("오너 리뷰 내 핵심 가치 비율")
plt.xlabel("비율 (%)")
plt.show()

# ============================================================
# 11. 💬 Voice of Real Owners : 찐 오너들의 비교 리뷰 (AUTO)
# ============================================================

print("\n" + "="*70)
print("💬 Voice of Real Owners : 찐 오너들의 비교 리뷰 (CSV 기반)")
print("="*70)

# 실제 오너 + 비교 리뷰만 사용
voice_df = df[
    (df["label"] == "comparison") &
    (df["Review"].str.len() > 30)
].copy()

# 문장 전처리
def clean_sentence(text):
    return (
        text.replace("\n", " ")
            .replace("  ", " ")
            .strip()
    )

# ============================================================
# 전체 비교차량 자동 출력
# ============================================================

for car_name, keywords in COMPETITORS.items():
    print(f"\n🏆 vs {car_name}")

    matched = (
        voice_df[
            voice_df["Review"].apply(
                lambda x: any(k in x for k in keywords)
            )
        ]["Review"]
        .apply(clean_sentence)
        .drop_duplicates()
        .head(10)
        .tolist()
    )

    if not matched:
        print("(조건에 맞는 실제 오너 리뷰 없음)")
    else:
        for i, m in enumerate(matched, 1):
            print(f"{i:02d}. \"{m}\"")

print("\n" + "="*70)
print("✅ 전체 비교차량 기준 Real Owner Voice 자동 출력 완료")


# ============================================================
# END
# ============================================================
print("🎯 분석 및 시각화 완료")
