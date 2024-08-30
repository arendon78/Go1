import numpy as np
import json
import matplotlib.pyplot as plt
import random
import math

def calculate_derivative(p1,p2):
    return ((p2[1]-p1[1])/(p2[0]-p1[0]))

#not exactly a gradient, but idea is the same idea
def gradient_ascent(list_point_derivative) : 
    HORIZON = min(max(int(len(list_point_derivative)/10),2), 10)
    p = random.randrange(HORIZON//2,len(list_point_derivative)-HORIZON//2)
    for _ in range(int(0.25*len(list_point_derivative))):
        current_point = list_point_derivative[p]
        found_higher_point = False
        j = 1
        while  j<HORIZON//2 and not found_higher_point: 
            if (p+j) > len(list_point_derivative)-1 or (p-j) < 0 : 
                break
            left_point = list_point_derivative[p-j]
            right_point = list_point_derivative[p+j]
            #we go in the direction of the highest point in an horizon of 10 points. this is to prevent beiing stuck because of local plateaus(where the first derivative would be stuck)
            if right_point[1] > current_point[1] : 
                p+=j
                found_higher_point = True
                break
            elif left_point[1] >= current_point[1]: 
                p-=j
                found_higher_point = True
                break
            else : None
            j+=1                
    return list_point_derivative[p]

#not exactly a gradient, but idea is the same
def gradient_descent(list_point_derivative): 
    
    HORIZON = min(max(int(len(list_point_derivative)/10),2), 10)
    p = random.randrange(HORIZON//2,len(list_point_derivative)-HORIZON//2)
    for _ in range(int(0.25*len(list_point_derivative))):
        current_point = list_point_derivative[p]

        found_higher_point = False
        j = 1
        while  j < HORIZON//2 and not found_higher_point: 
            if p+j > len(list_point_derivative)-1 or p-j< 0 : 
                break


            left_point = list_point_derivative[p-j]


            right_point = list_point_derivative[p+j]
            #we go in the direction of the lowest point in an horizon of 10 points. this is to prevent beiing stuck because of local plateaus(where the first derivative would be stuck)
            if right_point[1] < current_point[1] : 
                p+=j
                found_higher_point = True
            elif left_point[1] <= current_point[1]: 
                p-=j
                found_higher_point = True
            else : None
            j+=1                
    return list_point_derivative[p]


def calculate_mean_rooted_derivative(p1,p2, l) : 
    i1 = -1
    i2 = -1
    for i in range(len(l)): 
        if l[i] == p1 : 
            i1 = i
        if l[i] == p2 : 
            i2 = i
    if i1<0 and i2< 0: 
        print("one of the point not found inthe list !!!")
    if i1 > i2: # unordered params or unordered list: swap the points st l[i1] = p1 and l[i2] = p2 and i1<i2 in any case
        p1,p2 = p2,p1
        i1,i2 = i2,i1
    d_abs_sum = 0
    for p in range(i1, i2+1):
        d_abs_sum += math.sqrt(abs(l[p][2]))
    d_abs_mean = d_abs_sum/(i2-i1)
    return d_abs_mean

def find_value(time, list):
    for i in range(len(list)):
        if list[i][0] == time :
            return list[i]
    print("not found")


def monte_carlo_gradient(direction,l):
    # print("len(l) : ", len(l))
    n_rep = int(len(l)//10 *1.5)
    if direction <0 : 
        local_mins = []
        # print("nrep : ",n_rep)

        #monte carlo
        for i in range(n_rep): 
            local_min_found = gradient_descent(l)
            # if i%100 == 0: 
                # print("returned  :",local_min_found)
            local_mins.append(local_min_found)
        local_mins = list(set(tuple(sub_list) for sub_list in local_mins))
        # print("new length : ", len(local_mins))
        return local_mins
    
    else : 
        local_maxes = []
        for i in range(n_rep): 
            local_max_found = gradient_ascent(l)
            # if i%100 == 0: 
                # print("returned  :",local_max_found)
            local_maxes.append(local_max_found)
        local_maxes = list(set(tuple(sub_list) for sub_list in local_maxes))
        # print("new length : ", len(local_maxes))
        return local_maxes

#4 criterias  to recognise the curve of a step : 
#-alternate between max min max
#-time between max1 min1 and min1 max2 is in a given range 
#-the amplitudes are relatively close
#-there is not a plateau at the bottom of the curve (mean of sqrt of derivatives)
# def find_pattern_fr(merged_mins_maxes_coordinates,fr_coordinates) :
#     PRECISION = 0.5
#     pattern_to_fit = ["max","min","max"]
#     p = 0
#     for i in range(len(merged_mins_maxes_coordinates)-2): 
#         p0 = merged_mins_maxes_coordinates[i]
#         p1 = merged_mins_maxes_coordinates[i+1]
#         p2 = merged_mins_maxes_coordinates[i+2]

#         pattern = [p0[3],p1[3],p2[3]]
#         if pattern == pattern_to_fit : # good pattern : now let's see if that works

#             deltat1 = abs(p1[0] - p0[0])
#             deltat2 = abs(p2[0] - p1[0])

#             amplitude1 = abs(p1[1] - p0[1])
#             amplitude2 = abs(p2[1] - p1[1])

#             # if abs(deltat1 - 25) <25 * PRECISION and abs(deltat2 - 25) < 25 * PRECISION: 
#             if p0[1] > 500 and p2[1] > 500:# this is a criterion of height : if you decrease the weight of the robot (by taking away the battery for example), it might not work as expected. This is the best criterion for caracterising a step.)
#                 # if abs(amplitude1 - amplitude2)/ (amplitude1 + amplitude2) <0.2:# <0.1
#                 if calculate_mean_rooted_derivative(p0[:-1],p2[:-1],fr_coordinates) > 4:
#                     p+=1
#                     print("pattern found !! the robot was walking : ", p0,p1,p2,abs(amplitude1 - amplitude2)/ (amplitude1 + amplitude2),deltat1, deltat2 ,
#                       "\n mean absolute derivative : ",calculate_mean_rooted_derivative(p0[:-1],p2[:-1],fr_coordinates),"\n" )
    # print(p)

# def find_pattern_fl(merged_mins_maxes_coordinates,fr_coordinates) :
#     PRECISION = 0.5
#     pattern_to_fit = ["max","min","max"]
#     p = 0
#     for i in range(len(merged_mins_maxes_coordinates)-2): 
#         p0 = merged_mins_maxes_coordinates[i]
#         p1 = merged_mins_maxes_coordinates[i+1]
#         p2 = merged_mins_maxes_coordinates[i+2]

#         pattern = [p0[3],p1[3],p2[3]]
#         if pattern == pattern_to_fit : # good pattern : now let's see if that works

#             deltat1 = abs(p1[0] - p0[0])
#             deltat2 = abs(p2[0] - p1[0])

#             amplitude1 = abs(p1[1] - p0[1])
#             amplitude2 = abs(p2[1] - p1[1])

#             # if abs(deltat1 - 25) <25 * PRECISION and abs(deltat2 - 25) < 25 * PRECISION: 
#             if p0[1] > 700 and p2[1] > 700:# this is a criterion of height : if you decrease the weight of the robot (by taking away the battery for example), it might not work as expected. This is the best criterion for caracterising a step.)
#                     # if abs(amplitude1 - amplitude2)/ (amplitude1 + amplitude2) <0.2:# <0.1
#                 if calculate_mean_rooted_derivative(p0[:-1],p2[:-1],fr_coordinates) > 5.5:
#                     p+=1
#                     print("pattern found !! the robot was walking : ", p0,p1,p2,abs(amplitude1 - amplitude2)/ (amplitude1 + amplitude2),deltat1, deltat2 ,
#                       "\n mean absolute derivative : ",calculate_mean_rooted_derivative(p0[:-1],p2[:-1],fr_coordinates),"\n" )
#     print(p)


def find_patterns(merged_mins_maxes_coordinates, coordinates, p0_spike,p2_spike,MRD_value ) :
    pattern_to_fit = ["max","min","max"]
    p = 0
    for i in range(len(merged_mins_maxes_coordinates)-2): 
        p0 = merged_mins_maxes_coordinates[i]
        p1 = merged_mins_maxes_coordinates[i+1]
        p2 = merged_mins_maxes_coordinates[i+2]

        pattern = [p0[3],p1[3],p2[3]]
        if pattern == pattern_to_fit : # good pattern : now let's see if that works

            deltat1 = abs(p1[0] - p0[0])
            deltat2 = abs(p2[0] - p1[0])

            amplitude1 = abs(p1[1] - p0[1])
            amplitude2 = abs(p2[1] - p1[1])

            # if abs(deltat1 - 25) <25 * PRECISION and abs(deltat2 - 25) < 25 * PRECISION: 
            if p0[1] > p0_spike and p2[1] > p2_spike :# this is a criterion of height : if you decrease the weight of the robot (by taking away the battery for example), it might not work as expected. This is the best criterion for caracterising a step.)
                # if abs(amplitude1 - amplitude2)/ (amplitude1 + amplitude2) <0.2:# <0.1
                if calculate_mean_rooted_derivative(p0[:-1],p2[:-1],coordinates) > MRD_value:
                    p+=1
                    print("pattern found !! the robot was walking : ", p0,p1,p2,abs(amplitude1 - amplitude2)/ (amplitude1 + amplitude2),deltat1, deltat2 ,
                      "\n mean absolute derivative : ",calculate_mean_rooted_derivative(p0[:-1],p2[:-1],coordinates),"\n" )
    print(p)



def find_a_pattern(merged_mins_maxes_coordinates,coordinates, p0_spike,p2_spike, MRD_value) : 
    PRECISION = 0.5 
    pattern_to_fit = ["max","min","max"]
    p = 0
    for i in range(len(merged_mins_maxes_coordinates)-2): 
        p0 = merged_mins_maxes_coordinates[i]
        p1 = merged_mins_maxes_coordinates[i+1]
        p2 = merged_mins_maxes_coordinates[i+2]

        pattern = [p0[3],p1[3],p2[3]]
        if pattern == pattern_to_fit : # good pattern : now let's see if that works

            deltat1 = abs(p1[0] - p0[0])
            deltat2 = abs(p2[0] - p1[0])

            amplitude1 = abs(p1[1] - p0[1])
            amplitude2 = abs(p2[1] - p1[1])
            if abs(deltat1 - 25) <25 * PRECISION and abs(deltat2 - 25) < 25 * PRECISION: # when detecting in live, this criteria is important. (there can appear local maxes/mins that don't appear usually)
                if p0[1] > p0_spike and p2[1] > p2_spike:# this is a criterion of height : if you decrease the weight of the robot (by taking away the battery for example), it might not work as expected. This is the best criterion for caracterising a step.)
                    if calculate_mean_rooted_derivative(p0[:-1],p2[:-1],coordinates) > MRD_value:
                        # p+=1
                        print("pattern found !! the robot was walking : ", p0,p1,p2,abs(amplitude1 - amplitude2)/ (amplitude1 + amplitude2),deltat1, deltat2 ,
                          "\n mean absolute derivative : ",calculate_mean_rooted_derivative(p0[:-1],p2[:-1],coordinates),"\n" )
                        return True, p0,p1,p2
    return False ,None,None,None
                            
#builds an ordered list (along time axis) of maxes and mins 

def build_merge(local_maxes, local_mins) :# O(n**2)
    merged_mins_maxes_coordinates = []

    local_maxes_copy = local_maxes
    local_mins_copy = local_mins

    nmax  = len(local_maxes)
    nmin = len(local_mins)

    for _ in range(nmax + nmin):
        if local_maxes_copy != []:
            index_max_in_list = 0
            # first_point_max = local_maxes_copy[index_max_in_list]
            time_maxes_index = local_maxes_copy[index_max_in_list][0]
            #search for minimum time in maxes
            for j in range(len(local_maxes_copy)): 
                if local_maxes_copy[j][0] < time_maxes_index : 
                    time_maxes_index = local_maxes_copy[j][0]
                    index_max_in_list = j
                    # first_point = local_maxes_copy[index_max_in_list]
        else : 
            time_maxes_index = 100000000000000000000000000000000000000

        if local_mins_copy != []:
            index_min_in_list = 0
            # first_point_min = local_mins_copy[index_min_in_list]
            time_mins_index = local_mins_copy[index_min_in_list][0]
            #search for minimum min in mins
            for p in range(len(local_mins_copy)):
                if local_mins_copy[p][0] < time_mins_index : 
                    time_mins_index = local_mins_copy[p][0]
                    index_min_in_list = p
                    # first_point_min = local_mins_copy[index_min_in_list]
        else : 
            time_mins_index = 100000000000000000000000000000000000000

        if time_maxes_index < time_mins_index : 
            el = local_maxes_copy.pop(index_max_in_list)
            merged_mins_maxes_coordinates.append( [el[0],el[1],el[2],"max"])
        else : 
            el = local_mins_copy.pop(index_min_in_list)
            merged_mins_maxes_coordinates.append( [el[0],el[1],el[2],"min"])
    return merged_mins_maxes_coordinates
