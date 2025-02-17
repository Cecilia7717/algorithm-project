# function to check if a class can fit into a classroom at a given time slot
def could(classObj, room, time):
    prof = classObj.prof
    prof_classes = profArr[prof - 1] # how to get the index of a prof in its array
    
    for other_class in prof_classes:
        if other_class.time is not None and other_class.classroom is not None:
            if other_class.time == time:
                return False  # conflict found
            
    return True



def schedule_classes(classArr, classroomArr, timeSlots):
    empty = []  # list to store classes that couldn't be scheduled
    class_curr = 0  # current class index in the sorted class list
    one_done = False  # boolean to check if scheduling is complete
    
    # iterate over each classroom in descending order of size
    for roomID in roomList:
        # iterate over each time slot
        for time in timeSlots:
            # try the classes in 'empty' list first
            if empty:  # if there are classes in 'empty'
                for c in empty:
                    if could(c, classroomArr[roomID], time):
                        c.classroom = classroomArr[roomID]
                        c.time = time
                        one_done = True
                        empty.remove(c)
                        break  # stop traversing 'empty'

            # if no class from `empty` could be scheduled, try scheduling the class in classArr
            while not one_done:
                
                if class_curr == len(classArr): # if all classes are scheduled
                    return

                # try assigning the current class to the current room and time
                if could(classArr[popuList[class_curr]], classroomArr[roomID], time):
                    classArr[popuList[class_curr]].classroom = classroomArr[roomID]
                    classArr[popuList[class_curr]].time = time
                    one_done = True
                else:
                    # if it can't be scheduled, add it to 'empty'
                    empty.append(classArr[class_curr])
                
                class_curr += 1  # move to the next class in classArr

            # reset 'one_done' for the next iteration
            one_done = False