import cv2
import numpy as np
import random
import math

#이미지 경로
image_path = 

#이미지 로드 및 처리
img = cv2.imread(image_path)
if img is None:
    raise FileNotFoundError(f" {image_path}")

w_c = img.shape[0]/2
h_c = img.shape[1]/2

#회색조 변환 후 엣지 찾기
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 50, 50)

contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

rad = []

idx = 0
for i in range(62):
    idx_be = idx
    idx += 10 if i < 30 else 5
    img_zeros = np.zeros(img.shape).astype(np.uint8)
    img_zeros = img_zeros + 255

    #윤곽선 찾기 및 그리기
    cv2.drawContours(img_zeros, contours[idx_be:idx], -1, (255, 0, 0), 3)

    gray = cv2.cvtColor(img_zeros, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 0.00001, param1=50, param2=30, minRadius=0, maxRadius=0)

    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            if math.floor(w_c) - 10 < x < math.ceil(w_c) + 10 and math.floor(h_c) - 10 < y < math.ceil(h_c) + 10:
                save = True
                for k in rad:
                    if k - 10 < r < k + 10:
                        save = False
                if save:
                    rad.append(r)
                    cv2.circle(img, (x, y), r, (0, 255, 0), 1)
                break

#점에 따른 점수 계산 함수
def calculate_score(x, y, target_x, target_y, radii):
    distance = np.sqrt((x - target_x)**2 + (y - target_y)**2)
    for i, radius in enumerate(reversed(radii)):
        if distance <= radius:
            return len(radii) - i  
    return 0  

#두 팀의 점수 생성 및 계산 함수
def generate_teams_scores(image, num_dots_per_team, radius, target_x, target_y, radii):
    height, width, _ = image.shape
    team_scores = {'Team1': 0, 'Team2': 0}

    for team in team_scores:
        for _ in range(num_dots_per_team):
            x, y = random.randint(0, width), random.randint(0, height)
            color = (0, 0, 255) if team == 'Team1' else (255, 0, 0)
            cv2.circle(image, (x, y), radius, color, -1)
            score = calculate_score(x, y, target_x, target_y, radii)
            team_scores[team] += score
    
    return team_scores

#무작위 점 생성 및 점수 계산
num_dots_per_team = 5
radius = 5
scores = generate_teams_scores(img, num_dots_per_team, 5, w_c, h_c, rad)

#점수 출력 및 이미지에 점수 출력
cv2.putText(img, f"Team 1 Total Score: {scores['Team1']}", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
cv2.putText(img, f"Team 2 Total Score: {scores['Team2']}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
print("Team 1 Total Score:", scores['Team1'])
print("Team 2 Total Score:", scores['Team2'])


cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()