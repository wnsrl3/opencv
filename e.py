import cv2
import numpy as np
import random

# 타겟에 따른 점수 계산 함수
def calculate_score(x, y, target_x, target_y, radii):
    distance = np.sqrt((x - target_x)**2 + (y - target_y)**2)
    score = 10
    for radius in radii:
        if distance > radius:
            score -= 1
        else:
            break
    return max(0, score)

# 두 팀의 점수 생성 및 계산 함수
def generate_dots_and_calculate_scores(image, num_dots_per_team, radius, target_x, target_y, radii):
    height, width, _ = image.shape
    scores = {'Team1': 0, 'Team2': 0}

    for team in ['Team1', 'Team2']:
        for _ in range(num_dots_per_team):
            x, y = random.randint(0, width), random.randint(0, height)
            color = (0, 0, 255) if team == 'Team1' else (255, 0, 0)
            cv2.circle(image, (x, y), radius, color, -1)
            score = calculate_score(x, y, target_x, target_y, radii)
            scores[team] += score

    return scores

# 점수 구역 시각화 함수
def define_score_zones(image, target_x, target_y, radii):
    for radius in radii:
        cv2.circle(image, (target_x, target_y), radius, (255, 255, 255), 2)

# 첫 번째 감지된 원에 선을 그리는 함수
def detect_circle_and_draw_line(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=0, maxRadius=0)

    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            cv2.circle(image, (x, y), r, (0, 255, 0), 4)
            cv2.line(image, (x - r, y), (x + r, y), (255, 0, 0), 3)
            break

# 이미지 경로 수정
image_path = 'C:\\asdasda.png'

# 이미지 로드 및 처리
img = cv2.imread(image_path)
if img is None:
    raise FileNotFoundError(f"경로 {image_path}에서 이미지를 찾거나 열 수 없습니다.")

# 그레이스케일로 변환 후 에지 찾기
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 100, 200)

# 윤곽선 찾기 및 그리기
contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(img, contours, -1, (0, 255, 0), 3)

# 원 감지 및 선 그리기
detect_circle_and_draw_line(img)

# 타겟 위치 및 점수 구역 정의
radii_scores = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
target_x, target_y = 100, 100
define_score_zones(img, target_x, target_y, radii_scores)

# 점 생성 및 점수 계산
num_dots_per_team = 5
radius = 5
scores = generate_dots_and_calculate_scores(img, num_dots_per_team, radius, target_x, target_y, radii_scores)

# 점수 출력 및 이미지에 점수 표시
cv2.putText(img, f"Team 1 Total Score: {scores['Team1']}", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
cv2.putText(img, f"Team 2 Total Score: {scores['Team2']}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
print("Team 1 Total Score:", scores['Team1'])
print("Team 2 Total Score:", scores['Team2'])

# Display image, 도트
cv2.imshow('Image with dots', img)
cv2.waitKey(0)
cv2.destroyAllWindows()