#!/bin/bash
array_of_arrays=(
    [0]="100 1000 100 500000"
    [1]="1000 2000 100 500000"
    [2]="1000 10000 100 500000"
    [3]="1000 20000 100 500000"
    [4]="1000 50000 100 500000"
    [5]="1000 60000 100 500000"
    [6]="1000 80000 100 500000"
    [7]="1000 100000 100 500000"
)

# <number of rooms> <number of classes> <number of class times> <number of students> <contraint file> <student prefs file>
i=1

mkdir constr_class_large
mkdir studprefs_class_large
mkdir schedule_class_large

for row in "${array_of_arrays[@]}"; do
    # Read the row into an array to access each element by index
    read -a values <<< "$row"
    
    echo "Starting iteration $i..."
    start_time=$(date +%s)

    for v in {1..10}; do
        # Uncomment the following line if you need the Perl command
        perl make_random_input.pl ${values[0]} ${values[1]} ${values[2]} ${values[3]} /home/cecilia/340/basic/constr_class_large/constr_${i}_${v}.txt /home/cecilia/340/basic/studprefs_class_large/studprefs_${i}_${v}.txt
        
        # Measure time for each Python command/home/zchen4/340/basic/constr_large/constr_2_2.txt'
        time python3 ~/340/ds.py /home/cecilia/340/basic/constr_class_large/constr_${i}_${v}.txt /home/cecilia/340/basic/studprefs_class_large/studprefs_${i}_${v}.txt /home/cecilia/340/basic/schedule_class_large/schedule_${i}_${v}.txt
        # perl is_valid.pl /home/cecilia/340/basic/constr_show/constr_${i}_${v}.txt /home/cecilia/340/basic/studprefs_show/studprefs_${i}_${v}.txt /home/cecilia/340/basic/schedule_show/schedule_${i}_${v}.txt
    done 

    end_time=$(date +%s)
    duration=$(( end_time - start_time ))
    
    echo "Iteration $i completed in ${duration} seconds."

    ((i++))
done