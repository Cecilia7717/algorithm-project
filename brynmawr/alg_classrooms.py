from array import array
import sys

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

# function to schedule
def schedule_classes(classArr, classroomArr, timeSlots, roomList, popuList, profArr, class_ID_real, timeArr, classroomName):
    empty = []  # list to store classes that couldn't be scheduled
    class_curr = 0  # current class index in the sorted class list
    one_done = False  # boolean to check if scheduling is complete
    # iterate over each classroom in descending order of size
    for roomID in roomList:
        # iterate over each time slot
        time = 0
        while time != timeSlots:
            print("")
            # print(f"classroom: {classroomName[roomID]}")
            # try the classes in 'empty' list first
            if empty:  # if there are classes in 'empty'
                for c in empty:
                    if could_wy(classArr[class_ID_real[c]], classroomArr[roomID], time, profArr, classArr, class_ID_real, timeArr):
                        if classroomName[roomID] in classArr[class_ID_real[c]].dept.classrooms:
                            # print("{}")
                            classArr[class_ID_real[c]].classroom = roomID
                            classArr[class_ID_real[c]].timeslot = time
                            classArr[class_ID_real[c]].real_ID = c
                            one_done = True
                            empty.remove(c)
                            break # stop traversing 'empty'
            
            # if no class from `empty` could be scheduled, try scheduling the class in classArr
            while not one_done:
                # if class_curr == len(popuList): # if all classes are scheduled
                if class_curr == len(popuList) and not empty:
                    return classArr
                
                # try assigning the current class to the current room and time
                if could_wy(classArr[class_ID_real[popuList[class_curr]]], classroomArr[roomID], time, profArr, classArr, class_ID_real, timeArr):
                    if classroomName[roomID] in classArr[class_ID_real[popuList[class_curr]]].dept.classrooms:
                        classArr[class_ID_real[popuList[class_curr]]].classroom = roomID
                        classArr[class_ID_real[popuList[class_curr]]].real_ID = popuList[class_curr]
                        classArr[class_ID_real[popuList[class_curr]]].timeslot = time
                        one_done = True
                    else:
                        # if it can't be scheduled, add it to 'empty'
                        empty.append(popuList[class_curr])
                else:
                    # if it can't be scheduled, add it to 'empty'
                    empty.append(popuList[class_curr])

                # print(f"class_curr:{class_curr}")
                class_curr += 1  # move to the next class in classArr

            # reset 'one_done' for the next iteration
            one_done = False
            time += 1
            
            if class_curr >= len(popuList):
                one_done = True

    return classArr

# defines class type
class Classes:
  def __init__(classes = 0, freq = 0, prof = 0, real_prof = 0, classroom = 0, timeslot = "-1", aval = 0, students = "", real_ID = '-1', dept = None):
    classes.freq = freq # popularity
    classes.prof = prof
    classes.real_prof = real_prof
    classes.classroom = classroom
    classes.timeslot = timeslot
    classes.aval = aval
    classes.students = students
    classes.real_ID = real_ID
    classes.dept = dept

# defines Department type
class Department:
    def __init__(dept = 0, classrooms = None):
        if classrooms is None:
            classrooms = []
        dept.classrooms = classrooms

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
    dept_dict = {}
    
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
            elif parts[0].isdigit() and len(parts[0]) == 6: # get departments
                if parts[2] not in dept_dict:
                    deptrooms = []
                    for part in parts[3:]:
                        if part not in deptrooms:
                            deptrooms.append(part)
                    dept = Department(deptrooms)
                    dept_dict[parts[2]] = dept
    
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
                    
    first = False
    second = True
    slot = False

    # initialize arrays
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
            if slot:
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
                # print(start_hour)
                # print(start_minute)
                # print(end_hour)
                # print(end_minute)
                # print(day)
                slot = Slot(start_hour, start_minute, end_hour, end_minute, day)
                # print(str(slot))
                timeArr[s] = slot
                s += 1
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
                    classArr[i] = Classes(prof = j, real_prof = parts_1[1])
                    j = j + 1
                else:
                    # print(int(parts_1[0]))
                    index = prof_ID_real[int(parts_1[1])]
                    classArr[i] = Classes(prof = index, real_prof = parts_1[1])
                    profArr[1][index] = int(parts_1[0])
                i = i+1

    # open the file in read mode
    with open(constrain, 'r') as file:
        for line in file:
            parts = line.strip().split()

            if parts[0].isdigit() and len(parts[0]) == 6:
                classArr[class_ID_real[int(parts[0])]].dept = dept_dict[parts[2]]
    
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

    filteredList = [x for x in popuList if x != -1]
    popuList = sorted(filteredList, key=lambda x: classArr[class_ID_real[x]].freq, reverse=True)
    # print(popuList)

    roomList = []
    roomList = list(range(roomNum)) # storing integers from 0 to roomNum - 1
    roomList = sorted(roomList, key=lambda x: classroomArr[x], reverse=True)

    result = schedule_classes(classArr, classroomArr, timeNum, roomList, popuList, profArr, class_ID_real, timeArr, classroomName)

    score = assign(result, stuArr, classroomArr, class_ID_real, student_ID_real, timeArr)

    print(f"{score}")
    total_class = 0
    for stu in stuArr:
        for i in stu:
            if i != -1:
                total_class+=1
    print(score/(total_class))

    filename = sys.argv[3]
    #headers = ["Course","Room","Teacher", "Time", "Students"]
    line = "Course Room Teacher Time Students"

    # replace multiple spaces with a single tab
    headers = "\t".join(line.split(" "))
    save_results_to_file(filename, headers, result, classroomName, timeArr)
    
    for id in roomList:
        print(f"{classroomName[id]} --- {classroomArr[id]}")
    
    # for cls in popuList[:5]:  # Slicing to get the first 5 elements
    #     print(f"class: {cls}")
    #     print(f"avail: {classroomArr[classArr[class_ID_real[cls]].classroom]}")
    

main()