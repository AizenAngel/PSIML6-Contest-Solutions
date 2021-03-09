#
# Ako je bas mala razlika izmedju count-a, a i rastojanja se razlikuju bas brda malo
#

import os
import json
import math
from copy import deepcopy

def find_Min_Max(dataSet, position):
    first = position - 1
    last = position + 1
    
    while True:
        if first not in dataSet:
            first -= 1
            if first < 0:
                break
        else:
            break
    
    M = max([x for x in dataSet])
    
    while True:
        if last not in dataSet:
            last += 1
            if last > M:
                break
        else:
            break
            
    if first < 0:
        first = 0
    
    if last > M:
        last = position
    
    return first, last

boxesFile = input()
jointsFile = input()

# boxesFile = "Test2/public/set/4/bboxes.json"
# jointsFile = "Test2/public/set/4/joints.json"


boxes_dict = {}

with open(boxesFile) as f:
    read_files = json.load(f)

#read_files["frames"][6]["bounding_boxes"]

for frames in read_files["frames"]:
    frame_index = frames["frame_index"]
    boxes_dict[frame_index] = []
    for box in frames["bounding_boxes"]:
        identity = box["identity"]
        bounding_box = box["bounding_box"]
        
        boxes_dict[frame_index].append({identity: bounding_box})

#print(boxes_dict)

joints_dict = {}

with open(jointsFile) as f:
    read_files = json.load(f)
    
for frames in read_files["frames"]:
    frame_index = frames["frame_index"]
    joints_dict[frame_index] = []
    for joints in frames["joints"]:
        identity = joints["identity"]
        joint = joints["joint"]
        
        joints_dict[frame_index].append({identity: joint}) 


m1 = min([x for x in joints_dict])
M1 = max([x for x in joints_dict])

for box_frame in boxes_dict:
    if box_frame not in joints_dict:
        first, last = find_Min_Max(joints_dict, box_frame)
        #print(f"Box frame: {box_frame}")
        
        multiply = (box_frame - first) / (last-first)
        #print(f"Multiply: {multiply}")
        
        #racunamo samo drugu tacku
        if first < m1:
#             last_joint = joints_dict[last]
#             find_joint = deepcopy(last_joint)
            
            find_joint = deepcopy(joints_dict[last])
            
            for tmp in find_joint:
                for tmp1 in tmp:
                    tmp[tmp1]['x'] *= multiply
                    tmp[tmp1]['y'] *= multiply
            
            joints_dict[box_frame] = find_joint
            
            
        #racunamo samo prvu tacku
        elif last > M1:
#             first_joint = joints_dict[first]
#             find_joint = deepcopy(first_joint)
            
            find_joint = deepcopy(joints_dict[first])
    
            for tmp in find_joint:
                for tmp1 in tmp:
                    tmp[tmp1]['x'] *= (1/multiply)
                    tmp[tmp1]['y'] *= (1/multiply)
                    
            joints_dict[box_frame] = find_joint
        #racunamo obe tacke
        
        else:
            find_joint = deepcopy(joints_dict[first])
            last_joint = deepcopy(joints_dict[last])
            
            for array_l in last_joint:
                for points_l in array_l:
                    for array_f in find_joint:
                        for points_f in array_f:
                            if points_l == points_f:
                                array_f[points_f]['x'] = array_f[points_f]['x'] + multiply * (array_l[points_l]['x'] - array_f[points_f]['x'])
                                array_f[points_f]['y'] = array_f[points_f]['y'] + multiply * (array_l[points_l]['y'] - array_f[points_f]['y'])
            
            joints_dict[box_frame] = find_joint            

m1 = min([x for x in boxes_dict])
M1 = max([x for x in boxes_dict])

for joint_frame in joints_dict:
    if joint_frame not in boxes_dict:
        first, last = find_Min_Max(boxes_dict, joint_frame)
        #print(f"Box frame: {box_frame}")
        
        multiply = (joint_frame - first) / (last-first)
        #print(f"Multiply: {multiply}")
        
        #racunamo samo drugu tacku
        if first < m1:
            
            find_joint = deepcopy(boxes_dict[last])
            
            for tmp in find_joint:
                for tmp1 in tmp:
                    tmp[tmp1]['h'] *= multiply
                    tmp[tmp1]['w'] *= multiply
                    tmp[tmp1]['x'] *= multiply
                    tmp[tmp1]['y'] *= multiply
            
            boxes_dict[joint_frame] = find_joint
            
            
        #racunamo samo prvu tacku
        elif last > M1:
#             first_joint = joints_dict[first]
#             find_joint = deepcopy(first_joint)
            
            find_joint = deepcopy(boxes_dict[first])
    
            for tmp in find_joint:
                for tmp1 in tmp:
                    tmp[tmp1]['h'] *= multiply
                    tmp[tmp1]['w'] *= multiply
                    tmp[tmp1]['x'] *= multiply
                    tmp[tmp1]['y'] *= multiply
                    
            boxes_dict[joint_frame] = find_joint
        #racunamo obe tacke
        
        else:
            find_joint = deepcopy(boxes_dict[first])
            last_joint = deepcopy(boxes_dict[last])
            
            for array_l in last_joint:
                for points_l in array_l:
                    for array_f in find_joint:
                        for points_f in array_f:
                            if points_l == points_f:
                                array_f[points_f]['h'] = array_f[points_f]['h'] + multiply * (array_l[points_l]['h'] - array_f[points_f]['h'])
                                array_f[points_f]['w'] = array_f[points_f]['w'] + multiply * (array_l[points_l]['w'] - array_f[points_f]['w'])
                                array_f[points_f]['x'] = array_f[points_f]['x'] + multiply * (array_l[points_l]['x'] - array_f[points_f]['x'])
                                array_f[points_f]['y'] = array_f[points_f]['y'] + multiply * (array_l[points_l]['y'] - array_f[points_f]['y'])
                    
            boxes_dict[joint_frame] = find_joint            
            
            
m = min([x for x in boxes_dict])
M = max([x for x in boxes_dict])

solutions = {}
points_distance = {}

for i in range(m, M+1):
    if i not in boxes_dict or i not in joints_dict:
        continue
    
    boxes = boxes_dict[i]
    joints = joints_dict[i]
    
    for box in boxes:
        for index_box in box:
            for joint in joints:
                for index_joint in joint:
                    #print(index_joint)
                    
                    jointX = joint[index_joint]['x']
                    jointY = joint[index_joint]['y']

                    boxX = box[index_box]['x']
                    boxY = box[index_box]['y']
                    boxH = box[index_box]['h']
                    boxW = box[index_box]['w']
                     
                    if boxX < jointX and jointX < boxX + boxW and boxY + boxH > jointY and jointY > boxY:
                        if index_joint not in solutions:
                            
                            solutions[index_joint] = []
                            solutions[index_joint].append(index_box)
                            points_distance[index_joint] = []
                            points_distance[index_joint].append({index_box : {"dis": abs(boxX + boxW/2 - jointX), "count":int(1)}})
                        
                        elif index_box not in solutions[index_joint]:
                            
                            solutions[index_joint].append(index_box)
                            points_distance[index_joint].append({index_box : {"dis": abs(boxX + boxW/2 - jointX), "count":int(1)}})
                        
                        elif index_box in solutions[index_joint]:
                            for tmp in points_distance[index_joint]:
                                for tmp1 in tmp:
                                    if tmp1 == index_box:
                                        tmp[tmp1]["dis"] += abs(boxX + boxW/2 - jointX)
                                        tmp[tmp1]["count"] += 1
                                        break
                        
# for joints in points_distance:
#     print(joints, points_distance[joints])

final_solution = {}
# print()  

for joints in points_distance:
    min1 = 100000
    count1 = 0
    final_solution[joints] = []
    for group in points_distance[joints]:
        for boxes in group:
            dis = group[boxes]["dis"]
            dis_count = group[boxes]["count"]
            
            if dis_count > count1:
                min_box = boxes
                count1 = dis_count
                min1 = dis      
            
            elif (dis_count == count1 and dis < min1):
                #print(joints, boxes, dis_count, count1)
                min_box = boxes
                count1 = dis_count  
                min1 = dis
            
            elif (dis_count > count1 - 2 and 2 * dis < min1):
                min_box = boxes
                count1 = dis_count  
                min1 = dis    
    
    
    final_solution[joints].append(min_box)

        
m = min([int(x) for x in solutions])
M = max([int(x) for x in solutions])

for i in range(m, M+1):
    if str(i) in final_solution:
        print(f"{str(i)}:{(final_solution[str(i)][0])}")

# print(solutions)

# for point in points_distance:
#     print(point, points_distance[point])
#     print()