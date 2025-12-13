# 🏎️ 아반떼 N (Avante N) 실소유주 리뷰 심층 분석기
### 🧠 유튜브 댓글 기반 실소유주 분석 프로젝트
"그 돈이면 씨..."(그돈씨)를 외치는 비방글은 거르고, **진짜 오너들의 목소리만 듣는다.**

<div align="center">
<img src="avante1.jpg" width="48%" alt="Avante N Front View" style="border-radius: 10px; margin-right: 5px;" />
<img src="avante2.jpg" width="48%" alt="Avante N Rear View" style="border-radius: 10px;" />
</div>

---

## 📌 프로젝트 개요 (Project Overview)

아반떼 N은 국산차 역사상 최고의 퍼포먼스를 보여주지만, '아반떼'라는 이름 때문에  
**"그 돈이면 그랜저나 중고 G70을 산다"**는 비아냥의 대상이 되곤 합니다.

이 프로젝트는 **유튜브 댓글 빅데이터(약 10만 건)**를 수집 및 분석하여,  
대중의 편견(브랜드/하차감)과 실제 오너들의 경험(재미/가성비) 차이를 데이터로 증명합니다.

특히 경쟁 차종 오너들의 훈수나 단순 비방글을 필터링하고,  
**실제 소유주만이 알 수 있는 경험(출고, 서킷, 고급유, 기변 등)**을 추출하여  
아반떼 N의 진짜 가치를 재조명합니다.

---

## 🗂 데이터 수집 & 전처리

- YouTube 댓글 크롤링
- 멀티 CSV 통합 (총 6개)
- 중복 제거 및 텍스트 전처리
- 실오너/비오너/비교 리뷰 자동 라벨링

---

## 📊 1. 댓글 필터링 단계별 감소 과정

> 원본 댓글 → 의미 있는 댓글 → 경험 기반 → 실오너

<div align="center">
  <img src="avante4.png" width="75%" alt="Filtering Pipeline" />
</div>

**해석**  
단계별로 댓글 수가 급격히 줄어드는 것은,  
“실제 경험 기반” 문장만을 골라낸 필터의 강력함을 의미합니다.

---

## 📊 2. 리뷰 유형 비율

<div align="center">
  <img src="avante5.png" width="60%" alt="Review Ratio" />
</div>

**해석**  
비오너(관전평) 댓글이 과반을 차지하고,  
실오너는 소수지만 **질적 내용이 풍부**합니다.

---

## 📊 3. 경쟁 차종 언급 빈도

<div align="center">
  <img src="avante3.png" width="95%" alt="Competitor Mentions" />
</div>

**해석**  
가장 많이 비교된 모델은  
- BMW 3시리즈 / M 계열  
- 제네시스 G70  
- 머스탱 / 카마로  
입니다.  
이는 아반떼 N이 **순수 스포츠 드라이빙 머신**으로 인식된다는 증거입니다.

---

## 📊 4. 오너 vs 비오너 리뷰 길이 분포

<div align="center">
  <img src="avante6.png" width="80%" alt="Review Length Distribution" />
</div>

**해석**  
실오너 리뷰는 비오너 리뷰보다 글 길이가 훨씬 깁니다.  
이는 **경험 기반 서술 중심**임을 의미합니다.

---

## 📊 5. 오너 핵심 가치 키워드 분석

<div align="center">
  <img src="avante7.png" width="80%" alt="Owner Keyword Importance" />
</div>

**해석**  
오너들이 가장 많이 언급한 키워드:

- 운전 재미
- 코너링
- 배기음
- DCT 반응
- 가성비

브랜드/고급감보다  
**‘운전 경험’**이 핵심 가치로 드러납니다.

---

## 💬 Voice of Real Owners  
### CSV 기반 실오너 의견 자동 추출
---

## 💬 Voice of Real Owners : 찐 오너들의 비교 리뷰

### 🏆 vs 제네시스 G70 / 스팅어
> **"G70 2.5 타다가 아반떼 N으로 넘어왔습니다."**  
> 코너 거동은 비교 불가. 하차감은 포기했지만 **운전 재미는 10배**.

---

### 🏆 vs BMW 3시리즈 / M
> **"M440i 세컨카로 아반떼 N 들였습니다."**  
> 이 가격에 이런 미션 반응·배기음은 **전 세계 유일**. 성능 대비 가성비 우주 최강.

---

### 🏆 vs 머스탱 / 카마로
> **"머스탱 2.3 갔다가 다시 N 왔습니다."**  
> 무거운 차체보다 **와인딩·서킷에서 아엔 압살**.

---

# 🛠️ 핵심 기능 및 기술 (Features & Tech)

## 1. 🔍 유튜브 댓글 대량 수집 (Data Collection)
- YouTube Data API 기반 10만 건 크롤링
- 아반떼 N 키워드 자동 스캔 기능

---

## 2. 🛡️ 초고강도 오너 필터링 (Strict Filtering Algorithm)

| 라벨 | 설명 |
|------|------|
| owner | 실제 소유 경험 기반 리뷰 |
| comparison | 경쟁 차종 비교 리뷰 |
| non-owner | 단순 감상평 |
| noise | 스팸·단문·의미 없음 |

```python
owner_keywords = ["출고", "고급유", "서킷", "와인딩", "dct", "타봤", "몰아봄"]
comparison_keywords = ["g70", "bmw", "m2", "3시리즈", "머스탱"]

def classify(text):
    t = text.lower()

    if any(k in t for k in owner_keywords):
        return "owner"
    if any(k in t for k in comparison_keywords):
        return "comparison"
    if len(t.strip()) < 5:
        return "noise"
    return "non-owner"

