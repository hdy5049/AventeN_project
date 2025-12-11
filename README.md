# 🏎️ 아반떼 N (Avante N) 실소유주 리뷰 심층 분석기

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

## 📊 데이터 분석 시각화 (Visualization)

오너들이 아반떼 N을 선택할 때 어떤 차종과 가장 치열하게 고민했는지,  
그리고 어떤 매력 포인트 때문에 최종 선택을 했는지 시각화한 그래프입니다.

<div align="center">
<img src="avante3.png" width="95%" alt="Analysis Graph" style="border-radius: 10px; box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);" />
</div>

---

## 💡 분석 인사이트 (Insights)

### ✔ 최다 비교군  
BMW 3시리즈 / M 계열과의 비교 언급이 **가장 많음** →  
오너들이 이 차를 **스포츠 드라이빙 머신**으로 인식한다는 증거.

### ✔ 승리 요인  
브랜드나 고급감은 부족하지만  
**운전 재미, 코너링, 배기음, 가성비**에서 압도적 우세.

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
