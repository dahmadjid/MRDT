
from datetime import datetime

import os 
def timeSinceGame(game_start_time,p=0):
    
    v = game_start_time.split('.')[0]
    
    v = datetime.fromisoformat(v)
    time =datetime.utcnow().timestamp()-v.timestamp()
    if p == 1:
        return time
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


def combineIcons(faction_list,name):
    name = 'imgs/'+name+'.png'
    if len(faction_list) == 1:
        fac1 = cv2.imread(faction_list[0],cv2.IMREAD_UNCHANGED)
        cv2.imwrite(name,fac1)
        return 1
    elif len(faction_list) == 2:
        fac1 = cv2.imread(faction_list[0],cv2.IMREAD_UNCHANGED)
        fac2 = cv2.imread(faction_list[1],cv2.IMREAD_UNCHANGED)
        final = np.zeros(128*128*4*2).reshape(128,128*2,4)
        final[:,:128,:] = fac1[:,:,:]
        final[:,128:,:] = fac2
        cv2.imwrite(name,final)
        print(name)
        return 2
    elif len(faction_list)  == 3:
        fac1 = cv2.imread(faction_list[0],cv2.IMREAD_UNCHANGED)
        fac2 = cv2.imread(faction_list[1],cv2.IMREAD_UNCHANGED)
        fac3 = cv2.imread(faction_list[2],cv2.IMREAD_UNCHANGED)
        final = np.zeros(128*128*4*3).reshape(128,128*3,4)
        final[:,:128,:] = fac1
        final[:,128:256,:] = fac2
        final[:,256:,:] = fac3

        cv2.imwrite(name,final)
        print('3')
        return 3

# icon_dict ={'Demacia':'icon-demacia.png', 'ShadowIsles':'icon-shadowisles.png', 'Ionia':'icon-ionia.png', 'Freljord':'icon-freljord.png', 'MtTargon':'icon-targon.png', 'Piltover':'icon-piltoverzaun.png', 'Bilgewater':'icon-bilgewater.png', 'Noxus':'icon-noxus.png'}
# for faction1 in icon_dict:
#     combineIcons([icon_dict[faction1]],faction1)
# for faction1 in icon_dict:
#     for faction2 in icon_dict:
#         if faction2 == faction1:
#             continue
#         combineIcons([icon_dict[faction1],icon_dict[faction2]],faction1+'-'+faction2)
# for faction1 in icon_dict:
#     for faction2 in icon_dict:
#         if faction2 == faction1:
#             continue
#         for faction3 in icon_dict:
#             if faction3 == faction2 or faction3 == faction1:
#                 continue
#             combineIcons([icon_dict[faction1],icon_dict[faction2],icon_dict[faction3]],faction1+'-'+faction2+'-'+faction3)        
