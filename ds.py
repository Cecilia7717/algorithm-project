from array import array
import sys

# function to check if a class can fit into a classroom at a given time slot
def could(classObj, room, time, profArr, classArr):
    prof = classObj.prof
    prof_class1 = profArr[0][prof - 1]
    prof_class2 = profArr[1][prof - 1]

    if classArr[prof_class1 - 1].timeslot is not None:
        if (classArr[prof_class1 - 1].timeslot == time):
            return False

    if classArr[prof_class2 - 1].timeslot is not None:
        if (classArr[prof_class2 - 1].timeslot == time):
            return False

    return True


def schedule_classes(classArr, classroomArr, timeSlots, roomList, popuList, profArr):
    empty = []  # list to store classes that couldn't be scheduled
    class_curr = 0  # current class index in the sorted class list
    one_done = False  # boolean to check if scheduling is complete

    # iterate over each classroom in descending order of size
    for roomID in roomList:
        # iterate over each time slot
        for time in range(timeSlots):
            # try the classes in 'empty' list first
            if empty:  # if there are classes in 'empty'
                for c in empty:
                    if could(classArr[c], classroomArr[roomID], time, profArr, classArr):
                        # print(f"empty classid:{c}time:{time} room:{roomID}")#hhhhhh
                        classArr[c].classroom = roomID
                        classArr[c].timeslot = time
                        one_done = True
                        empty.remove(c)
                        break  # stop traversing 'empty'
                    
            # if no class from `empty` could be scheduled, try scheduling the class in classArr
            while not one_done:
                if class_curr == len(popuList): # if all classes are scheduled
                    return classArr
                # print(f"popu{len(popuList)}, class_curr{class_curr}")
                # try assigning the current class to the current room and time
                if could(classArr[popuList[class_curr] - 1], classroomArr[roomID], time, profArr, classArr):
                    classArr[popuList[class_curr] - 1].classroom = roomID
                    classArr[popuList[class_curr] - 1].timeslot = time
                    # print(f"classid:{popuList[class_curr]-1}time:{time} room:{roomID}")#hhhhhh
                    one_done = True
                else:
                    # if it can't be scheduled, add it to 'empty'
                    empty.append(popuList[class_curr] - 1)

                class_curr += 1  # move to the next class in classArr

            # reset 'one_done' for the next iteration
            one_done = False
    
    return classArr


class Classes:
  def __init__(classes = 0, freq = 0, prof = 0, classroom = 0, timeslot = "0", aval = 0, students = ""):
    classes.freq = freq # opularity
    classes.prof = prof
    classes.classroom = classroom
    classes.timeslot = timeslot
    classes.aval = aval
    classes.students = students

def assign(classArr, stuArr, classroomArr):
    score = 0
    for a in classArr:
        a.aval = classroomArr[a.classroom]
        # CHECKED: print(classroomArr[a.classroom])
    i = 1
    for stu in stuArr:
        if classArr[stu[0]-1].aval > 0:
            score += 1
            classArr[stu[0]-1].students = f"{classArr[stu[0]-1].students} {i}"
            classArr[stu[0]-1].aval = classArr[stu[0]-1].aval - 1
        if classArr[stu[1]-1].aval > 0:
            if classArr[stu[0]-1].timeslot != classArr[stu[1]-1].timeslot:
                score += 1
                classArr[stu[1]-1].students = f"{classArr[stu[1]-1].students} {i}"
                classArr[stu[1]-1].aval = classArr[stu[1]-1].aval - 1
        if classArr[stu[2]-1].aval > 0:
            if (classArr[stu[0]-1].timeslot != classArr[stu[2]-1].timeslot) and (classArr[stu[1]-1].timeslot != classArr[stu[2]-1].timeslot):
                score += 1
                classArr[stu[2]-1].students = f"{classArr[stu[2]-1].students} {i}"
                classArr[stu[2]-1].aval = classArr[stu[2]-1].aval - 1
        if classArr[stu[3] - 1].aval > 0:
            if classArr[stu[0]-1].timeslot != classArr[stu[3]-1].timeslot:
                if (classArr[stu[1]-1].timeslot != classArr[stu[3]-1].timeslot) and (classArr[stu[2]-1].timeslot != classArr[stu[3]-1].timeslot):
                    score += 1
                    classArr[stu[3]-1].students = f"{classArr[stu[3]-1].students} {i}"
                    classArr[stu[3]-1].aval = classArr[stu[3]-1].aval - 1
        i += 1
    return score
        
def save_results_to_file(filename, headers, results):
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
            time = int(result.timeslot) + 1
            file.write(
                f"{i}\t{int(result.classroom)+1}\t{result.prof}\t{time}\t{student}\n"
            )
            i += 1

def main():
    if len(sys.argv) < 3:
        print("python ds.py <constrain.txt> <student_preference.txt")
        return

    constrain = sys.argv[1]
    preference = sys.argv[2]

    classNum = -1
    first = True
    # Open the file in read mode
    with open(constrain, 'r') as file:
        # To set the size of each array/list
        for line in file:
            # Split the line by spaces
            parts = line.strip().split()

            # Check if the first element is "classes"
            if parts[0] == "Classes":
                classNum = int(parts[1]) # CHECK: print(classNum)
            elif parts[0] == "Class":
                timeNum = int(parts[2])
            elif parts[0] == "Rooms":
                roomNum = int(parts[1])
            elif parts[0] == "Teachers":
                teacherNum = int(parts[1])

    with open(preference, 'r') as file:
        for line in file:
            parts = line.strip().split()

            if parts[0] == "Students":
                stuNum = int(parts[1])
                stuArr = [[-1]*4 for _ in range(stuNum)]
                # print(stuArr)
            else:
                # print(parts[1])
                stuArr[int(parts[0]) - 1][0] = int(parts[1])
                stuArr[int(parts[0]) - 1][1] = int(parts[2])
                stuArr[int(parts[0]) - 1][2] = int(parts[3])
                stuArr[int(parts[0]) - 1][3] = int(parts[4])

    # print(stuArr)


    # To initialize each array/list
    classArr = [None] * classNum # classArr = [None] * classNum
    classroomArr = [None] * roomNum # size for each classroom
    profArr = [[0 for _ in range(teacherNum)] for _ in range(2)] # print(profArr)
    
    with open(constrain, 'r') as file:
        # To store value into each array/list
        for line_1 in file:
            parts_1 = line_1.strip().split()
            if parts_1[0] == "Classes":
                first = False
            try:
                # Try converting parts[0] to an integer
                first_index = int(parts_1[0])
            except ValueError:
                continue
            if first:
                classroomArr[int(parts_1[0])-1] = int(parts_1[1])
            else:
                classArr[int(parts_1[0]) -1] = Classes(prof = int(parts_1[1]))
                if profArr[0][int(parts_1[1]) - 1] == 0:
                    profArr[0][int(parts_1[1]) - 1] = int(parts_1[0])
                else:
                    profArr[1][int(parts_1[1]) - 1] = int(parts_1[0])

    classPopu = [] * classNum
    popuList = []
    for row in stuArr:
        index = row[0]
        # print(f"hhh{index}")
        if index not in popuList:
            popuList.append(index)
        classArr[index-1].freq += 1
        index = row[1]
        if index not in popuList:
            popuList.append(index)
        classArr[index-1].freq += 1
        index = row[2]
        if index not in popuList:
            popuList.append(index)
        classArr[index-1].freq += 1
        index = row[3]
        if index not in popuList:
            popuList.append(index)
        classArr[index-1].freq += 1
        
    for prof in profArr:
        element = prof[0]
        # print(f"fff{element}")
        if element not in popuList:
            popuList.append(element)
            classArr[element-1].freq = 0
        element = prof[1]
        # print(f"fff{element}")
        if element not in popuList:
            popuList.append(element)
            classArr[element-1].freq = 0
    
    popuList = sorted(popuList, key=lambda x: classArr[x - 1].freq, reverse=True) # list of class indices in descending popularity
    roomList = []
    roomList = list(range(roomNum)) # storing integers from 0 to roomNum - 1
    roomList = sorted(roomList, key=lambda x: classroomArr[x], reverse=True)

    result = schedule_classes(classArr, classroomArr, timeNum, roomList, popuList, profArr)

    """for i, a in enumerate(result):
        print(i,end=":")
        print(a.timeslot, end=";")
        print(a.classroom)"""

    score = assign(result, stuArr, classroomArr)

    print(f"{score}")

    print(score/(stuNum*4))

    #print(roomNum)
    #print(classNum)
    #print(timeNum)
    #print(stuNum)
    filename = sys.argv[3]
    #headers = ["Course","Room","Teacher", "Time", "Students"]
    line = "Course Room Teacher Time Students"

    # Replace multiple spaces with a single tab
    headers = "\t".join(line.split(" "))
    save_results_to_file(filename, headers, result)

main()