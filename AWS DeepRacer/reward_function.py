import math

def reward_function(params):
    
    """
    Parameters 불러오기
    """
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    all_wheels_on_track = params['all_wheels_on_track']
    closest_waypoints = params['closest_waypoints']
    waypoints = params['waypoints']
    heading = params['heading']
    speed = params['speed']


    """
    중앙으로 안전하게 가게끔
    """
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width
    
    # 중앙에서 멀수록 낮은 reward
    if distance_from_center <= marker_1:
        reward = 1.0
    elif distance_from_center <= marker_2:
        reward = 0.5
    elif distance_from_center <= marker_3:
        reward = 0.1
    else:
        reward = 1e-3  # likely crashed/ close to off track
    
    """
    속도
    """
    reward += speed
    
    """
    Trck 방향 = 이동 방향 되게끔
    """
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]
    
    track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
    track_direction = math.degrees(track_direction)
    direction_diff = abs(track_direction - heading)
    
    if direction_diff > 180:
        direction_diff = 360 - direction_diff
    DIRECTION_THRESHOLD = 10.0
    
    if direction_diff > DIRECTION_THRESHOLD: # 트랙 방향 != 이동 방향
        reward *= 0.5
    else: # 트랙 방향 == 이동방향
        reward *= 1.2
        
    """
    바퀴 4개 전부 트랙 안에 있게 --> 안전
    """
    if all_wheels_on_track:
        reward *= 1.2
    else:
        reward *= 0.2
        
        
    return float(reward)