import cv2
from datetime import datetime
import numpy as np

def timeSinceGame(game_start_time):
    
    v = game_start_time.split('.')[0]
    print(v)
    
    v = datetime.fromisoformat(v)
    time =datetime.utcnow().timestamp()-v.timestamp()
    if time < 0:
        return None
    year = time // (12 * 30 * 24 * 3600)
    time = time % (12 * 30 * 24 * 3600)
    month = time // (30 * 24 * 3600)
    time = time % (30 * 24 * 3600)
    day = time // (24 * 3600)
    time = time % (24 * 3600)
    hour = time // 3600
    time %= 3600
    minutes = time // 60
    time %= 60
    seconds = time
    time_list = list(map(int,[year,month,day,hour,minutes,seconds]))
    str_list = ['Y','M','D','H','MIN','S']
    i =-1
    for t in time_list:
        i += 1
        if not t > 0:
            continue
        elif t == time_list[-1]:
            time_since_game = str(time_list[-2]) + str_list[-2]
            break
        else:
            time_since_game = str(t) + str_list[i]     
            break    
            
    return time_since_game


def combineIcons(faction_list):
    if len(faction_list) == 1:
        return 1
    elif len(faction_list) == 2:
        fac1 = cv2.imread(faction_list[0],cv2.IMREAD_UNCHANGED)
        fac2 = cv2.imread(faction_list[1],cv2.IMREAD_UNCHANGED)
        final = np.zeros(128*128*4*2).reshape(128,128*2,4)
        final[:,:128,:] = fac1[:,:,:]
        final[:,128:,:] = fac2
        cv2.imwrite('sss.png',final)
        return 2
    elif len(faction_list)  == 3:
        fac1 = cv2.imread(faction_list[0],cv2.IMREAD_UNCHANGED)
        fac2 = cv2.imread(faction_list[1],cv2.IMREAD_UNCHANGED)
        fac3 = cv2.imread(faction_list[2],cv2.IMREAD_UNCHANGED)
        final = np.zeros(128*128*4*3).reshape(128,128*3,4)
        final[:,:128,:] = fac1
        final[:,128:256,:] = fac2
        final[:,256:,:] = fac3
        cv2.imwrite('sss.png',final)
        return 3
print(combineIcons(['icon-ionia.png'])    )    


