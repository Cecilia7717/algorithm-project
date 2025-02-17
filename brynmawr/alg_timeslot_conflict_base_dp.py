# This is a naive base 
from array import array
import sys
# sys.setrecursionlimit(2000000)
import numpy as np
import pandas as pd

# function to check if a class can fit into a classroom at a given time slot
def could_wy(classObj, room, time, profArr, classArr, class_ID_real, timeArr):
    prof = classObj.prof
    prof_class1 = profArr[0][prof]
    prof_class2 = profArr[1][prof]

    if (prof_class1 != -1) and (int(classArr[class_ID_real[prof_class1]].timeslot) != -1):
        if (if_conflict(timeArr[int(classArr[class_ID_real[prof_class1]].timeslot)], timeArr[int(time)])):
            return False

    if (prof_class2 != -1) and (int(classArr[class_ID_real[prof_class2]].timeslot) != -1):
        if (if_conflict(timeArr[int(classArr[class_ID_real[prof_class2]].timeslot)], timeArr[int(time)])):
            return False

    return True

from functools import cmp_to_key


# Find the latest job (in sorted array) that 
# doesn't conflict with the job[i]. If there
# is no compatible job, then it returns -1
def latestNonConflict(arr, i):
    
    for j in range(i - 2, -1, -1):
        if not if_conflict(arr[j], arr[i-1]):
            return j
            
    return -1

def gen_schedule(n, arr):
    global pred
    # print(f"hh{pred}")
    j = n-1
    S = []
    while(j >= 0):
        # print(f"incl: {j} = {latestNonConflict(arr, j+1)}")
        if (pred[j] == latestNonConflict(arr, j+1)):
            S.insert(0, j)
        j = pred[j]
    return S

# A recursive function that returns the 
# maximum possible profit from given
# array of jobs. The array of jobs must
# be sorted according to finish time
def findMaxProfitRec(arr, n):
    global pred
    # Base case
    if n == 1:
        return 1
    
    # Find profit when current job is included
    inclProf = 1
    i = latestNonConflict(arr, n)
    if i != -1:
        inclProf += findMaxProfitRec(arr, i + 1)

    # Find profit when current job is excluded
    exclProf = findMaxProfitRec(arr, n - 1)
    if inclProf > exclProf:
        pred[n-1] = i
        # print(f"inclProf{n-1}: {i}")
        return inclProf
    else:
        pred[n-1] = n-2
        # print(f"exclProf{n-1}: {n-2}")
        return exclProf

# The main function that returns the maximum
# possible profit from given array of jobs
def findMaxProfit(arr, n):
    global pred
    # Sort jobs according to finish time
    pred = [-1] * len(arr)
    a = findMaxProfitRec(arr, n)
    # print(pred)
    return a

# function to schedule
def schedule_classes(classArr, classroomArr, timeSlots, roomList, popuList, profArr, class_ID_real, prof_ID_real, timeArr):
    empty = []  # list to store classes that couldn't be scheduled
    class_curr = 0  # current class index in the sorted class list
    one_done = False  # boolean to check if scheduling is complete
    # iterate over each classroom in descending order of size
    for roomID in roomList:
        # iterate over each time slot
        time = 0
        while time != timeSlots:
            # try the classes in 'empty' list first
            if empty:  # if there are classes in 'empty'
                for c in empty:
                    if could_wy(classArr[class_ID_real[c]], classroomArr[roomID], time, profArr, classArr, class_ID_real, timeArr):
                        # (f"empty classid:{c}time:{time} room:{roomID}")#hhhhhh
                        classArr[class_ID_real[c]].classroom = roomID
                        classArr[class_ID_real[c]].timeslot = time
                        classArr[class_ID_real[c]].real_ID = c
                        one_done = True
                        # print("class from empty is scheduled")
                        empty.remove(c)
                        break  # stop traversing 'empty'
            
            # if no class from `empty` could be scheduled, try scheduling the class in classArr
            while not one_done:
                if class_curr == len(popuList): # if all classes are scheduled
                    return classArr
                
                # try assigning the current class to the current room and time
                if could_wy(classArr[class_ID_real[popuList[class_curr]]], classroomArr[roomID], time, profArr, classArr, class_ID_real, timeArr):
                    classArr[class_ID_real[popuList[class_curr]]].classroom = roomID
                    classArr[class_ID_real[popuList[class_curr]]].real_ID = popuList[class_curr]
                    classArr[class_ID_real[popuList[class_curr]]].timeslot = time
                    one_done = True
                else:
                    # if it can't be scheduled, add it to 'empty'
                    # print("added to empty")
                    empty.append(popuList[class_curr])
                    #print(f"hi:{popuList[class_curr]}")

                # print(f"class_curr:{class_curr}")
                class_curr += 1  # move to the next class in classArr

            # reset 'one_done' for the next iteration
            one_done = False
            time += 1
            
    return classArr

# defines class type
class Classes:
  def __init__(classes = 0, freq = 0, prof = 0, real_prof = 0, classroom = 0, timeslot = "-1", aval = 0, students = "", real_ID = '-1'):
    classes.freq = freq # popularity
    classes.prof = prof
    classes.real_prof = real_prof
    classes.classroom = classroom
    classes.timeslot = timeslot
    classes.aval = aval
    classes.students = students
    classes.real_ID = real_ID

# defines Slot type
class Slot:
    def __init__(slot, start_hour, start_minute, end_hour, end_minute, day):
        slot.start_hour = start_hour
        slot.start_minute = start_minute
        slot.end_hour = end_hour
        slot.end_minute = end_minute
        slot.day = day
    
    def __str__(slot):
        return f"{slot.start_hour}:{slot.start_minute} - {slot.end_hour}:{slot.end_minute} {slot.day}"

def if_conflict(slot1, slot2):
    day1 = slot1.day
    day2 = slot2.day
    
    days = ["M", "T", "W", "TH", "F"]

    
    if "-" in day1:
        start, end = day1.split("-")
        start_index = days.index(start)
        end_index = days.index(end)
        meeting_days1 = days[start_index:end_index + 1]
    else:
        meeting_days1 = []
        if "TH" in day1:
            meeting_days1 = ["TH"]
            day1 = day1.replace("TH", "")
        for i in days:
            if i in day1:
                meeting_days1.append(i)
        
    if "-" in day2:
        start, end = day2.split("-")
        start_index = days.index(start)
        end_index = days.index(end)
        meeting_days2 = days[start_index:end_index + 1]
    else:
        meeting_days2 = []
        if "TH" in day2:
            meeting_days2 = ["TH"]
            day2 = day2.replace("TH", "")
        for i in days:
            if i in day2:
                meeting_days2.append(i)

    a = False
    
    slot1d=slot1
    slot2d=slot2
    
    if (int(slot1d.start_hour) > int(slot2d.start_hour)):
        temp = slot1d
        slot1d = slot2d
        slot2d = temp
    
    if (int(slot1d.start_hour) == int(slot2d.start_hour)):
        if int(slot1d.start_minute) > int(slot2d.start_minute):
            temp = slot1d
            slot1d = slot2d
            slot2d = temp
    
    for i in meeting_days1:
        if i in meeting_days2:
            if int(slot1d.end_hour) > int(slot2d.start_hour):
                return True
            elif int(slot1d.end_hour) == int(slot2d.start_hour):
                if int(slot1d.end_minute) > int(slot2d.start_minute):
                    return True
    return a
        
# function to assign students to the schedule
def assign(classArr, stuArr, classroomArr, class_ID_real, student_ID_real, timeArr):
    score = 0
    for a in classArr:
        a.aval = classroomArr[a.classroom]
    i = 0
    for stu in stuArr:
        # print(stu)
        occu_times = []
        for j in range(10):
            if(stu[j] != -1):
                if stu[j] in class_ID_real:
                    if(classArr[class_ID_real[stu[j]]].aval > 0):
                        timeslot = classArr[class_ID_real[stu[j]]].timeslot
                        # print(timeslot)
                        can = True # the class CAN be added to the current schedule
                        
                        for occu in occu_times:
                            # print(occu)
                            if if_conflict(timeArr[int(occu)], timeArr[int(timeslot)]):
                                can = False
                        
                        if can:
                            occu_times.append(timeslot)
                            # print(stu)
                            score += 1
                            classArr[class_ID_real[stu[j]]].students = f"{classArr[class_ID_real[stu[j]]].students} {student_ID_real[i]}"
                            classArr[class_ID_real[stu[j]]].aval = classArr[class_ID_real[stu[j]]].aval - 1
        i = i + 1
    return score


def best_timeslot(timeArr, index):
    arr = sorted(index, key=lambda x: int(timeArr[x].end_hour), reverse=False)
    # for i in arr:
    #     print(f"arr:{timeArr[i]}")
    # print(f"arr:{arr}")
    """
    index = [0, 2, 4, 5]
    arr = [2, 5, 0, 4]
    timeArr[arr[x]]
    gen --> [0, 2, 3]
    arr[0] = ?
    resultArr = [2, 0, 4]
    """
    arr_temp=[int]* len(arr)
    for i in range(len(arr)):
        arr_temp[i] = arr[i] #index
        arr[i] = timeArr[arr[i]] #timeSlot
    pred = []
    n = len(arr)
    findMaxProfit(arr, n)
    result = gen_schedule(n, arr)
    resultArr = []
    for i in result:
        resultArr.append(arr_temp[i])
    return resultArr

# function to print results in tabular format
def save_results_to_file(filename, headers, results, classroomName, timeArr):
    # Open a new file with the specified name in write mode
    with open(filename, 'w') as file:
        # Write the headers on the first line
        file.write("".join(f"{header}" for header in headers) + "\n")
        i = 1
        # Write each set of values in results on a new line
        for result in results:
            # Join values into a space-separated string and write to the file
            # re = ["1", result.classroom, result.prof, result.timeslot, result.students]
            student = result.students[1:]
            # print(result.students)
            time = int(result.timeslot) - 1
            # print(f"result.timeslot: {result.timeslot}")
            # print(f"time:{time}")
            file.write(
                f"{str(result.real_ID).zfill(6)}\t{classroomName[int(result.classroom)]}\t{result.real_prof}\t{timeArr[time]}\t{student}\n"
            )
            i += 1

def main():
    if len(sys.argv) < 3:
        print("python ds.py <constrain.txt> <student_preference.txt")
        return

    constrain = sys.argv[1]
    preference = sys.argv[2]

    classNum = -1
    
    # open the file in read mode
    with open(constrain, 'r') as file:
        for line in file:
            # split the line by spaces
            parts = line.strip().split()

            # get the number of entities
            if parts[0] == "Classes":
                classNum = int(parts[1])
            elif parts[0] == "Class":
                timeNum = int(parts[2])
            elif parts[0] == "Rooms":
                roomNum = int(parts[1])
            elif parts[0] == "Teachers":
                profNum = int(parts[1])
    
    with open(preference, 'r') as file:
        i = 0
        for line in file:
            parts = line.strip().split()

            if parts[0] == "Students":
                stuNum = int(parts[1])
                stuArr = [[-1]*10 for _ in range(stuNum)] # each student at most prefers 6 classes
                student_ID_real = {}

            else:
                student_ID_real[i]=int(parts[0])
                # print(stuArr)
                for j in range(len(parts) - 1):
                    # print(j)
                    stuArr[i][j] = int(parts[j+1])
                i += 1
                
    # print(stuArr) #DONE
    
    first = False
    second = True
    slot = False
    b = True
    # initialize each array/list
    classArr = [None] * classNum
    classroomArr = [None] * roomNum # stores the room capacities
    classroomName = [None] * roomNum
    profArr = [[-1 for _ in range(profNum)] for _ in range(2)] # 2 * profArr array, initialized to -1
    timeArr = [None] * timeNum
    with open(constrain, 'r') as file:
        for line_1 in file:
            parts_1 = line_1.strip().split()
            if parts_1[0] == "Class":
                slot = True
                s = 0
            if parts_1[0] == "Classes":
                slot = False
                second = False
                first = False
                i = 0
                class_ID_real = {}
                j = 0
                prof_ID_real = {}
                # print("b")
            if parts_1[0] == "Rooms":
                slot = False
                first = True
                room_ID_real = [None] * roomNum
                i = 0
                # print("a")
                continue
            if not first:
                try:
                    # Try converting parts[0] to an integer
                    first_index = int(parts_1[0])
                except ValueError:
                    continue
            # print(line_1)
            if slot and b:
                start_hour = (parts_1[1].split(':')[0])# +12
                start_minute = (parts_1[1].split(':')[1])
                
                if 'PM' in parts_1[2] and start_hour!="12":
                    start_hour = int(start_hour) + 12
                    start_hour = str(start_hour)
                
                end_hour = (parts_1[3].split(':')[0])# +12
                end_minute = (parts_1[3].split(':')[1])

                if 'PM' in parts_1[4] and end_hour!="12":
                    end_hour = int(end_hour) + 12
                    end_hour = str(end_hour)
                    
                day = str(parts_1[5])
                slot = Slot(start_hour, start_minute, end_hour, end_minute, day)
                timeArr[s] = slot
                s += 1
                # if s == 60:
                #     b = False
            elif first == True and second == True:
                room_ID_real[i] = parts_1[0]
                classroomArr[i] = int(parts_1[1])
                classroomName[i] = parts_1[0]
                # print(int(parts_1[1]))
                i = i + 1
            elif not second:
                class_ID_real[int(parts_1[0])] = i
                # print(parts_1[0])
                #print(line_1)
                #print(j)
                # print(f"{profArr[0][prof_ID_real[parts_1[1]]]} and {profArr[1][prof_ID_real[parts_1[1]]]}")
                if int(parts_1[1]) not in prof_ID_real:
                    #print(parts_1[1])
                    prof_ID_real[int(parts_1[1])]=j
                    # print(parts_1[1])
                    # print(int(parts_1[0]))
                    profArr[0][j] = int(parts_1[0])
                    classArr[i] = Classes(prof = j, real_prof = parts_1[1], real_ID = int(parts_1[0]))
                    j = j + 1
                else:
                    # print(parts_1)
                    index = prof_ID_real[int(parts_1[1])]
                    classArr[i] = Classes(prof = index, real_prof = parts_1[1], real_ID = int(parts_1[0]))
                    profArr[1][index] = int(parts_1[0])
                i = i+1
    # DONE
    # print(classroomArr)
    classPopu = [] * classNum
    popuList = []
    for row in stuArr:
        for i in range(len(row)):
            index = row[i]
            if index != -1:
                if index in class_ID_real:
                    if index not in popuList:
                        popuList.append(index)
                    classArr[class_ID_real[index]].freq += 1
                    
    for prof in profArr:
        element = prof[0]
        if element not in popuList:
            popuList.append(element)
            classArr[element-1].freq = 0
        element = prof[1]
        if element not in popuList:
            popuList.append(element)
            classArr[element-1].freq = 0
    
    conflict_matrix = array = [[-1 for _ in range(classNum)] for _ in range(classNum)]
    conflictList = []
    for stu in stuArr:
        for i in stu:
            # print(class_ID_real[7125])
            if  i != -1 and (i in class_ID_real) and class_ID_real[i] != -1:
                for j in stu:
                    # print(j)
                    if j != -1 and (j in class_ID_real) and class_ID_real[j] != -1:
                        a = class_ID_real[i]
                        # print(conflict_matrix[a][0])
                        if i != j:
                            if conflict_matrix[class_ID_real[i]][class_ID_real[j]] == -1:
                                conflict_matrix[class_ID_real[i]][class_ID_real[j]] = 1
                            else:
                                conflict_matrix[class_ID_real[i]][class_ID_real[j]] += 1
                            if conflict_matrix[class_ID_real[i]][class_ID_real[j]] == -1:
                                conflict_matrix[class_ID_real[i]][class_ID_real[j]] = 1
                            else:
                                conflict_matrix[class_ID_real[i]][class_ID_real[j]] += 1
    conflict_matrix = np.array(conflict_matrix)
    conflict_matrix = np.array(conflict_matrix)
    df = pd.DataFrame(conflict_matrix)
    # print(df)
    
    while True:
        max_index, max_index2 = np.unravel_index(np.argmax(conflict_matrix), conflict_matrix.shape)
        if (conflict_matrix[max_index][max_index2] == 0) or (conflict_matrix[max_index][max_index2] == -999999) or (conflict_matrix[max_index][max_index2] == -1):
            break
        conflict_matrix[max_index][max_index2] = -999999
        conflict_matrix[max_index2][max_index] = -999999
        if classArr[max_index].real_ID not in conflictList:
            conflictList.append(classArr[max_index].real_ID)
        if classArr[max_index2].real_ID not in conflictList:
            conflictList.append(classArr[max_index2].real_ID)
    # print(conflictList)
    
    filteredList = [x for x in popuList if x != -1]
    popuList = sorted(filteredList, key=lambda x: classArr[class_ID_real[x]].freq, reverse=True)

    for i in popuList:
        if i not in conflictList:
            conflictList.append(i)

    # print(popuList[1])
    roomList = []
    roomList = list(range(roomNum)) # storing integers from 0 to roomNum - 1
    roomList = sorted(roomList, key=lambda x: classroomArr[x], reverse=True)

    new_timeArr = []
    MWF = []
    MW_F = []
    M_WF = [] 
    M_W_F = []
    TTH = []
    T_TH = []
    for i, time in enumerate(timeArr):
        if time != None:
            if time.day == "MWF":
                MWF.append(i)
                # print(time.day)
            elif time.day == "M" or time.day == "WF":
                M_WF.append(i)
            elif time.day == "MW" or time.day == "F":
                MW_F.append(i)
            elif time.day == "M" or time.day == "W" or time.day == "F":
                M_W_F.append(i)
            elif time.day == "TTH":
                TTH.append(i)
            elif time.day == "T" or time.day == "TH":
                # print(time.day)
                T_TH.append(i)

    MWF_list = [MWF, MW_F, M_WF, M_W_F]
    max_MWF = 0
    idx_MWF = []
    for i in range(len(MWF_list)):
        best = best_timeslot(timeArr,MWF_list[i])
        if len(best) > max_MWF:
            max_MWF = len(best)
            idx_MWF = best

    TTH_list = [TTH, T_TH]
    max_TTH = 0
    idx_TTH = []

    for i in range(len(TTH_list)):
        best = best_timeslot(timeArr,TTH_list[i])
        if len(best) > max_TTH:
            max_TTH = len(best)
            idx_TTH = best
    
    for i in idx_TTH:
        # print(f"TTh{timeArr[i]}")
        new_timeArr.append(timeArr[int(i)])
    for i in idx_MWF:
        new_timeArr.append(timeArr[int(i)])
        # print(f"MWF{timeArr[i]}")
    timeArr = new_timeArr
    # for i in timeArr:
    #     print(i)
    timeNum = len(timeArr)
    # print(len(timeArr))
    result = schedule_classes(classArr, classroomArr, timeNum, roomList, conflictList, profArr, class_ID_real, prof_ID_real, timeArr)

    score = assign(result, stuArr, classroomArr, class_ID_real, student_ID_real, timeArr)

    print(f"{score}")
    total_class = 0
    for stu in stuArr:
        for i in stu:
            if i != -1:
                total_class+=1
    print(score/(total_class))

    filename = sys.argv[3]
    # headers = ["Course","Room","Teacher", "Time", "Students"]
    line = "Course Room Teacher Time Students"

    # Replace multiple spaces with a single tab
    headers = "\t".join(line.split(" "))
    save_results_to_file(filename, headers, result, classroomName, timeArr)

main()