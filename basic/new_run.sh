#!/bin/bash
array_of_arrays=(
    [0]="100 5 10 20"
    [1]="100 10 5 20"
    [2]="200 5 10 20"
    [3]="200 10 5 20"
    [4]="200 10 20 40"
    [5]="200 20 10 40"
    [6]="400 10 20 40"
    [7]="400 20 10 40"
    [8]="400 30 30 80"
    [9]="600 30 30 80"
    [10]="600 30 30 100"
    [11]="800 30 30 100"
    [12]="1000 30 30 100"
    [13]="2000 30 30 100"
    [14]="1000 30 30 200"
    [15]="2000 30 30 200"
    [16]="3000 30 30 200"
)
mkdir schedule
mkdir constr
mkdir studprefs
i=1
for row in "${array_of_arrays[@]}"; do
    # Read the row into an array to access each element by index
    read -a values <<< "$row"
    
    echo "Starting iteration $i..."
    start_time=$(date +%s)

    for v in {1..10}; do
        # Uncomment the following line if you need the Perl command
        perl make_random_input.pl ${values[0]} ${values[3]} ${values[2]} ${values[1]} /home/zchen4/340/basic/constr/constr_${i}_${v}.txt /home/zchen4/340/basic/studprefs/studprefs_${i}_${v}.txt
        
        # Measure time for each Python command
        time python3 ~/340/ds.py /home/zchen4/340/basic/constr/constr_${i}_${v}.txt /home/zchen4/340/basic/studprefs/studprefs_${i}_${v}.txt /home/zchen4/340/basic/schedule/schedule_${i}_${v}.txt 
    done 

    end_time=$(date +%s)
    duration=$(( end_time - start_time ))
    
    echo "Iteration $i completed in ${duration} seconds."

    ((i++))
done